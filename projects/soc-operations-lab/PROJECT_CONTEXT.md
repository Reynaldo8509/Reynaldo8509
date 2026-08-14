# Contexto maestro persistente — SOC HomeLab

> Propósito: punto de partida técnico para futuras sesiones. Resume únicamente decisiones, estado y límites persistentes; no reemplaza las evidencias ni las configuraciones activas. Última consolidación: 2026-08-13.

## 1. Objetivo del SOC HomeLab

Construir un laboratorio SOC reproducible, basado en VirtualBox, que permita diseñar y validar detecciones Windows con evidencia verificable. El criterio del proyecto es separar claramente la telemetría recibida de una alerta creada, ejecutar escenarios autorizados y controlados, y no declarar una detección como validada hasta comprobar su comportamiento con eventos reales.

El caso de uso principal terminado es la detección heurística de reconocimiento/port scan mediante eventos WFP de Windows. Sysmon EID 3, brute force, YARA y FIM conservan estados distintos y no deben presentarse como equivalentes a esa validación.

## 2. Arquitectura

| Componente | Rol persistente |
|---|---|
| Kali Linux | Administración desde MANAGEMENT y ejecución de escenarios controlados desde ATTACK/LAB. |
| Ubuntu / Wazuh Manager 4.14.7 | Recibe Windows EventChannel, analiza y correlaciona eventos, guarda archivos locales y alimenta el pipeline de alertas. |
| Windows 11 Endpoint | Endpoint monitorizado con Wazuh Agent, Windows Security EventChannel, Sysmon y FIM. |
| VirtualBox | Plataforma de virtualización y segmentación de los adaptadores/redes del laboratorio. |

Flujo de telemetría:

```text
Windows Security / Sysmon -> Wazuh Agent -> Ubuntu Wazuh Manager
  -> archives.json (ingesta) -> ruleset/correlación -> alerts.json (alerta)
  -> Filebeat -> Wazuh Indexer -> Wazuh Dashboard
```

`archives.json` prueba que el manager ingirió y decodificó el evento. `alerts.json` prueba que una regla creó una alerta. La indexación y la visualización en Dashboard son una capa independiente que exige una consulta autenticada al índice o una comprobación visible en la UI.

## 3. Tres redes

| Red | CIDR | Kali | Ubuntu / Wazuh | Windows 11 |
|---|---|---:|---:|---:|
| MANAGEMENT | `192.168.57.0/24` | `192.168.57.1` | `192.168.57.10` | `192.168.57.20` |
| ATTACK/LAB | `192.168.56.0/24` | `192.168.56.1` | `192.168.56.10` | `192.168.56.20` |
| NAT/INTERNET | `10.0.2.0/24` | — | `10.0.2.3` | `10.0.2.15` |

## 4. Propósito de cada red

- **MANAGEMENT:** administración, SSH, SCP/SFTP, WinRM, mantenimiento y transferencia de archivos. Es telemetría legítima y no debe clasificarse por defecto como ataque.
- **ATTACK/LAB:** único plano destinado a reconnaissance y pruebas de detección controladas contra activos del laboratorio. Para el detector WFP, solo el tráfico desde esta red hacia Windows es elegible.
- **NAT/INTERNET:** actualizaciones, repositorios y conectividad externa normal. Su telemetría se conserva para investigación, pero no alimenta el detector WFP de port scan.

## 5. Wazuh

- **Versión del manager:** `4.14.7`.
- **Ubicación del manager:** VM Ubuntu; direcciones `192.168.57.10`, `192.168.56.10` y `10.0.2.3` según el plano.
- **Reglas locales activas:** `/var/ossec/etc/rules/local_rules.xml` en el manager.
- **Archivos de evidencia operativa:** `/var/ossec/logs/archives/archives.json` y `/var/ossec/logs/alerts/alerts.json`.

### Validación de reglas

`local_rules.xml` puede contener fragmentos con varios grupos de nivel superior, por lo que se valida el fragmento mediante un wrapper temporal, sin modificar el archivo real:

```bash
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
```

Tratar cualquier warning nuevo de `wazuh-analysisd -t` como fallo que debe investigarse, incluso si el proceso devuelve código cero. Después de un cambio autorizado, validar con EventChannel real y comprobar tanto `archives.json` como `alerts.json`; no basta con `wazuh-logtest` ni con la salud de Filebeat.

## 6. WFP Port Scan

