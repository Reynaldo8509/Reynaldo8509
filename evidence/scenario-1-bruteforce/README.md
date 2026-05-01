# Scenario 1 — Brute Force Attack

## Description
Simulated brute force attack against Windows endpoint.

## Detection
- Event ID: 4625
- Multiple failed login attempts

## Evidence
- attack.png → ejecución del ataque
- wazuh-alert.png → alerta en SIEM
- logs.json → logs exportados

## MITRE ATT&CK
T1110 - Brute Force
