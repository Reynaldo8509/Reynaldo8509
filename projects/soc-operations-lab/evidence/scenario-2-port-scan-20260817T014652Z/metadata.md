# Controlled TCP Connect enrichment validation

| Field | Value |
| --- | --- |
| Source | `192.168.56.1` (ATTACK/LAB) |
| Target | `192.168.56.20` (Windows endpoint) |
| Scan type | TCP Connect, ports 1–100 |
| Result | 22/TCP open; 99 ports filtered |
| WFP evidence | Event ID 5152 produced the Wazuh correlation alerts |
| Sysmon enrichment | Event ID 3 recorded two completed inbound TCP connections to 22/TCP (`initiated:false`) |
| UTC event window | 2026-08-17 01:46:52–01:46:56 |

This authorized ATTACK/LAB run is sanitized. It contains no credentials,
private keys, or full raw event records.
