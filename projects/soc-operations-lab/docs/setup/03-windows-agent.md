# 03 — Windows 11 and Wazuh Agent

## Endpoint Role

Windows 11 is the monitored endpoint. It sends Windows Security EventChannel and Sysmon telemetry to the manager through Wazuh Agent.

## Relevant Telemetry Sources

- Windows Security `5152`/`5157`: WFP signal used by the validated detector.
- Windows Security `4625`: authentication failures.
- Microsoft-Windows-Sysmon/Operational Event ID 3: Sysmon network connections.
- FIM/syscheck: file-integrity changes according to the active configuration.

The agent configuration and monitored paths are not published here because a sanitized, reviewed export is not yet available. Detection documentation must be based on fields that appear in `archives.json`, not only on expected configurations.
