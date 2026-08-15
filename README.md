# Reynaldo Rodríguez

## IT & Network Specialist | Junior SOC Analyst Candidate | Blue Team

**Windows & Linux · Networking · Wazuh · Sysmon · Log Analysis · Detection Engineering**

IT professional with **15+ years of hands-on experience** across Windows/Linux support, systems administration, networking, endpoint troubleshooting and infrastructure operations, now focused on translating that background into **Junior SOC / Blue Team** capability.

My security development combines structured troubleshooting with practical lab work in **Wazuh, Sysmon, Windows Event Logs, Windows Filtering Platform (WFP), network analysis, alert triage, IOC review and MITRE ATT&CK-aware investigation**. I deliberately distinguish validated detections from scenarios that are still under audit or controlled validation.

**Target roles:** Junior SOC Analyst · Security Operations · Blue Team · Junior Cybersecurity Analyst

### Recruiter Quick Links

[**SOC HomeLab**](projects/soc-operations-lab/README.md) · [**WFP Case Study**](projects/soc-operations-lab/detection-rules/WFP_PortScan_Detection_Final.md) · [**Evidence Matrix**](projects/soc-operations-lab/evidence/evidence-matrix.md) · [**Command Reference**](projects/soc-operations-lab/docs/setup/08-command-reference.md) · [**Credly**](https://www.credly.com/users/reynaldo-amado-rodriguez-gonzalez) · [**LinkedIn**](https://www.linkedin.com/in/reynaldo8509/)

## Evidence Snapshot

| HomeLab signal | Result |
|---|---|
| WFP port-scan use case | **Validated — documented controlled run** |
| WFP telemetry observed | **34 records / 15 raw destination ports** |
| Network planes | **3 — MANAGEMENT / ATTACK-LAB / NAT-INTERNET** |
| SIEM stack | **Wazuh 4.14.7 + Windows Security + Sysmon** |
| Current detection discipline | **Evidence-backed status with explicit limitations** |

## Selected Technical Outcomes

- Built and documented a Wazuh WFP port-scan use case using **34 real Windows telemetry records across 15 raw destination ports**.
- Designed three separated network planes to retain legitimate telemetry while reducing WFP detector false positives.
- Documented detection-engineering decisions, correlation heuristics, negative controls, engine limitations and reproducibility commands.

## What I Bring to a SOC Team

- Strong Windows/Linux troubleshooting and endpoint administration background
- Network administration across **TCP/IP, DNS, DHCP, VLANs, routing, segmentation and firewalls**
- Experience with **Active Directory / AD DS, Group Policy, access management and server operations**
- Practical SIEM and endpoint telemetry work with **Wazuh + Sysmon + Windows EventChannel**
- Structured log analysis, alert triage, root-cause analysis and technical documentation
- Blue Team training in cybersecurity monitoring, threat management, network defense and endpoint security

## Featured Project — SOC Operations Lab

A reproducible VirtualBox **SOC HomeLab** built with Kali Linux, Ubuntu/Wazuh and a Windows 11 endpoint. The lab documents architecture, network-plane separation, detection engineering, evidence handling, validation methodology, false-positive reduction and known engine limitations. The project foregrounds inspected Wazuh, Windows and WFP evidence rather than treating diagrams as proof.

![SOC HomeLab architecture showing Kali Linux, Windows 11 with Wazuh Agent and Sysmon, Ubuntu/Wazuh Manager 4.14.7, Wazuh Dashboard, and separated management, attack/lab, and NAT network planes](assets/soc-home-lab-hero.svg)

### Validated Detection Case — WFP Port Scan

```text
ATTACK/LAB
192.168.56.1 (Kali)
        |
        | controlled TCP reconnaissance
        v
192.168.56.20 (Windows 11)
        |
        | WFP 5152 / 5157
        v
Wazuh Agent
        |
        v
Wazuh Manager 4.14.7
        |
        | correlation: 100500 -> 100501 / 100502
        v
Wazuh Dashboard
```

**Documented controlled validation:** 34 WFP records over 15 raw destination ports, with negative tests on MANAGEMENT and NAT traffic. The correlation rules are **heuristics**, not exact `COUNT(DISTINCT destinationPort)` logic. The repository documents historical `archives.json`/`alerts.json` results but does not publish raw HomeLab logs or direct Dashboard proof.

- **WFP Port Scan:** VALIDATED — documented controlled run
- **Sysmon Event ID 3:** AUDITED / PENDING VALIDATION
- **Windows authentication / brute force:** TELEMETRY OBSERVED / PENDING DETECTION VALIDATION
- **YARA:** PENDING VALIDATION
- **FIM:** CONFIGURED / REVALIDATION PENDING

[Explore the full SOC Operations Lab →](projects/soc-operations-lab/README.md)

[Evidence matrix](projects/soc-operations-lab/evidence/evidence-matrix.md) · [WFP case study](projects/soc-operations-lab/detection-rules/WFP_PortScan_Detection_Final.md) · [Historical command reference](projects/soc-operations-lab/docs/setup/08-command-reference.md)

## Core Skills

| Area | Skills |
|---|---|
| **SOC / Blue Team** | Wazuh, Sysmon, Windows Event Logs, WFP telemetry, log analysis, alert triage, IOC review, MITRE ATT&CK awareness, incident documentation |
| **Detection Engineering** | Custom Wazuh rules, event correlation, threshold tuning, false-positive reduction, validation methodology, evidence-backed detection claims |
| **Infrastructure** | Windows, Linux, Windows Server, Active Directory / AD DS, Group Policy, TCP/IP, DNS, DHCP, VLANs, routing and firewalls |
| **Tools / Automation** | Kali, Wireshark, Nmap, PowerShell, Bash/Linux CLI, Python fundamentals, SQL basics, `jq`, technical reporting |

## Certifications & Credentials

### Cybersecurity & SOC — Featured

| Credential | Issuer | Relevance |
|---|---|---|
| [CyberOps Associate](https://www.credly.com/org/cisco/badge/cyberops-associate) | Cisco | Security operations, intrusion analysis and security monitoring |
| [Google Cybersecurity Professional Certificate (v.2)](https://www.credly.com/org/coursera/badge/google-cybersecurity-professional-certificate-v-2) | Coursera | Entry-level cybersecurity and SOC foundations |
| [Junior Cybersecurity Analyst Career Path](https://www.credly.com/org/cisco/badge/junior-cybersecurity-analyst-career-path.1) | Cisco | Network and endpoint defense, alerting and incident-response concepts |
| [Cyber Threat Management](https://www.credly.com/org/cisco/badge/cyber-threat-management) | Cisco | Threat management, risk and incident-response concepts |
| [Network Defense](https://www.credly.com/org/cisco/badge/network-defense) | Cisco | Network monitoring and defensive controls |
| [Endpoint Security](https://www.credly.com/org/cisco/badge/endpoint-security) | Cisco | Endpoint protection and host-based defense |

Credentials support the lab; they do not replace hands-on evidence.

See the broader [certification and credential inventory](docs/certifications/README.md) and my [public Credly profile](https://www.credly.com/users/reynaldo-amado-rodriguez-gonzalez).

## SOC Workflow

```text
01  Generate controlled activity
02  Collect endpoint telemetry
03  Decode / normalize the event path
04  Apply base tracking rule
05  Correlate and evaluate thresholds
06  Validate against real HomeLab evidence
07  Investigate false positives / negatives
08  Document result and limitations
```

## False-Positive Reduction

The HomeLab deliberately separates three network planes so legitimate traffic remains observable without feeding the WFP port-scan detector:

```text
MANAGEMENT 192.168.57.0/24
    -> retained telemetry
    -> excluded from WFP scan correlation

NAT/INTERNET 10.0.2.0/24
    -> retained telemetry
    -> excluded from WFP scan correlation

ATTACK/LAB 192.168.56.0/24
    -> controlled reconnaissance
    -> eligible for the WFP port-scan detector
```

This separation was a key part of reducing false positives without globally silencing legitimate telemetry.

## Professional Background

My professional experience spans **IT Support, Help Desk, systems administration and network administration**, including Windows/Linux environments, Active Directory, server operations, networking and structured troubleshooting.

My current work in **AI quality analysis and data annotation** also strengthens attention to detail, guideline-based evaluation, ambiguity handling and structured quality documentation. This complements, rather than replaces, my IT and cybersecurity career direction.

## Target Roles

Open to **Junior SOC Analyst, Security Operations, Blue Team and entry-level Cybersecurity Analyst** roles, with a focus on Windows/Linux monitoring, detection engineering, log analysis and incident-response fundamentals.

## Current Focus

Building practical **Blue Team / SOC** capability through controlled detection scenarios, log analysis, endpoint telemetry, evidence-backed validation and technical writing.

## Technical Portfolio

- [Technical profile](docs/technical-profile/README.md)
- [Career and professional scope](docs/career/README.md)
- [SOC HomeLab setup and command reference](projects/soc-operations-lab/docs/setup/README.md)
- [SOC HomeLab architecture](projects/soc-operations-lab/docs/architecture/README.md)
- [SOC HomeLab detection engineering index](projects/soc-operations-lab/detection-rules/README.md)
- [SOC HomeLab evidence inventory](projects/soc-operations-lab/evidence/README.md)
- [SOC HomeLab evidence catalog](projects/soc-operations-lab/evidence/image-catalog.md)

## Additional Project

### LG TV Tools

[LG TV Tools](https://github.com/Reynaldo8509/lg-tv-tools) is an independent Python/PyQt6 Linux application for discovering LG webOS TVs and supporting screen mirroring, desktop casting and media handoff through SSDP, UPnP AVTransport and DLNA.

## Connect

- [LinkedIn](https://www.linkedin.com/in/reynaldo8509/)
- [Credly](https://www.credly.com/users/reynaldo-amado-rodriguez-gonzalez)

## Responsible Use

Security material in this portfolio is for authorized environments, education and professional development. Detection status and project claims are intentionally evidence-based and scoped to the documented lab environment.
