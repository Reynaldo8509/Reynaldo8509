# Detection: Encoded PowerShell execution

## Summary

An administrator-led lab exercise executed a benign `IEX` payload through
`powershell.exe -EncodedCommand` on `WIN11-ENDPOINT`. The command returned its
unique exercise marker, confirming execution. No destructive command, download,
or credential access was used.

## MITRE ATT&CK

- **T1059.001 – Command and Scripting Interpreter: PowerShell.**

## Evidence

- **Endpoint:** `WIN11-ENDPOINT` (`192.168.56.20`), user `endpointuser`.
- **Execution proof:** `command-output.txt` contains the unique marker
  `SOC-HOMELAB-PS-20260816T234426Z`.
- **Agent health:** `WazuhSvc` was running and configured to start
  automatically.
- **Telemetry gap observed:** Sysmon Operational and PowerShell Operational
  logs were enabled, but this exercise yielded neither Sysmon Event ID 1 nor
  PowerShell Event ID 4104. The Security Event ID 4688 query also returned no
  matching process-creation record. Therefore, no Wazuh rule or alert is
  claimed for this execution.
- **Artifacts:**
  [`metadata.txt`](../evidence/scenario-3-powershell-20260816T234426Z/metadata.txt),
  [`command-output.txt`](../evidence/scenario-3-powershell-20260816T234426Z/command-output.txt),
  and [`wazuh-agent-status.json`](../evidence/scenario-3-powershell-20260816T234426Z/wazuh-agent-status.json).

## Timeline

| UTC time | Event | Evidence |
|---|---|---|
| 2026-08-16 23:44:26 | Benign encoded PowerShell with `IEX` executed | Endpoint returned the scenario marker. |
| 2026-08-16 23:44–23:46 | Endpoint telemetry queried | Sysmon EID 1, PowerShell 4104, and Security 4688 yielded no matching event. |
| 2026-08-16 23:47 | Detection gap recorded | No Wazuh validation asserted because the needed source telemetry was absent. |

## Analysis

Encoded PowerShell combined with `IEX` is a high-value behavioral signal in a
production environment because it can conceal script content and dynamically
execute it. Here it was deliberately benign and carried a unique marker.

The important defensive finding is not a failed Wazuh rule: it is the absence
of the event sources a rule would need. Creating an active Wazuh correlation
rule now would be misleading because the manager cannot match telemetry that
the endpoint does not emit. A candidate rule is included in
[`configs/wazuh-rules-custom.xml`](../configs/wazuh-rules-custom.xml), but it
must remain uninstalled until Sysmon process creation and PowerShell script
block logging are enabled and tested.

## Risk Level

**High** in production when unapproved or correlated with file writes,
persistence, credential access, or external network activity. **Authorized
and benign** for this isolated lab exercise.

## Recommendations

1. Enable Sysmon Event ID 1 for `powershell.exe`, `pwsh.exe`, and their command
   lines; collect it through the Wazuh agent.
2. Enable PowerShell Script Block Logging (Event ID 4104) and protect the log
   channel from clearing or tampering.
3. Validate the candidate Wazuh rule against a benign marker before enabling
   it in the active ruleset.
4. Correlate an encoded PowerShell process event with nearby file creation and
   scheduled-task creation only when process, user, host, and time fields
   support that relationship.