**Estado: VALIDATED.** Es un detector de alta señal y con throttling para el HomeLab, no un contador exacto de puertos únicos.

### Reglas y ruta efectiva

```text
windows_eventchannel -> 60000 -> 60001 -> 100500 -> 100501 / 100502
```

Las reglas están en `local_rules.xml` del manager:

| ID | Función | Parámetros/alcance clave |
|---:|---|---|
| `100500` | Base de tracking silenciosa | Nivel 6; `if_sid=60001`; Security EID `5152`/`5157`; inbound (`%%14592`), TCP (`6`), origen `192.168.56.0/24`, destino `192.168.56.20`; `no_log`. |
| `100501` | Correlación de señal alta | Nivel 10; `if_matched_sid=100500`; misma `sourceAddress`; distinto `destPort`; `frequency=10`, `timeframe=60`, `ignore=60`. |
| `100502` | Correlación de señal más alta | Nivel 13; misma lógica; `frequency=14`, `timeframe=60`, `ignore=60`. |

### Significado técnico de los parámetros

- **Nivel 6 en `100500`:** es necesario para ganar la comparación entre reglas hermanas de la rama Security. Con nivel 1, la regla oficial `60104` (nivel 5) eclipsaba la base custom. `60104` permanece sin cambios como telemetría de auditoría WFP; no es un veredicto de port scan.
- **`frequency`:** número de coincidencias históricas que la correlación requiere dentro de su ventana; no equivale a un conteo SQL ni a puertos únicos.
- **`timeframe=60`:** ventana móvil de correlación de 60 segundos.
- **`ignore=60`:** tras una alerta, suprime nuevas alertas de esa regla durante 60 segundos. Limita flooding, pero no deduplica eventos WFP ni garantiza una alerta única durante campañas largas.
- **`if_matched_sid=100500`:** las correlaciones cuentan la cadena base filtrada, no cualquier evento Windows.
- **`same_field sourceAddress`:** restringe la correlación a un mismo origen.
- **`different_field destPort`:** compara el puerto del evento actual con eventos previos. No construye ni mantiene un conjunto de puertos distintos.

### Limitación de cardinalidad

La validación real observó 34 eventos WFP para 15 puertos de destino crudos distintos; hubo repeticiones con `eventRecordID` únicos. En Wazuh 4.14.7, `different_field` filtra comparaciones de historial, pero no implementa `COUNT(DISTINCT destPort)`. Por ello, `100501` y `100502` son umbrales heurísticos de patrones rápidos, no afirmaciones de exactamente 10 o 15 puertos únicos. `frequency=14` en `100502` es una compensación empírica de la interacción de reglas hermanas y tampoco debe reinterpretarse como cardinalidad exacta.

### Evidencia y controles negativos

La prueba ATTACK/LAB real produjo 34 eventos WFP y una alerta visible de cada regla de correlación (`100501` y `100502`), mientras la base silenciosa recibió el resto aplicable. MANAGEMENT y NAT conservaron telemetría sin alimentar estas correlaciones. La salud de Filebeat, Indexer y Dashboard se comprobó en el momento de la validación, pero no se realizó una consulta autenticada a `wazuh-alerts-*` ni una búsqueda UI para probar de forma directa la visualización final.

## 7. Sysmon EID 3

**Estado: AUDITED / PENDING VALIDATION.** Esta cadena no es un detector validado de port scan.

Ruta oficial auditada:

```text
windows_eventchannel -> 60000 -> 60004 -> 61600 -> 61605 -> sysmon_event3
```

| ID | Función documentada |
|---:|---|
| `100409` | Base silenciosa de nivel 1: `if_group=sysmon_event3`, TCP, origen `192.168.56.0/24`, destino `192.168.56.20`. |
| `100420` | Correlación nivel 10: `if_matched_sid=100409`, `frequency=10`, `timeframe=60`, mismo `sourceIp`, distinto `destinationPort`. |
| `100421` | Correlación nivel 13: `if_matched_sid=100409`, `frequency=15`, `timeframe=60`, mismo `sourceIp`, distinto `destinationPort`. |

Se confirmó EID 3 real en MANAGEMENT (`192.168.57.1 -> 192.168.57.20:22`) y en NAT/INTERNET hacia servicios externos; esos casos no alimentaron `100409`. **Todavía no existe evidencia archivada de un EID 3 ATTACK real desde `192.168.56.1` hacia `192.168.56.20`.** Sin ese evento fuente no se puede validar en producción `100409`, `100420` ni `100421`.

