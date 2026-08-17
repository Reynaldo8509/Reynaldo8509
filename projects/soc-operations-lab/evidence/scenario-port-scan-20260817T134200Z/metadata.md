# Controlled TCP Connect port-scan validation

| Field | Value |
| --- | --- |
| Source | `192.168.56.1` (ATTACK/LAB) |
| Target | `192.168.56.20` (Windows endpoint) |
| Profile | TCP Connect scan of ports 1–100 at T3 |
| Scan outcome | 22/TCP open; 99 selected ports filtered |
| WFP correlation | `100501` at 13:42:34.631 UTC; `100502` at 13:42:35.494 UTC |
| Sysmon enrichment | EID 3 for the completed inbound 22/TCP connection at 13:42:38.544 UTC |
| Scope | Authorized ATTACK/LAB exercise; no Management or NAT telemetry included |

## Detection summary

WFP Security events for blocked connections remain the authoritative source for
the port-scan correlation. Sysmon EID 3 supplied context for the successful
TCP Connect to the open SSH service, but did not represent the filtered ports.
The exported JSONL records contain only the fields necessary for analysis.
