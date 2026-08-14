# Setup and Reproducibility

This section separates reproducible components from configurations that require reconstruction or a sanitized export. It does not replace validation in the real environment.

| Document | Coverage | Status |
|---|---|---|
| [01 VirtualBox](01-virtualbox.md) | Machines and network planes | Documented at the architecture level |
| [02 Ubuntu/Wazuh](02-ubuntu-wazuh.md) | Manager and publication boundaries | Partially documented |
| [03 Windows Agent](03-windows-agent.md) | Endpoint and EventChannel | Partially documented |
| [04 Sysmon](04-sysmon.md) | EID 3 telemetry | Audited; ATTACK validation pending |
| [05 YARA](05-yara.md) | Configuration status | Pending validation |
| [06 Networking](06-networking.md) | Segmentation | Documented and partially evidenced |
| [07 SSH Management](07-ssh-management.md) | Secure management | Documented without private material |
| [08 Historical command reference](08-command-reference.md) | Commands with real evidence and historical gaps | Partial evidence; not a generic guide |

## How to Use This Section

- Documents `01`–`07` explain the architecture, installation/roles, and design decisions without publishing sensitive configurations.
- `08 Historical command reference` gathers commands whose execution appears in reviewed evidence or the validation record. It also lists useful tools without a recovered historical command, without presenting them as used.
- The complete historical installation is not yet presented as reproducible because the original transcripts were not published verbatim.

Active configurations, certificates, keys, and environment copies are not included until a sanitized, reviewed version is available.
