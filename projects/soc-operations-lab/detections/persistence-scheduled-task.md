# Detection: Scheduled task persistence simulation

## Summary

A controlled, one-time Windows scheduled task with a harmless `cmd.exe /c exit
0` action was created on `WIN11-ENDPOINT` and then removed after evidence
capture. Windows Security recorded Event ID 4698 and Wazuh alerted on the task
creation.

## MITRE ATT&CK

- **T1053 – Scheduled Task/Job.** Wazuh mapped the alert to Execution,
  Persistence, and Privilege Escalation tactics.

## Evidence

- **Windows Security:** Event ID **4698**, record `696932`, task
  `\SOC-HOMELAB-PERSISTENCE-20260816T234835Z`, created by `endpointuser`.
- **Wazuh:** rule **60228**, level **4**, `A scheduled task was created`, at
  `2026-08-16T23:48:37.280+0000`; its MITRE mapping is T1053.
- **Cleanup:** the exact task was deleted and verification returned
  `TaskExists: false` and `FilesRemaining: []`.
- **Artifacts:**
  [`security-scheduled-task-events.jsonl`](../evidence/scenario-5-scheduled-task-20260816T234835Z/security-scheduled-task-events.jsonl),
  [`wazuh-scheduled-task-alerts-sanitized.jsonl`](../evidence/scenario-5-scheduled-task-20260816T234835Z/wazuh-scheduled-task-alerts-sanitized.jsonl),
  and
  [`cleanup-verification.json`](../evidence/scenario-5-scheduled-task-20260816T234835Z/cleanup-verification.json).

## Timeline

| UTC time | Event | Result |
|---|---|---|
| 2026-08-16 23:48:35 | Task created | A uniquely named, one-time harmless task was registered. |
| 2026-08-16 23:48:36.348 | Security Event ID 4698 | Task creation audited on the endpoint. |
| 2026-08-16 23:48:37.280 | Wazuh rule 60228 | Scheduled-task creation alert generated. |
| 2026-08-16 23:49 | Cleanup | Task and exercise files were removed; state verified. |

## Analysis

Task creation is a common persistence mechanism because it can survive user
logoff and execute at configured times or triggers. The built-in Wazuh rule
provides useful baseline visibility, but its level reflects that task creation
can be legitimate. Context determines severity: task path, author, action,
trigger, account, and relationship to recently created scripts are decisive.

## Risk Level

**Medium** by itself; **High** when a new or unusual task launches a script
from a user-writable directory. This event was authorized and fully cleaned up.

## Recommendations

1. Review task XML, executable path, arguments, account, triggers, and author.
2. Compare task names and actions against a baseline of sanctioned software.
3. Raise priority when Event ID 4698 follows a suspicious EID 11 file creation
   or encoded PowerShell event on the same endpoint.
4. Keep Security auditing for scheduled task creation enabled and forward it
   through the Wazuh agent.
