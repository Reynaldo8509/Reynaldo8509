# 06 — Networking

| Network | CIDR | Kali | Ubuntu/Wazuh | Windows | Purpose |
|---|---|---:|---:|---:|---|
| MANAGEMENT | `192.168.57.0/24` | `192.168.57.1` | `192.168.57.10` | `192.168.57.20` | Management and transfers. |
| ATTACK/LAB | `192.168.56.0/24` | `192.168.56.1` | `192.168.56.10` | `192.168.56.20` | Simulations and detection validation. |
| NAT/INTERNET | `10.0.2.0/24` | — | `10.0.2.3` | `10.0.2.15` | Updates and external services. |

## Evidence Scope

The table describes the documented final operating design. The reviewed screenshots show ATTACK/LAB and NAT addresses on the endpoint and a point-in-time connectivity test, but do not recover adapter-creation commands, routes, or a final screenshot of all three planes at once. Therefore, segmentation is **documented and partially evidenced**, not a reproducible step-by-step VirtualBox procedure.

### Operating Rule

Attack-detection tests are limited to ATTACK/LAB. MANAGEMENT and NAT must retain telemetry; they are not eligible sources for the WFP port-scan detector.

See the confirmed commands and historical gaps in the [command reference](08-command-reference.md).
