# Detection: Suspicious file creation in user-writable paths

## Summary

A controlled PowerShell action created a benign `.ps1` file in the endpoint's
`%USERPROFILE%\AppData\Local\Temp` directory and a benign text file on the
Desktop. Sysmon recorded both file creations as Event ID 11. Wazuh alerted on
the executable script dropped in Temp.

## MITRE ATT&CK

- **T1204.002 – User Execution: Malicious File** (behavioral context only; the
  lab file was benign).
- **T1059.001 – PowerShell** (the observed creating process).

## Evidence

- **Sysmon:** two Event ID **11** records at `2026-08-16 23:47:40.291` UTC;
  creating image `powershell.exe`, user `WIN11-ENDPOINT\endpointuser`.
- **Wazuh:** rule **92213**, level **15**, `Executable file dropped in folder
  commonly used by malware`, at `2026-08-16T23:47:41.531+0000`.
- **Alerted path:** `%USERPROFILE%\AppData\Local\Temp\SOC-HOMELAB-FILE-20260816T234739Z.ps1`.
- **Artifacts:**
  [`sysmon-file-create-events.jsonl`](../evidence/scenario-4-file-activity-20260816T234739Z/sysmon-file-create-events.jsonl)
  and
  [`wazuh-file-create-alerts-sanitized.jsonl`](../evidence/scenario-4-file-activity-20260816T234739Z/wazuh-file-create-alerts-sanitized.jsonl).

## Timeline

| UTC time | Event | Result |
|---|---|---|
| 2026-08-16 23:47:39 | Controlled file activity started | Paths resolved from `%USERPROFILE%`; no profile path was hardcoded. |
| 2026-08-16 23:47:40.291 | Sysmon Event ID 11 × 2 | Temp `.ps1` and Desktop `.txt` were created by PowerShell. |
| 2026-08-16 23:47:41.531 | Wazuh rule 92213 | Level-15 alert for the Temp PowerShell script. |
| 2026-08-16 23:49 | Cleanup verified | Both test files were removed after evidence collection. |

## Analysis

Scripts written to user-writable temporary folders are a strong triage signal:
they are easy to stage and are commonly used by malware loaders. The rule
correctly prioritized the `.ps1` in Temp. The Desktop text file created the
same Sysmon telemetry but did not independently meet the executable-in-suspicious-folder
logic, which is expected and reduces noise.

## Risk Level

**High** if the script is unapproved, unsigned, newly downloaded, or followed
by execution or persistence. **Authorized / benign** in this lab.

## Recommendations

1. Triage the file hash, signer, provenance, and parent process before
   containment.
2. Correlate EID 11 with EID 1 process creation when that telemetry is enabled.
3. Preserve the user-writable-path rule and tune exclusions only for documented
   sanctioned software.
4. Escalate when file creation is followed by scheduled-task creation on the
   same host and user within a narrow time window.
