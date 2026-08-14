# Detection engineering index

This index separates a documented use case from a validated detector. A rule is not marked **VALIDATED** merely because a configuration or screenshot exists: the required boundary is real telemetry, the effective rule path, an alert result and the relevant negative control.

| Use case | Telemetry source | Rule IDs / detection logic | Threshold and false-positive controls | MITRE ATT&CK | Current status | Evidence |
|---|---|---|---|---|---|---|
| [WFP Port Scan](WFP_PortScan_Detection_Final.md) | Windows Security EventChannel `5152`/`5157`, inbound TCP | `100500` base; `100501` / `100502` correlations. Scope is `192.168.56.0/24` to `192.168.56.20`. | `100501`: `frequency=10`, `timeframe=60`, `ignore=60`; `100502`: `frequency=14`, `timeframe=60`, `ignore=60`. MANAGEMENT and NAT are retained but excluded. | [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/) | **VALIDATED — documented controlled run** | 34 WFP events / 15 raw ports; documented `archives.json` and `alerts.json` results; negative controls. Raw production logs are not public. |
| [Sysmon Network / Event ID 3](sysmon-network.md) | Sysmon Operational EID `3` through Windows EventChannel | Audited `100409` base; `100420` / `100421` correlations for ATTACK/LAB TCP to the endpoint. | `frequency=10` / `15`, `timeframe=60`; no `ignore`; MANAGEMENT and NAT do not enter the base. | [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/) (intended use case) | **AUDITED / PENDING VALIDATION** | EID 3 seen in MANAGEMENT and NAT; required ATTACK/LAB source event is absent. |
| [Windows authentication / brute force](brute-force.md) | Windows Security `4625`; OpenSSH/Operational reviewed | Official `60122` records individual failures. No public custom correlation is asserted. | A correlation must first prove a usable source-IP field and include a controlled negative path. | [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/) (use-case mapping, not a validated rule mapping) | **TELEMETRY OBSERVED / PENDING DETECTION VALIDATION** | Sanitized 4625 export includes ATTACK/LAB NTLM failures, but no validated correlation or negative control. |
| [File Integrity Monitoring](fim.md) | Wazuh syscheck/FIM | No public rule ID or active configuration. | Historical noise reduction was narrow; its scope needs revalidation. | Not assigned: a generic file-change signal needs a concrete behavior before mapping. | **CONFIGURED / REVALIDATION PENDING** | No sanitized change-to-alert evidence package. |
| [YARA](yara.md) | Intended Wazuh/YARA collection path | No public rule, rule ID or execution configuration. | Not yet established. | Not assigned: no rule or scenario is public. | **PENDING VALIDATION** | No end-to-end event, alert or negative test. |

## Reading a rule page

- **Telemetry source** says what was observed, not what was detected.
- **Rule IDs** are published only when their live use is documented; active configuration files remain private until independently sanitized.
- **Thresholds** are Wazuh correlation behavior, not automatically counts of unique values.
- **Status** is evidence-scoped. For WFP, `100501` and `100502` are high-signal heuristics, never `COUNT(DISTINCT destinationPort)` claims.

For the evidence boundary behind every status, see the [evidence matrix](../evidence/evidence-matrix.md).
