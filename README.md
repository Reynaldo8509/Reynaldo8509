# 🛡️ SOC Home Lab — Threat Detection & Incident Response

A hands-on Security Operations Center (SOC) lab environment built to simulate 
real-world threat detection, log analysis, and incident response workflows.

---

## 🎯 Objectives

- Simulate Blue Team operations in a controlled environment
- Practice alert triage, investigation, and incident response (Tier 1 / Tier 2)
- Build detection rules based on real attack techniques (MITRE ATT&CK)
- Develop hands-on experience with enterprise-grade security tools

---

## 🏗️ Lab Architecture

---

## 🧰 Tools & Technologies

| Tool | Role | Version |
|------|------|---------|
| Wazuh | SIEM / XDR | 4.x |
| Sysmon | Endpoint Telemetry | 15.x |
| Windows 10 | Target Endpoint | Enterprise |
| Kali Linux | Attack Simulation | 2024.x |
| VirtualBox | Hypervisor | 7.x |

---

## 📁 Repository Structure

---

## 🔍 Detection Use Cases

| # | Use Case | MITRE Technique | Status |
|---|----------|----------------|--------|
| 1 | Brute Force Login Detection | T1110 | ✅ Documented |
| 2 | Privilege Escalation | T1068 | 🔄 In progress |
| 3 | Suspicious PowerShell Execution | T1059.001 | 🔄 In progress |
| 4 | Lateral Movement Detection | T1021 | 📋 Planned |

---

## 📊 SOC Workflow Simulated

1. **Attack Simulated** → Kali Linux executes brute force against Windows endpoint
2. **Telemetry Collected** → Sysmon captures Event ID 4625 (failed login)
3. **Logs Forwarded** → Wazuh Agent sends logs to Wazuh Manager
4. **Alert Generated** → Correlation rule triggers alert in SIEM
5. **Triage (Tier 1)** → Validate alert, identify source IP, check targeted account
6. **Investigation (Tier 2)** → Correlate logs, detect lateral movement, analyze behavior
7. **Response** → Lock account, block IP, enforce password reset, escalate if needed

---

## 🧠 Skills Demonstrated

- SIEM configuration and log management (Wazuh)
- Endpoint monitoring and telemetry (Sysmon + Windows Event Logs)
- Alert triage and incident investigation
- Detection rule creation based on MITRE ATT&CK
- Attack simulation and Blue Team response
- Documentation of SOC use cases and IR playbooks

---

## 📌 Key Windows Event IDs Used

| Event ID | Description |
|----------|-------------|
| 4625 | Failed logon attempt |
| 4624 | Successful logon |
| 4672 | Special privileges assigned |
| 4688 | New process created |
| 7045 | New service installed |

---

## 🚀 Lab Setup (Summary)

> Full setup documentation coming soon in `/setup/` folder.

- VirtualBox with 3 VMs: Kali, Windows 10, Wazuh Manager (Ubuntu)
- Sysmon deployed on Windows with custom config
- Wazuh Agent installed and connected to Manager
- Custom detection rules loaded in Wazuh

---

## 📄 License

MIT License — © 2026 Reynaldo Amado Rodríguez González
