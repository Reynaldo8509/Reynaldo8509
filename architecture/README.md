# Architecture

This SOC lab simulates a real-world monitoring environment.

## Components

- Wazuh Manager (SIEM)
- Windows 10 Endpoint (Sysmon + Wazuh Agent)
- Kali Linux (Attacker)

## Data Flow

1. Logs generated on Windows
2. Collected by Wazuh Agent
3. Sent to Wazuh Manager
4. Alerts generated
5. Analyst performs triage
