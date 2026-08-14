# SOC HomeLab Architecture

## Design Objective

The SOC HomeLab separates management, controlled scenarios, and external connectivity. This separation makes it possible to interpret the source of telemetry before applying a detection.

## Virtualized Components

| Component | Function |
|---|---|
| Kali Linux | Management from MANAGEMENT and controlled-scenario execution from ATTACK/LAB. |
| Ubuntu / Wazuh Manager 4.14.7 | Event reception, analysis, correlation, local file storage, and forwarding to the visualization pipeline. |
| Windows 11 endpoint | Monitored endpoint with Wazuh Agent, Windows Security EventChannel, and Sysmon. |
| VirtualBox | SOC HomeLab virtualization platform and adapter segmentation. |

## Network Planes

| Plane | CIDR | Addresses | Permitted Use |
|---|---|---|---|
| Management Network | `192.168.57.0/24` | Kali `.1`, Ubuntu `.10`, Windows `.20` | SSH, SCP/SFTP, WinRM, maintenance, and file transfer. |
| Attack/Lab Network | `192.168.56.0/24` | Kali `.1`, Ubuntu `.10`, Windows `.20` | Reconnaissance and controlled tests against the SOC HomeLab endpoint. |
| NAT/Internet Network | `10.0.2.0/24` | Ubuntu `.3`, Windows `.15` | Updates, repositories, and normal external connections. |

The MANAGEMENT Network does not participate in the WFP port-scan detector. NAT retains telemetry but also does not participate. Only ATTACK/LAB is eligible for that use case.

## Network-Plane False-Positive Control

```text
MANAGEMENT 192.168.57.0/24 ──> telemetry retained ──> excluded from the WFP detector
ATTACK/LAB 192.168.56.0/24 ──> eligible telemetry ──> base 100500 → 100501 / 100502
NAT 10.0.2.0/24 ────────────> telemetry retained ──> excluded from the WFP detector
```

This is a scope control for the WFP case, not a rule to delete or ignore telemetry. MANAGEMENT and NAT remain available in investigation sources; the exclusion limits which events can feed base rule `100500`.

## Telemetry Flow

```text
Windows 11
  ├─ Windows Security: WFP 5152/5157
  ├─ Sysmon Operational: Event ID 3 and other sources
  └─ Wazuh Agent
          |
          v
Ubuntu / Wazuh Manager
  ├─ archives.json: ingestion evidence
  ├─ ruleset: classification and correlation
  └─ alerts.json: created alerts
          |
          v
Filebeat -> Wazuh Indexer -> Wazuh Dashboard
```

The status of Filebeat or the Indexer service does not replace an authenticated query to the index or a visible Dashboard search.

## Security Decisions

- Management activity is legitimate telemetry, not attack activity by default.
- NAT telemetry is retained for investigation rather than globally silenced.
- Detection rules are validated first against the real Windows EventChannel event, not only with `wazuh-logtest`.
- Public artifacts contain procedures and sanitized evidence, never private keys or secrets.
