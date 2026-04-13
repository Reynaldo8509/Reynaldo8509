# 🛡️ SOC Home Lab — Threat Detection & Incident Response

A hands-on Security Operations Center (SOC) lab environment built to simulate real-world threat detection, log analysis, and incident response workflows.

---

## 🎯 Objectives

* Simulate Blue Team operations in a controlled environment
* Practice alert triage, investigation, and incident response (Tier 1 / Tier 2)
* Build detection rules based on real attack techniques (MITRE ATT&CK)
* Develop hands-on experience with enterprise-grade security tools

---

## 🏗️ Lab Architecture

```
[Kali Linux - Attacker]
│
│ Simulated attacks (brute force, enumeration)
▼
[Windows 10 Endpoint]
- Sysmon (telemetry)
- Wazuh Agent (log forwarding)
│
▼
[Wazuh Manager - SIEM]
- Log collection & correlation
- Alert generation
│
▼
[SOC Analyst]
```

---

## 🧰 Tools & Technologies

* Wazuh (SIEM)
* Sysmon (Endpoint Telemetry)
* Windows 10
* Kali Linux
* VirtualBox

---

## 📁 Repository Structure

```
soc-operations-lab/
│
├── README.md
├── LICENSE
├── architecture/
├── wazuh/
├── sysmon/
├── detection-rules/
├── incident-response/
├── evidence/
```

---

## 🔍 Detection Use Cases

* Brute Force Login Detection (T1110)
* Privilege Escalation (in progress)
* Suspicious PowerShell (in progress)

---

## 📊 SOC Workflow Simulated

1. Attack simulated from Kali
2. Logs generated in Windows (Event ID 4625)
3. Logs sent to Wazuh
4. Alert generated
5. Triage (Tier 1)
6. Investigation (Tier 2)
7. Response actions

---

## 🧠 Skills Demonstrated

* SIEM monitoring (Wazuh)
* Log analysis (Windows Events)
* Detection engineering
* Incident response workflow
* MITRE ATT&CK usage

---

## 📌 Key Event IDs

* 4625 → Failed login
* 4624 → Successful login
* 4672 → Privileged login
* 4688 → Process creation

---

## 🚀 Lab Setup (Summary)

* 3 VMs: Kali, Windows 10, Wazuh
* Sysmon installed
* Wazuh agent connected
* Detection rules configured

---

## 📸 Evidence (Coming Soon)

This section will include:

* Wazuh alerts screenshots
* Brute force logs
* Investigation process

---

## 📄 License

MIT License — © 2026 Reynaldo Amado Rodríguez González
