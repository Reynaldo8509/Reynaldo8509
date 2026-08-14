# 08 — Command Reference and Reproduction Notes

This document records commands that are supported by the current public lab evidence. It intentionally does **not** invent installer commands that were not preserved in the sanitized project history.

## 1. Verify the VirtualBox host networks (Kali)

```bash
ip -br -4 addr
ip route
```

Expected lab interfaces/routes include:

```text
192.168.56.0/24  -> ATTACK/LAB
192.168.57.0/24  -> MANAGEMENT
```

## 2. Verify Ubuntu/Wazuh network assignments

```bash
ip -br -4 addr show scope global
```

Expected addresses in this lab:

```text
192.168.56.10  ATTACK/LAB
192.168.57.10  MANAGEMENT
10.0.2.3       NAT/INTERNET
```

## 3. Verify Windows 11 IPv4 assignments

Run in PowerShell:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress, AddressState
```

Expected lab addresses:

```text
192.168.56.20  ATTACK/LAB
192.168.57.20  MANAGEMENT
10.0.2.15      NAT/INTERNET
```

## 4. Verify management connectivity from Kali

```bash
ping -c 3 192.168.57.10
ping -c 3 192.168.56.10
ping -c 3 192.168.57.20
ping -c 3 192.168.56.20
```

Management SSH is intentionally performed through `192.168.57.0/24`.

Examples:

```bash
ssh soc-admin@192.168.57.10 'hostname; ip -br -4 addr'
ssh endpointuser@192.168.57.20 'hostname'
```

## 5. Verify Sysmon Event ID 3 on Windows

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-Sysmon/Operational'
    Id=3
} -MaxEvents 20 |
Select-Object TimeCreated, Id, Message |
Format-List
```

This is useful for separating legitimate management connections from ATTACK/LAB test traffic before changing a detector.

## 6. Verify the live Wazuh ruleset on Ubuntu

```bash
sudo grep -Rni "sysmon_event3" /var/ossec/ruleset/rules/
sudo grep -Rni "eventID.*3" /var/ossec/ruleset/rules/0595-win-sysmon_rules.xml
```

Check the custom WFP rules:

```bash
sudo sed -n '/<rule id="100500"/,/<\/rule>/p' /var/ossec/etc/rules/local_rules.xml
sudo sed -n '/<rule id="100501"/,/<\/rule>/p' /var/ossec/etc/rules/local_rules.xml
sudo sed -n '/<rule id="100502"/,/<\/rule>/p' /var/ossec/etc/rules/local_rules.xml
```

## 7. Validate local rules safely

`local_rules.xml` intentionally contains multiple top-level `<group>` fragments, so strict XML validation should be performed against a temporary wrapper:

```bash
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
```

Then verify the manager:

```bash
systemctl is-active wazuh-manager
```

## 8. Inspect WFP telemetry in archives

For the validated ATTACK/LAB scan, filter the archived Windows Security events with `jq`:

```bash
jq -c 'select(.data.win.eventdata.sourceAddress == "192.168.56.1" and .data.win.eventdata.destAddress == "192.168.56.20" and (.data.win.system.eventID == "5152" or .data.win.system.eventID == "5157"))' /var/ossec/logs/archives/archives.json
```

## 9. Inspect visible correlation alerts

```bash
jq -c 'select(.rule.id == "100501" or .rule.id == "100502")' /var/ossec/logs/alerts/alerts.json
```

## 10. Reproduce a controlled port-scan test

The validated evidence used this exact Nmap command against the Windows ATTACK/LAB address:

```bash
nmap -Pn -sT -p 20,21,23,25,53,80,110,143,161,389,443,636,993,995,5985 192.168.56.20
```

Run attack tests only from the ATTACK/LAB plane. Do not use the MANAGEMENT or NAT interfaces as scan sources for this use case.

## 11. Installation history vs. operational commands

The public repository currently preserves the architecture, validation and operational commands above, but the exact original installation transcripts for VirtualBox, Wazuh Manager, Windows Agent, Sysmon and YARA were intentionally kept out of the public repository because the historical transcripts contained operational material and potentially sensitive configuration.

When the lab is rebuilt, capture the exact installer commands in a **sanitized** installation transcript before declaring the procedure fully reproducible. Never publish passwords, tokens, private keys, authentication cookies, private certificates or unsanitized production configuration.
