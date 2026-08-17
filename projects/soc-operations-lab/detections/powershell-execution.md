# Detection: PowerShell execution with scheduled-task persistence

## Summary

An authorized HomeLab exercise on `WIN11-ENDPOINT` executed a benign encoded
PowerShell command, ran a benign process-discovery command, wrote `evil.ps1`
to the user's Temp directory, and created the `UpdaterTask` logon task. The
task and file were removed after evidence collection.

Wazuh observed all material stages through existing rules: encoded PowerShell,
PowerShell process execution, a script dropped in a user-writable directory,
and scheduled-task creation. No active Wazuh rules were changed.

## MITRE ATT&CK

- **T1059.001 – Command and Scripting Interpreter: PowerShell.**
- **T1053 – Scheduled Task/Job.**

## Evidence

- **Encoded PowerShell:** Sysmon Event ID **1** at
  `2026-08-17T13:28:57.108Z`; Wazuh rule **92057**, level **12**, identified a
  PowerShell process executing a base64-encoded command.
- **Process execution:** Sysmon Event ID **1** at
  `2026-08-17T13:28:57.324Z`; Wazuh rule **92027** recorded
  `Get-Process | Out-Null`.
- **File creation:** Sysmon Event ID **11** at
  `2026-08-17T13:28:57.580Z`; Wazuh rule **92213**, level **15**, recorded
  `%USERPROFILE%\AppData\Local\Temp\evil.ps1`.
- **Persistence:** Windows Security Event ID **4698** at
  `2026-08-17T13:29:22.101Z`; Wazuh rule **60228** recorded creation of
  `\UpdaterTask` with a PowerShell file action.
- **Sanitized artifacts:**
  [`metadata.md`](../evidence/scenario-powershell-persistence-20260817T132820Z/metadata.md),
  [`sysmon-events.jsonl`](../evidence/scenario-powershell-persistence-20260817T132820Z/sysmon-events.jsonl),
  [`security-events.jsonl`](../evidence/scenario-powershell-persistence-20260817T132820Z/security-events.jsonl),
  and [`wazuh-alerts.jsonl`](../evidence/scenario-powershell-persistence-20260817T132820Z/wazuh-alerts.jsonl).

## Timeline

| UTC time | Event | Correlation |
| --- | --- | --- |
| 13:28:57.108 | Encoded PowerShell starts | EID 1 → Wazuh 92057 / T1059.001. |
| 13:28:57.324 | Process-discovery command runs | EID 1 → Wazuh 92027. |
| 13:28:57.580 | Script is written to Temp | EID 11 → Wazuh 92213. |
| 13:29:20.953 | `UpdaterTask` created | Endpoint confirmation. |
| 13:29:22.101 | Scheduled-task event ingested | EID 4698 → Wazuh 60228 / T1053. |
| After collection | Artifacts removed | File and task cleanup verified. |

## Analysis

Individually, a PowerShell process, a Temp-file write, or a scheduled task can
be legitimate. Together and in a narrow time window, they form a credible
execution-to-persistence chain: encoded command execution is followed by a
script written to a user-writable location and a task configured to run it at
logon.

The exercise confirms that Wazuh can classify the chain using existing Sysmon
and Windows Security rules. PowerShell Script Block Logging Event ID 4104 was
not observed, so decoded script content is not claimed as a telemetry source.
This is a documented coverage gap; it does not invalidate the confirmed EID 1,
EID 11, and EID 4698 evidence.

## Risk Level

**High** in production: encoded PowerShell combined with a new script in Temp
and logon-triggered persistence warrants immediate triage. This instance was
authorized, benign, and cleaned up in the isolated lab.

## Recommendations

1. Triage high-severity EID 1 and EID 11 alerts by linking process, user,
   script path, parent process, and nearby task-creation events.
2. Review Event ID 4698 task action, trigger, account, and author; prioritize
   actions running scripts from user-writable folders.
3. Enable and validate PowerShell Script Block Logging (EID 4104) to retain
   decoded script content for investigation.
4. Baseline approved scheduled tasks and alert on newly created tasks that run
   PowerShell, especially from Temp or Downloads paths.
