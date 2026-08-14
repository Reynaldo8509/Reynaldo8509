# Detection Engineering Index

This directory contains the HomeLab detection use cases and their current validation state.

| Use case | Telemetry | Main artifact | Status | MITRE |
|---|---|---|---|---|
| WFP Port Scan | Windows Security 5152/5157 | [WFP Port Scan](WFP_PortScan_Detection_Final.md) | **VALIDATED** | T1046 |
| Sysmon Network | Sysmon Event ID 3 | [Sysmon Network](sysmon-network.md) | **AUDITED / PENDING VALIDATION** | T1046 / context-dependent |
| Windows Brute Force | Windows Security 4625 | [Brute Force](brute-force.md) | **PENDING CONTROLLED VALIDATION** | T1110 |
| File Integrity | Wazuh syscheck/FIM | [FIM](fim.md) | **CONFIGURED / REVALIDATION PENDING** | Context-dependent |
| Malware/YARA | YARA scan results | [YARA](yara.md) | **PENDING VALIDATION** | Context-dependent |

## Detection workflow

```text
Telemetry
   -> Decoder / EventChannel path
   -> Base tracking rule
   -> Correlation / threshold
   -> Alert
   -> Evidence validation
   -> False-positive review
   -> Documentation
```

## Engineering standard

A detection is not considered validated merely because `wazuh-logtest` matches a rule. The project prioritizes production EventChannel evidence, negative tests for known legitimate traffic, reproducibility and explicit documentation of engine limitations.

See the [SOC HomeLab README](../README.md) for the lab-wide validation model.
