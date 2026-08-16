# SOC incident report: controlled multi-stage endpoint exercise

## Case metadata

| Field | Value |
|---|---|
| Classification | Authorized SOC HomeLab exercise |
| Investigation window | 2026-08-16 23:42–23:49 UTC |
| Affected system | `WIN11-ENDPOINT` (`192.168.56.20`) |
| Source | `192.168.56.1` on ATTACK/LAB |
| Analyst disposition | Closed — test artifacts removed and state verified |

## Attack description

The exercise simulated reconnaissance, encoded PowerShell execution, creation
of files in user-writable locations, and scheduled-task persistence. Each
payload was intentionally harmless. The objective was to verify endpoint
telemetry, Wazuh alerting, and the quality of a Tier 1 analyst investigation.

## Indicators of compromise / exercise indicators

| Indicator | Type | Context |
|---|---|---|
| `192.168.56.1` | Source IP | Authorized ATTACK/LAB host. |
| `SOC-HOMELAB-PS-20260816T234426Z` | Execution marker | Benign encoded PowerShell output. |
| `SOC-HOMELAB-FILE-20260816T234739Z.ps1` | File marker | Created under `%USERPROFILE%\AppData\Local\Temp`, then removed. |
| `SOC-HOMELAB-PERSISTENCE-20260816T234835Z` | Task marker | One-time task, then removed. |

## Timeline

| UTC time | Activity | Windows / Sysmon evidence | Wazuh evidence |
|---|---|---|---|
| 23:42:38–23:42:43 | 15-port TCP SYN scan | Windows Security 5152 expected and observed at manager | `100501` at 23:42:43.831; `100502` at 23:42:43.928 |
| 23:44:26 | Encoded PowerShell with benign `IEX` | Marker output confirmed execution | No alert: EID 1, 4104, and 4688 source records absent |
| 23:47:40.291 | Temp script and Desktop text file created | Sysmon EID 11 × 2, `powershell.exe` | `92213`, level 15, for Temp `.ps1` |
| 23:48:36.348 | One-time scheduled task created | Security EID 4698 | `60228`, level 4, T1053 |
| 23:49 | Cleanup | Task absent; test file list empty | Exercise closed |

## Analysis and correlation

The sequence resembles a common intrusion story: reconnaissance precedes host
activity; a script appears in a user-writable directory; persistence is then
established with a scheduled task. The file and task alerts are independently
confirmed by endpoint and manager evidence.

However, the encoded-PowerShell portion lacks the necessary EID 1/4104/4688
record. It is therefore a **logical exercise sequence**, not a forensically
proven PowerShell-to-file-to-task process chain. A Tier 1 analyst should report
both the correlation and its evidentiary limit.

## Analyst conclusion

The lab validated three Wazuh detection paths: WFP scan correlation, suspicious
script creation in Temp, and scheduled-task creation. The principal detection
engineering gap is process/script telemetry for PowerShell. No indicators remain
on the endpoint from this exercise.

## Recommended response actions

1. In a non-lab incident, contain the endpoint when unapproved encoded
   PowerShell, a Temp script, and a new scheduled task occur together.
2. Acquire task XML, file hashes, parent/child process data, and network
   connections before removal when incident handling permits.
3. Enable Sysmon Process Create and PowerShell Script Block logging, then
   validate the documented candidate rule with a benign marker.
4. Keep the WFP detector's ATTACK/LAB scope and treat its thresholds as a
   high-signal heuristic rather than exact unique-port cardinality.