Riesgos pendientes: la misma limitación de cardinalidad heurística; reglas hermanas que pueden competir al compartir la base; falta de `ignore` en las correlaciones; y posible eclipse por reglas oficiales Sysmon más específicas o una regla local dirigida al puerto 22. No elevar niveles ni rediseñar esta cadena por intuición antes de generar y archivar la señal ATTACK autorizada.

## 8. Otros detectores

| Detector | Estado documentado | Hecho comprobado / brecha |
|---|---|---|
| Windows brute force | TELEMETRY OBSERVED / PENDING DETECTION VALIDATION | Security EID `4625` da visibilidad de fallos y existe la regla oficial `60122`; una exportación sanitizada contiene fallos históricos, incluidos tres desde ATTACK/LAB. Para OpenSSH algunos eventos dejan `win.eventdata.ipAddress` como `-`, por lo que una correlación por IP aún no es fiable ni validada. |
| YARA | PENDING VALIDATION | No hay regla pública sanitizada, configuración de ejecución/recolección ni evidencia extremo a extremo en `archives.json` y `alerts.json`. El historial no basta para afirmar cobertura. |
| FIM / syscheck | CONFIGURED / REVALIDATION PENDING | Existe un ajuste estrecho histórico para reducir ruido en una ruta de pruebas conservando FIM fuera de ella. Falta un paquete sanitizado con configuración, cambio de archivo, evidencia de ingesta y alerta final. |

## 9. Principales lecciones aprendidas

1. Separar MANAGEMENT, ATTACK/LAB y NAT reduce falsos positivos sin perder telemetría útil.
2. Una regla base custom puede perder ante una hermana oficial de mayor nivel; validar la ruta EventChannel real es imprescindible.
3. La telemetría estándar (`60104`, por ejemplo) y el veredicto de detección son conceptos distintos.
4. `wazuh-logtest` con JSON pegado puede usar el decoder `json`, no la cadena `windows_eventchannel`; no sustituye una prueba real.
5. `archives.json` demuestra ingesta, `alerts.json` creación de alertas y una consulta/UI autenticada demuestra indexación/visualización.
6. `frequency`, `timeframe` y `different_field` no implementan cardinalidad exacta de puertos distintos.
7. Las pruebas negativas de MANAGEMENT y NAT son parte de la validación, no un detalle opcional.
8. La ausencia de EID 3 ATTACK es una brecha de evidencia, no una confirmación de que Sysmon o la correlación funcionen.

## 10. Limitaciones conocidas

- WFP `100501`/`100502` son heurísticas y no cuentan puertos únicos de forma exacta.
- `ignore=60` reduce alertas repetidas, pero una campaña de más de 60 segundos puede volver a generar alertas.
- La visualización final de WFP en Dashboard/Indexer no se verificó directamente mediante consulta autenticada; solo se comprobó la salud del pipeline y la creación local de alertas.
- Sysmon EID 3 no cuenta con la señal ATTACK fuente necesaria; sus correlaciones no tienen throttling y pueden competir con reglas más específicas.
- Brute force por IP en OpenSSH depende de disponer de un campo fuente real y correlacionable.
- YARA y FIM no tienen aún evidencia pública sanitizada de extremo a extremo.

## 11. Reglas importantes de operación

- No mezclar MANAGEMENT con ATTACK/LAB: solo ATTACK/LAB debe participar en escenarios de ataque y en la base WFP de este caso de uso.
- NAT conserva telemetría para investigación, aunque quede excluida de detectores específicos.
- No asumir cardinalidad exacta a partir de `frequency` o `different_field`.
- Validar producción con eventos reales en `archives.json` y alertas en `alerts.json`.
- Diferenciar siempre `wazuh-logtest` de EventChannel real y de la ruta de decoder/ruleset efectiva.
- Antes de un cambio autorizado de reglas: respaldo, wrapper `xmllint`, `wazuh-analysisd -t`, prueba positiva y negativas de MANAGEMENT/NAT, e inspección de evidencias.
- No publicar copias activas de Wazuh/Sysmon/YARA, transcripciones, capturas sin revisar, claves, contraseñas, tokens o respaldos de producción.

## 12. Estructura del repositorio

