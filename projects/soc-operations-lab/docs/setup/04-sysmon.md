# 04 — Sysmon

Sysmon is present on the endpoint, and Event ID 3 telemetry was observed for MANAGEMENT and NAT connections. The official Wazuh path is:

```text
60000 -> 60004 -> 61600 -> 61605 -> sysmon_event3
```

Sysmon network configuration is enabled, but the reviewed archives do not contain an ATTACK EID 3 sample `192.168.56.1 -> 192.168.56.20`. Therefore, the Sysmon Network detector is not considered validated. See [sysmon-network.md](../../detection-rules/sysmon-network.md).

Active Sysmon XML is not published until a sanitized, reviewed, reproducible version is available.
