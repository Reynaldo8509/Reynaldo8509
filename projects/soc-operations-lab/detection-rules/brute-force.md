# Windows Brute Force

> **Status: PENDING CONTROLLED VALIDATION**

## Available Signals

- Windows Security `4625` records authentication failures.
- Official rule `60122` provides visibility into individual failures.
- The SOC HomeLab history includes custom correlation for repeated patterns, but some OpenSSH events left `win.eventdata.ipAddress` as `-`.
- The `OpenSSH/Operational` channel retained the IP in the payload, but automatic extraction into a correlatable field was not validated as the final solution.
- A sanitized export contains five historical `4625` events: three NTLM failures from `192.168.56.1` and two local failures from `127.0.0.1`, all with individual rule `60122`. This is telemetry evidence, not brute-force correlation evidence.

## Implication

The SOC HomeLab must not yet claim a validated IP-based brute-force detection for OpenSSH. Failure telemetry exists; correlation depends on a reliable source field for the authentication type being assessed.

## Next Required Validation

1. Select an authorized failed-authentication scenario.
2. Confirm the real fields in `archives.json` for Security and OpenSSH/Operational.
3. Verify the final rule in `alerts.json`.
4. Record a negative test and the known limitations.

This document does not include active rules until a reviewed export and reproducible evidence are available.

The available export is in [evidence/scenario-1-bruteforce](../evidence/scenario-1-bruteforce/events-2026-08-08T18_46_56.179Z.csv). Its `rule.mitre.id` field reflects the historical Wazuh rule and must not be reinterpreted as the final use-case mapping; the intended detection maps to [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/) once validated correlation exists.
