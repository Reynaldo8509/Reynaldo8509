# 03 — Windows 11 y Wazuh Agent

## Rol del endpoint

Windows 11 es el endpoint monitorizado. Entrega Windows Security EventChannel y Sysmon al manager mediante Wazuh Agent.

## Fuentes de telemetría relevantes

- Windows Security `5152`/`5157`: señal WFP usada por el detector validado.
- Windows Security `4625`: fallos de autenticación.
- Microsoft-Windows-Sysmon/Operational Event ID 3: conexiones de red Sysmon.
- FIM/syscheck: cambios de integridad de archivos según la configuración activa.

La configuración del agente y las rutas monitorizadas no se publican aquí porque no existe todavía una exportación sanitizada y revisada. La documentación de detección debe basarse en campos que aparezcan en `archives.json`, no solo en configuraciones esperadas.
