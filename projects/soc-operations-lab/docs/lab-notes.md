# Lab notes: controlled detection exercises — 2026-08-16

## Scope and safety

All activity occurred in the isolated ATTACK/LAB and Windows endpoint described
in the architecture. No exploit, payload download, credential harvesting, or
destructive action was used. Files and the scheduled task created by the
exercise were removed after collection, with state verification retained as
evidence.

## Observed detection outcomes

| Scenario | Endpoint telemetry | Wazuh validation | Status |
|---|---|---|---|
| TCP SYN scan of 15 selected ports | Windows Security 5152 | `100501` and `100502`, each once | Validated |
| Encoded PowerShell + benign IEX | Command output; agent service health | No EID 1, 4104, or 4688 source event | Telemetry gap documented |
| Temp `.ps1` + Desktop `.txt` creation | Sysmon EID 11 × 2 | `92213`, level 15, for Temp `.ps1` | Validated |
| One-time scheduled task | Security EID 4698 | `60228`, level 4, MITRE T1053 | Validated and cleaned up |

## Analyst note

The event sequence can be used as a controlled investigation timeline, but it
does **not** prove a process-parent chain from encoded PowerShell to the files
or task because Sysmon Process Create and PowerShell Script Block telemetry were
not present. That distinction prevents an analyst from escalating a plausible
story as a confirmed causal chain.
