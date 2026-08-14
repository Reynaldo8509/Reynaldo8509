# Project context

This repository documents a SOC HomeLab with evidence-based detection engineering.

- WFP Port Scan is **VALIDATED** as a high-signal heuristic, not exact distinct-port counting.
- Sysmon Event ID 3 network detection is **AUDITED / PENDING VALIDATION**.
- MANAGEMENT and NAT telemetry must be retained and must not feed the WFP port-scan detector.
- Do not publish secrets, private keys, raw internal transcripts, active configuration backups or unsanitized captures.
- Any future rule change needs backup, syntax validation, production evidence and negative-path validation.
