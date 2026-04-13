## Sysmon
Sysmon provides detailed endpoint telemetry.

- Logs Collected
  
-Process creation

-Network connections

-File modifications

-Registry changes


---

# Architecture

This SOC lab simulates a real-world Security Operations Center environment.

---


## 🧱 Components

- **Wazuh Manager (SIEM)**
  - Centralized log collection
  - Alert generation
  - Correlation engine

- **Windows 10 Endpoint**
  - Sysmon installed for detailed telemetry
  - Wazuh Agent for log forwarding

- **Kali Linux**
  - Used to simulate attacks (brute force, enumeration, exploitation)

---

## 🔄 Data Flow

1. Events generated on Windows (Sysmon + Event Logs)
2. Logs collected by Wazuh Agent
3. Forwarded to Wazuh Manager
4. Correlation rules applied
5. Alerts generated in SIEM
6. Analyst performs triage and investigation

---

## 🎯 Security Monitoring Goals

- Detect brute force attempts
- Identify privilege escalation
- Monitor suspicious PowerShell activity
- Detect malware execution

---

## 🧠 SOC Perspective

This lab replicates a Tier 1 / Tier 2 SOC workflow:

- Log ingestion
- Alert monitoring
- Triage
- Investigation
- Incident response
