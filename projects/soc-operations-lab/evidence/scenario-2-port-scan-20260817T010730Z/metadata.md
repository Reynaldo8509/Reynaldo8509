# Controlled WFP port-scan validation

| Field | Value |
| --- | --- |
| Scenario | Controlled TCP SYN port-scan validation |
| UTC alert window | 2026-08-17 01:07:30 UTC |
| Source | `192.168.56.1` (ATTACK/LAB) |
| Target | `192.168.56.20` (Windows endpoint) |
| Scope | Ten-plus filtered TCP ports, endpoint only |
| Telemetry source | Windows Security / Windows Filtering Platform (Event ID 5152) |
| Wazuh result | `100501` at the 10th distinct blocked port; `100502` at the 15th |
| Manager validation | `wazuh-manager` active; `wazuh-analysisd -t` passed before the test |

The scan was authorized and confined to the ATTACK/LAB network. No credentials,
private keys, full raw event logs, or Management/NAT telemetry are included.
