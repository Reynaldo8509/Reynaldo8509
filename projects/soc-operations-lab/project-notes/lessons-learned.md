# Lessons learned

1. Separating MANAGEMENT from ATTACK/LAB reduces false positives without losing management telemetry.
2. NAT must be retained for investigation even when it is outside a specific detector.
3. `wazuh-logtest` and Windows EventChannel are not equivalent when the effective decoder changes.
4. `archives.json` proves ingestion; `alerts.json` proves alert creation; Dashboard requires independent verification.
5. Wazuh `frequency` and `different_field` rules do not implement `COUNT(DISTINCT)`.
6. Priority between sibling rules can prevent a custom base from receiving the real event.
7. Standard telemetry and the detection verdict are distinct concepts: `60104` is WFP audit telemetry, not a port-scan alert.
8. The absence of a Sysmon ATTACK signal must be treated as a validation gap, not as success or failure of the correlation.
9. Limitations and negative tests are part of a professional detection, not a secondary note.