```text
soc-operations-lab/
├── README.md                         # visión general y estados
├── PROJECT_CONTEXT.md                # este contexto maestro
├── configs/                          # solo configuraciones sanitizadas (sin activos por ahora)
├── detection-rules/                  # WFP, Sysmon, brute force, YARA y FIM
├── docs/
│   ├── architecture/                 # diseño de redes y componentes
│   ├── operations/                   # flujo de validación e inventario
│   ├── setup/                        # material de reconstrucción parcial
│   ├── timeline/                     # cronología técnica
│   └── troubleshooting/              # incidencias WFP y Sysmon
├── evidence/                         # inventario y artefactos sanitizados/históricos
├── project-notes/                    # lecciones, mejoras y limitaciones
└── scripts/validation/               # comprobación de seguridad de publicación
```

La documentación pública no contiene las configuraciones activas de `ossec.conf`, Sysmon ni Wazuh, y los artefactos históricos privados permanecen fuera del repositorio.

## 13. Estado actual de GitHub

- Remoto configurado: `origin` apunta al repositorio GitHub `Reynaldo8509/soc-operations-lab`.
- Rama local actual: `main`.
- HEAD local observado: `89502f8023c95290c95ae144985062b584aa711f` (`Auto sync: 2026-04-30 20:06:20`). No se consultó el remoto durante esta consolidación, así que la relación actual de `main` con `origin/main` no está verificada.
- El árbol de trabajo ya contenía modificaciones, eliminaciones y archivos sin seguimiento antes de crear este contexto. Son cambios del usuario/proyecto y deben preservarse.
- En esta tarea no se ejecutaron `git add`, `git commit` ni `git push`.

## 14. Qué está terminado

- Arquitectura de tres redes y sus límites operativos documentados.
- Wazuh Manager 4.14.7 con recepción de Windows EventChannel en el laboratorio.
- Detector WFP `100500`/`100501`/`100502` validado con eventos reales ATTACK/LAB, controles negativos de MANAGEMENT/NAT y evidencias de `archives.json`/`alerts.json`.
- Documentación de la limitación de cardinalidad, prioridad de reglas y throttling WFP.
- Auditoría de la ruta oficial Sysmon EID 3 y exclusiones negativas de MANAGEMENT/NAT.
- Estructura de documentación, política de publicación y chequeo estático de patrones de secretos en el repositorio.

## 15. Qué está pendiente

1. Generar un evento Sysmon EID 3 ATTACK autorizado `192.168.56.1 -> 192.168.56.20`; después confirmar ruta final, reglas ganadoras, repetición de alertas y negativos MANAGEMENT/NAT.
2. Verificar indexación/visualización WFP mediante consulta autenticada a `wazuh-alerts-*` y/o búsqueda en Dashboard antes de afirmar visibilidad UI.
3. Validar brute force con un escenario autorizado y un campo de IP fuente realmente utilizable; documentar alerta y prueba negativa.
4. Preparar una regla YARA con procedencia/licencia, procedimiento de ejecución y evidencia sanitizada de ingesta, alerta y negativo.
5. Revalidar FIM con un cambio controlado, verificando que la exclusión limitada no oculte rutas fuera de su ámbito.
6. Publicar configuraciones reproducibles solo tras sanitización y revisión; reemplazar o retirar con autorización los placeholders vacíos de brute force.
7. Si se requiere conteo exacto de puertos distintos, diseñar y validar una normalización stateful externa al motor de reglas nativo.

## 16. Qué no debe modificarse sin una nueva decisión técnica

- Los límites y direccionamiento de MANAGEMENT, ATTACK/LAB y NAT.
- `100500`, `100501` y `100502`, incluidos el nivel 6, filtros ATTACK/LAB, umbrales y `ignore=60`, sin nueva evidencia de producción y pruebas negativas.
- Las reglas oficiales Wazuh, Windows Firewall y cualquier configuración activa de Wazuh/Sysmon, incluida `ossec.conf`, salvo alcance explícitamente autorizado.
- La telemetría de MANAGEMENT o NAT mediante supresión global para reducir ruido.
- La clasificación de Sysmon EID 3 como "validada" hasta capturar el evento ATTACK real requerido.
- La afirmación de que WFP cuenta puertos únicos exactamente o que Dashboard muestra alertas sin prueba directa.
- Publicación de claves, secretos, configuraciones activas, respaldos, transcripciones completas o capturas sin revisión de sensibilidad.
