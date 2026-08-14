# Inventario de evidencia

## Capturas visuales curadas

Las ocho capturas siguientes son copias sin modificar de material histórico revisado visualmente. Se conservan las direcciones privadas del HomeLab porque documentan las redes ATTACK/LAB y NAT descritas en el proyecto; no se incluyen direcciones públicas ni del rango privado excluido durante la revisión. Los originales permanecen fuera del repositorio.

| Image | Category | What it demonstrates |
|---|---|---|
| [windows-endpoint-attack-nat-connectivity.png](screenshots/windows-endpoint-attack-nat-connectivity.png) | Architecture / Windows endpoint | El endpoint Windows 11 tiene la interfaz ATTACK/LAB `192.168.56.20`, la interfaz NAT `10.0.2.15` y conectividad hacia el manager ATTACK/LAB. |
| [wazuh-windows-agent-enrollment.jpg](screenshots/wazuh-windows-agent-enrollment.jpg) | Wazuh / enrollment | El Dashboard muestra el flujo de enrolamiento del agente Windows y el manager ATTACK/LAB `192.168.56.10`. |
| [wazuh-endpoint-summary.jpg](screenshots/wazuh-endpoint-summary.jpg) | Wazuh / endpoint | Resumen histórico del endpoint Windows administrado por Wazuh 4.14.7. |
| [wazuh-events-explorer.jpg](screenshots/wazuh-events-explorer.jpg) | Wazuh / event exploration | Exploración histórica de eventos del endpoint en el Dashboard; aporta contexto de observabilidad, no una validación adicional de detector. |
| [wazuh-mitre-dashboard.jpg](screenshots/wazuh-mitre-dashboard.jpg) | Wazuh / MITRE | Vista histórica MITRE del Dashboard que ilustra el análisis de telemetría del endpoint; no se atribuye a WFP ni a Sysmon EID 3. |
| [wfp-eventchannel-attack-lab.png](screenshots/wfp-eventchannel-attack-lab.png) | WFP / raw EventChannel | Evento WFP decodificado de ATTACK/LAB, con origen `192.168.56.1`, destino `192.168.56.20` y TCP. Demuestra la telemetría que alimenta la detección. |
| [wfp-blocked-connections-attack-lab.png](screenshots/wfp-blocked-connections-attack-lab.png) | WFP / network evidence | Registros de conexiones TCP bloqueadas desde Kali ATTACK/LAB hacia el endpoint Windows. Complementa la evidencia WFP publicada. |
| [windows-sysmon-installation.png](screenshots/windows-sysmon-installation.png) | Sysmon / endpoint | Instalación correcta de Sysmon en Windows. Es evidencia de preparación del endpoint, no una validación de la detección Sysmon Event ID 3. |

La detección WFP Port Scan está **VALIDATED** por eventos reales, `archives.json` y `alerts.json`; las capturas WFP son apoyo visual. Sus reglas `100500`, `100501` y `100502` son una detección heurística de alta señal, no un conteo exacto de puertos únicos. Sysmon Event ID 3 permanece **AUDITED / PENDING VALIDATION**: todavía no existe una evidencia publicada de un EID 3 ATTACK real `192.168.56.1 -> 192.168.56.20` que valide ese escenario.

## Decisión de publicación

- **PUBLISH_AS_IS:** las ocho imágenes de la tabla recibieron revisión visual real y no requerían edición.
- **SANITIZE_AND_PUBLISH:** ninguna. No se alteraron originales ni se generaron recortes que pudieran cambiar su significado técnico.
- **DO_NOT_PUBLISH:** 49 de las 57 capturas históricas permanecen fuera del repositorio por mostrar pantallas de inicio o restablecimiento de sesión, prompts de contraseña, rutas o nombres personales, marcadores del navegador, direcciones públicas, comandos no necesarios o evidencia de bajo valor documental.
- **VISUAL_REVIEW_PENDING:** ninguna de las imágenes publicadas.

La revisión de las ocho copias no encontró contraseñas, tokens, claves privadas, cookies, códigos de autenticación ni pantallas de login. No se suben logs completos de producción, transcripciones ni material histórico sin una finalidad pública y una revisión individual.

## Evidencia de escenarios

| Ruta | Tipo | Estado de publicación |
|---|---|---|
| `scenario-1-bruteforce/` | Marcador histórico de brute force | Solo README; no contiene prueba, log ni captura y no valida la detección. |
