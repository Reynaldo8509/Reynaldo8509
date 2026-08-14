# Setup y reproducibilidad

Esta sección separa los componentes reproducibles de las configuraciones que requieren reconstrucción o una exportación sanitizada. No sustituye las validaciones en el entorno real.

| Documento | Cobertura | Estado |
|---|---|---|
| [01 VirtualBox](01-virtualbox.md) | Máquinas y planos de red | Documentado a nivel de arquitectura |
| [02 Ubuntu/Wazuh](02-ubuntu-wazuh.md) | Manager y límites de publicación | Parcialmente documentado |
| [03 Windows Agent](03-windows-agent.md) | Endpoint y EventChannel | Parcialmente documentado |
| [04 Sysmon](04-sysmon.md) | Telemetría EID 3 | Auditado; pendiente validar ATTACK |
| [05 YARA](05-yara.md) | Estado de configuración | Pendiente de validación |
| [06 Networking](06-networking.md) | Segmentación | Validado por arquitectura |
| [07 SSH Management](07-ssh-management.md) | Administración segura | Documentado sin material privado |
| [08 Command Reference](08-command-reference.md) | Comandos operativos, validación y reproducción | **Documentado con evidencia pública** |

## Cómo usar esta sección

- Los documentos `01`–`07` explican la arquitectura, instalación/roles y decisiones de diseño sin publicar configuraciones sensibles.
- `08 Command Reference` reúne comandos que sí están respaldados por la evidencia pública actual: verificación de interfaces, conectividad, Sysmon, reglas Wazuh, `xmllint`, `wazuh-analysisd`, `jq` y la prueba Nmap validada.
- La instalación histórica completa no se presenta como reproducible todavía porque las transcripciones originales no fueron publicadas en bruto.

Las configuraciones activas, certificados, claves y copias de producción no se incluyen hasta contar con una versión sanitizada y revisada.
