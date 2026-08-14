# Operación: flujo de validación

## Principio de evidencia

| Capa | Qué demuestra | Qué no demuestra |
|---|---|---|
| `archives.json` | El manager ingirió y decodificó el evento. | Que una regla creó alerta o que Dashboard la muestra. |
| `alerts.json` | Una regla creó una alerta visible. | Que Indexer y Dashboard la recibieron. |
| Filebeat / Indexer | Salud del pipeline de indexación. | Que una consulta o panel concreto muestra el documento. |
| Consulta autenticada / Dashboard | Indexación y visualización real. | La calidad o la semántica de la detección. |

## Flujo de cambios de reglas

1. Respaldar el archivo afectado y registrar hash cuando corresponda.
2. Validar XML mediante wrapper si el ruleset es un fragmento de varios grupos.
3. Ejecutar `wazuh-analysisd -t` y tratar warnings nuevos como fallos a investigar.
4. Reiniciar solo el servicio autorizado.
5. Probar con telemetría real del ámbito autorizado.
6. Validar ruta positiva y negativas de MANAGEMENT/NAT.
7. Revisar `archives.json`, `alerts.json` y, si hay acceso, el índice/Dashboard.

## Uso de wazuh-logtest

`wazuh-logtest` es útil para validar sintaxis y conceptos de correlación. No sustituye el evento de producción: un JSON pegado manualmente puede seguir el decoder `json` y no la ruta `windows_eventchannel` real.
