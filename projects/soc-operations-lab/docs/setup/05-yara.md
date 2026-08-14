# 05 — YARA

## Status

**PENDING VALIDATION**.

Historical material mentions YARA work and malware detection, but this repository does not contain a rule, deployment configuration, and sanitized evidence that support an end-to-end workflow claim.

Before publishing a YARA implementation, the following must exist at minimum:

1. A YARA rule that is safe to share and its license/provenance.
2. A documented Wazuh execution and collection method.
3. An event sample in `archives.json` and its corresponding alert in `alerts.json`.
4. A negative test and update strategy.
