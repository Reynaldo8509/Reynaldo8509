# Setup y reproducibilidad

Esta sección separa los componentes reproducibles de las configuraciones que requieren reconstrucción o una exportación sanitizada. No sustituye las validaciones en el entorno real.

| Documento | Cobertura | Estado |
|---|---|---|
| [01 VirtualBox](01-virtualbox.md) | Máquinas y planos de red | Documentado a nivel de arquitectura |
| [02 Ubuntu/Wazuh](02-ubuntu-wazuh.md) | Manager y límites de publicación | Parcialmente documentado |
| [03 Windows Agent](03-windows-agent.md) | Endpoint y EventChannel | Parcialmente documentado |
| [04 Sysmon](04-sysmon.md) | Telemetría EID 3 | Auditado; pendiente validar ATTACK |
| [05 YARA](05-yara.md) | Estado de configuración | Pendiente de validación |
| [06 Networking](06-networking.md) | Segmentación | Documentado y parcialmente evidenciado |
| [07 SSH Management](07-ssh-management.md) | Administración segura | Documentado sin material privado |
| [08 Historical command reference](08-command-reference.md) | Comandos realmente evidenciados y brechas históricas | Evidencia parcial; no es guía genérica |

## Cómo usar esta sección

- Los documentos `01`–`07` explican la arquitectura, instalación/roles y decisiones de diseño sin publicar configuraciones sensibles.
- `08 Historical command reference` reúne comandos cuya ejecución aparece en evidencia revisada o en el registro de validación. También enumera herramientas útiles sin un comando histórico recuperado, sin presentarlas como usadas.
- La instalación histórica completa no se presenta como reproducible todavía porque las transcripciones originales no fueron publicadas en bruto.

Las configuraciones activas, certificados, claves y copias de producción no se incluyen hasta contar con una versión sanitizada y revisada.
