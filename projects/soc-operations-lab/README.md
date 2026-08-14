# SOC Operations HomeLab

Repositorio de un laboratorio SOC reproducible construido con VirtualBox, Kali Linux, Ubuntu/Wazuh y un endpoint Windows 11. El proyecto prioriza ingeniería de detección verificable: separar telemetría de veredictos, reproducir escenarios controlados y documentar límites del motor antes de declarar una detección válida.

## Estado de detecciones

| Detección | Estado | Evidencia disponible |
|---|---|---|
| WFP Port Scan | **VALIDATED** | Eventos WFP reales, `archives.json`, `alerts.json` y pruebas negativas de NAT/MANAGEMENT. |
| Sysmon Network / Event ID 3 | **AUDITED / PENDING VALIDATION** | EID 3 confirmado en MANAGEMENT y NAT; falta una señal ATTACK real que permita validar el detector. |
| Windows brute force | **PENDING CONTROLLED VALIDATION** | Telemetría 4625 y reglas históricas documentadas; la correlación depende de que Windows proporcione una IP fuente utilizable. |
| FIM | **CONFIGURED / REVALIDATION PENDING** | Historial de ajuste de ruido de rutas de prueba; falta un paquete público de evidencias reproducibles. |
| YARA | **PENDING VALIDATION** | No hay configuración ni evidencia sanitizada suficiente para hacer una afirmación operativa. |

## Arquitectura

```text
                           Administration Plane
  Kali 192.168.57.1 ───────────────┬─────────────── Ubuntu/Wazuh 192.168.57.10
                                   │ SSH / SCP / WinRM
                                   └─────────────── Windows 11 192.168.57.20

                              Attack/Lab Plane
  Kali 192.168.56.1 ───────────────┬─────────────── Ubuntu/Wazuh 192.168.56.10
                                   │ controlled reconnaissance
                                   └─────────────── Windows 11 192.168.56.20

                              Internet/NAT Plane
             Ubuntu/Wazuh 10.0.2.3 ──────────────── Windows 11 10.0.2.15
```

| Network | CIDR | Kali | Ubuntu/Wazuh | Windows 11 | Purpose |
|---|---|---:|---:|---:|---|
| MANAGEMENT | `192.168.57.0/24` | `.1` | `.10` | `.20` | Administración: SSH, SCP/SFTP, WinRM y mantenimiento. |
| ATTACK/LAB | `192.168.56.0/24` | `.1` | `.10` | `.20` | Escenarios controlados de reconnaissance y detección. |
| NAT/INTERNET | `10.0.2.0/24` | — | `.3` | `.15` | Actualizaciones y telemetría externa normal. |

La separación evita que tráfico administrativo o NAT se clasifique como actividad del laboratorio. Más detalle: [arquitectura](docs/architecture/README.md).

## Flujo de datos

```text
Windows Security / Sysmon
        -> Wazuh Agent
        -> Wazuh Manager 4.14.7
        -> archives.json (ingesta)
        -> ruleset / correlación
        -> alerts.json (alertas)
        -> Filebeat / Indexer / Dashboard
```

`archives.json` demuestra que un evento ingresó; `alerts.json` demuestra que una regla creó una alerta. La visualización en Dashboard requiere una comprobación independiente de indexación.

## Caso destacado: WFP Port Scan

La detección WFP utiliza eventos Windows Security `5152`/`5157` inbound TCP, limitados a `192.168.56.0/24 -> 192.168.56.20`.

- `100500`: base de tracking silenciosa, nivel 6, anclada a la rama Security EventChannel.
- `100501`: correlación de señal alta nivel 10.
- `100502`: correlación de señal alta nivel 13.

Una prueba real produjo 34 eventos WFP sobre 15 puertos de destino crudos distintos y exactamente una alerta visible de cada umbral. Estos umbrales son **heurísticas de correlación**, no `COUNT(DISTINCT destinationPort)`. Consulta la [documentación WFP validada](detection-rules/WFP_PortScan_Detection_Final.md).

## Evidencia visual curada

El repositorio incluye ocho capturas técnicas revisadas de arquitectura, Wazuh, WFP y Sysmon. Las capturas conservan únicamente las direcciones privadas relevantes del HomeLab; no contienen secretos ni pantallas de autenticación. La evidencia WFP ilustra telemetría ATTACK/LAB y acompaña una detección **VALIDATED** de naturaleza heurística. La captura de Sysmon prueba la preparación del endpoint, pero Sysmon EID 3 continúa **AUDITED / PENDING VALIDATION**. Consulta el [inventario de evidencia](evidence/README.md) para el alcance y las limitaciones de cada imagen.

## Problemas técnicos reales resueltos

- Una regla oficial WFP `60104` de nivel 5 eclipsaba la base custom de nivel 1. La base validada quedó en nivel 6.
- Un escaneo generó múltiples eventos `5152`/`5157` por puerto. `ignore="60"` limita el flooding sin eliminar telemetría.
- `wazuh-logtest` con JSON archivado puede usar un decoder distinto de `windows_eventchannel`; la validación definitiva se hizo con eventos de producción.

## Tecnologías

- VirtualBox
- Kali Linux
- Ubuntu con Wazuh Manager 4.14.7
- Windows 11 con Wazuh Agent y Sysmon
- Windows Filtering Platform, Windows EventChannel, `jq`, Filebeat y Wazuh Indexer/Dashboard

## Navegación

- [Arquitectura](docs/architecture/README.md)
- [Guía de setup reproducible](docs/setup/README.md)
- [Operación y validación](docs/operations/validation-workflow.md)
- [Reglas de detección](detection-rules/)
- [Troubleshooting](docs/troubleshooting/)
- [Cronología técnica](docs/timeline/project-history.md)
- [Lecciones y limitaciones](project-notes/)
- [Inventario de evidencia](evidence/README.md)

## Principios del proyecto

1. No declarar una detección validada sin evidencia real.
2. Mantener telemetría legítima aunque quede fuera de un detector.
3. Documentar límites del rules engine y de la observabilidad.
4. No publicar claves, contraseñas, tokens, transcripciones internas ni configuraciones con secretos.

## Licencia

Este proyecto se publica bajo [MIT](LICENSE).
