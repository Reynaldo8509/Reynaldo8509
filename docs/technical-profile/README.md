# Technical Profile

## IT, Systems and Networking

- Windows and Linux administration
- Server operations, DNS and DHCP
- Network administration, segmentation and firewall fundamentals
- Active Directory / AD DS, Group Policy and access-management fundamentals
- Troubleshooting, root-cause analysis and operational documentation

## Blue Team and SOC Development

- Wazuh Manager and Windows Agent telemetry
- Windows EventChannel, Windows Filtering Platform (WFP) and Sysmon
- Detection engineering, alert triage and evidence handling
- SIEM-oriented log analysis and incident-response fundamentals
- False-positive reduction through network-plane scoping and correlation tuning

## Detection Engineering Practices

- Custom Wazuh base and correlation rules
- Threshold and `timeframe` tuning
- Negative controls for MANAGEMENT and NAT traffic
- Evidence-backed validation with real HomeLab events
- Explicit separation of telemetry, alert creation, indexing and Dashboard visibility
- Documentation of engine limitations and known detection boundaries

## Automation and Tooling

- Kali Linux, PowerShell, Bash/Linux CLI and `jq`
- Python fundamentals and SQL basics
- Wireshark and Nmap for controlled network analysis
- Microsoft Entra ID, Azure Fundamentals and Microsoft Defender familiarity

## Evidence Standard

The associated [SOC Operations Lab](../../projects/soc-operations-lab/README.md) distinguishes **VALIDATED**, **OBSERVED**, and **PENDING** capabilities. A documented event, service state or screenshot is not treated as a validated detection without the required event path, correlation result and negative controls.

For the strongest demonstrated case, see the [WFP Port Scan case study](../../projects/soc-operations-lab/detection-rules/WFP_PortScan_Detection_Final.md) and the [evidence matrix](../../projects/soc-operations-lab/evidence/evidence-matrix.md).
