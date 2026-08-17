# Controlled PowerShell and persistence validation

## Scope

- **Target:** `WIN11-ENDPOINT` (`192.168.56.20`).
- **Operator:** authorized HomeLab administrative session; an operator source IP
  is not treated as an endpoint IOC for this host-local process activity.
- **Safety:** benign commands only; no download, credential access, destructive
  action, or task execution occurred. The file and task were removed after
  collection.

## Timeline (UTC)

| Time | Activity | Evidence |
| --- | --- | --- |
| 13:28:57.108 | Encoded PowerShell executed | Sysmon EID 1; Wazuh `92057`, level 12. |
| 13:28:57.324 | `Get-Process | Out-Null` executed | Sysmon EID 1; Wazuh `92027`. |
| 13:28:57.580 | Test script written to Temp | Sysmon EID 11; Wazuh `92213`, level 15. |
| 13:29:20.953 | `UpdaterTask` created | Endpoint task creation confirmation. |
| 13:29:22.101 | Task creation ingested | Windows Security EID 4698; Wazuh `60228`. |
| 13:32:27.648 | File and task removed | `cleanup-verification.json` confirms neither remains. |

## Detection summary

The full behavioral chain was visible in Wazuh using existing Sysmon and
Windows Security rules. PowerShell Script Block Logging (EID 4104) was not
observed in this run; that is documented as a telemetry gap, not silently
filled with a new rule.
