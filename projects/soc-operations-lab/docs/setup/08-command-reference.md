# 08 — Historical command reference

This is a record of commands evidenced in the lab documentation, validation record or reviewed HomeLab captures. It is **not** a generic build guide. A command is listed as executed only when its use is directly documented; variables, credentials and commands with no historical trace are intentionally omitted.

## Evidence standard

| Label | Meaning |
|---|---|
| **Captured execution** | The command and its result are visible in a reviewed HomeLab screenshot. |
| **Validation record** | The exact command is recorded in the WFP validation documentation. |
| **Not enough historical evidence** | The command may be useful, but no exact invocation was found. It is not presented as used. |

## Phase 01 — VirtualBox

**NOT ENOUGH HISTORICAL EVIDENCE.** The screenshots show Ubuntu and Windows running in VirtualBox, but no `VBoxManage` command, VM-creation command, adapter-assignment command, snapshot command or export command was recovered. The repository documents the intended three-plane design, not a reconstructable VirtualBox command history.

## Phase 02 — Ubuntu installation and Wazuh Manager

### Install the documented Wazuh all-in-one deployment

**Purpose:** start the Wazuh installation assistant on the Ubuntu manager.

**Command:**

```bash
sudo ./wazuh-install.sh -a
```

**Expected result:** the installer reports Wazuh `4.14.7`, creates its components and completes manager/indexer/Dashboard installation.

**What it proves:** captured execution of the installation assistant in this HomeLab; it does not publish installer inputs, certificates or active configuration.

### Check the manager service

**Purpose:** verify that the Wazuh Manager service is active after installation.

**Command:**

```bash
sudo systemctl status wazuh-manager --no-pager
```

**Expected result:** `Active: active (running)` for `wazuh-manager.service`.

**What it proves:** captured historical manager service state, not a current live check.

### Check indexer and Dashboard services

**Purpose:** inspect the historical state of the two other Wazuh components.

**Command:**

```bash
sudo systemctl status wazuh-indexer --no-pager
sudo systemctl status wazuh-dashboard --no-pager
```

**Expected result:** each service reports `active (running)`.

**What it proves:** captured service health after installation; it does not prove a particular alert was indexed or visible in the UI.

## Phase 03 — Windows 11 and Wazuh Agent

### Install and start the Wazuh agent

**Purpose:** install the Wazuh Windows agent configured for the ATTACK/LAB manager and start its service.

**Command:**

```powershell
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.14.7-1.msi -OutFile $env:tmp\wazuh-agent; msiexec.exe /i $env:tmp\wazuh-agent /q WAZUH_MANAGER='192.168.56.10' WAZUH_AGENT_NAME='WIN11-ENDPOINT'
NET START Wazuh
```

**Expected result:** the service reports that it started successfully.

**What it proves:** captured command execution and service start for the historical endpoint. It does not expose an active agent configuration.

### Verify the Wazuh agent service

**Purpose:** confirm the local Windows service state.

**Command:**

```powershell
Get-Service Wazuh
```

**Expected result:** `WazuhSvc` is `Running`.

**What it proves:** captured historical service state. The separate Dashboard capture provides historical enrollment context.

## Phase 04 — Sysmon

### Create the working directory and retrieve Sysmon materials

**Purpose:** prepare the Windows endpoint for Sysmon installation and retrieve the documented configuration source.

**Command:**

```powershell
New-Item -ItemType Directory -Force -Path C:\Sysmon
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "C:\Sysmon\Sysmon.zip"
Expand-Archive -Path "C:\Sysmon\Sysmon.zip" -DestinationPath "C:\Sysmon" -Force
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml" -OutFile "C:\Sysmon\sysmonconfig-export.xml"
Get-ChildItem C:\Sysmon
```

**Expected result:** the directory contains the Sysmon binaries, archive and configuration XML.

**What it proves:** captured execution of the preparation/download steps. The referenced configuration was historical input; its active final XML is not published as a portable lab configuration.

### Install and verify Sysmon

**Purpose:** install Sysmon64 with the downloaded XML and verify the service.

**Command:**

```powershell
cd C:\Sysmon
.\Sysmon64.exe -accepteula -i .\sysmonconfig-export.xml
Get-Service Sysmon64
```

**Expected result:** installation reports a validated configuration and `Sysmon64` reports `Running`.

**What it proves:** captured Sysmon installation and service state. It does **not** validate the ATTACK/LAB Event ID 3 detector.

## Phase 05 — YARA

**NOT ENOUGH HISTORICAL EVIDENCE.** No exact installation command, rule provenance, deployment configuration, event or alert was recovered. No YARA command is represented as used.

## Phase 06 — Network and Windows Firewall telemetry

### Check Windows Firewall logging configuration

**Purpose:** inspect profile state and the configured firewall-log behavior.

**Command:**

```powershell
Get-NetFirewallProfile | Select Name, Enabled, LogFileName, LogAllowed, LogBlocked
```

**Expected result:** output lists Domain, Private and Public profiles and their logging values.

**What it proves:** captured historical inspection of Windows Firewall profile logging; it is not a full proof of the final three-plane routing configuration.

### Inspect the Windows Firewall log tail

**Purpose:** inspect recent connection records in the firewall log.

**Command:**

```powershell
Get-Content "C:\Windows\system32\LogFiles\Firewall\pfirewall.log" -Tail 20
```

**Expected result:** the last 20 firewall-log entries are displayed.

**What it proves:** captured use of the firewall log as supporting network evidence. The uncurated source capture contains external destinations, so it is not published.

### Confirm ATTACK/LAB reachability from the manager

**Purpose:** test reachability to the Windows endpoint on the ATTACK/LAB plane.

**Command:**

```bash
ping 192.168.56.20
```

**Expected result:** replies from `192.168.56.20` with no observed packet loss in the historical capture.

**What it proves:** a point-in-time reachability test only; it does not document adapter creation, routes or management-plane configuration.

## Phase 07 — SSH Management

**NOT ENOUGH HISTORICAL EVIDENCE.** Ubuntu installation captures show OpenSSH was selected, but no exact `ssh`, `sshd_config`, key-generation or key-only-hardening command was recovered. SSH administration is documented architecturally but no command is labelled as executed.

## Phase 08 — WFP detection engineering and validation

### Validate the local rules fragment and manager ruleset

**Purpose:** syntax-check a multi-fragment `local_rules.xml` without changing the live file, then test the analyzer configuration.

**Command:**

```bash
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
systemctl is-active wazuh-manager
```

**Expected result:** `xmllint` returns cleanly, the analyzer check has no new warnings, and the manager is active.

**What it proves:** validation-record evidence for the WFP ruleset deployment. It does not by itself prove EventChannel matching or alert creation.

### Generate the documented 15-port WFP validation scenario

**Purpose:** generate the controlled ATTACK/LAB TCP activity used in the final WFP case study.

**Command:**

```bash
nmap -Pn -sT -p 20,21,23,25,53,80,110,143,161,389,443,636,993,995,5985 192.168.56.20
```

**Expected result:** a controlled scan of the listed Windows endpoint ports from the ATTACK/LAB source.

**What it proves:** the documented validation record attributes the 34 WFP events and 15 raw destination ports to this command. It does not make `100501` or `100502` a distinct-port counter.

### Inspect archived WFP telemetry and created correlation alerts

**Purpose:** distinguish ingestion from alert creation after the controlled run.

**Command:**

```bash
jq -c 'select(.data.win.eventdata.sourceAddress == "192.168.56.1" and .data.win.eventdata.destAddress == "192.168.56.20" and (.data.win.system.eventID == "5152" or .data.win.system.eventID == "5157"))' /var/ossec/logs/archives/archives.json
jq -c 'select(.rule.id == "100501" or .rule.id == "100502")' /var/ossec/logs/alerts/alerts.json
```

**Expected result:** WFP events are selected from `archives.json`; visible correlation alerts are selected from `alerts.json`.

**What it proves:** the documented evidence method for the validated WFP run. Raw HomeLab log files remain private, so the repository records the result and method rather than publishing them.

### Historical full-port reconnaissance command

**Purpose:** conduct an earlier, broader controlled SYN scan of the HomeLab endpoint.

**Command:**

```bash
sudo nmap -Pn -sS -T4 -p- 192.168.56.20
```

**Expected result:** Nmap reports the reachable endpoint and scanned TCP-port states.

**What it proves:** a captured historical reconnaissance command. It is not the 15-port WFP validation run and should not be cited as its evidence.

## Phase 09 — Validation boundaries and unavailable command history

The following requested commands/tools were searched for in the repository, historical text and reviewed HomeLab captures. No exact historical invocation was recovered, so they are deliberately **not** presented as used:

| Area | Not enough historical evidence for |
|---|---|
| VirtualBox and networking | `VBoxManage`, `ip`, `ip route`, route-addition or adapter configuration commands |
| Linux operations | `ssh`, `grep`, `sed`, `journalctl` and an exact `wazuh-logtest` invocation |
| Windows investigation | `Get-WinEvent`, `Get-NetIPAddress`, OpenSSH service/configuration commands |
| YARA, FIM and brute force | installation, rule deployment, controlled-validation or alert-query commands |

Useful commands must be captured in a future controlled run before they are added here as historical evidence. Do not backfill this document with generic commands.

## Installation-history coverage

| Phase | Historical evidence available? | Boundary |
|---|---|---|
| 01 VirtualBox | Partial visual only | VM windows are visible; creation/adapter commands are absent. |
| 02 Ubuntu | Partial visual and command evidence | Installer states and Wazuh installation are captured; no full Ubuntu install script/history. |
| 03 Wazuh Manager | Yes, partial reproducibility | Installer and service checks exist; certificates/active configuration remain private. |
| 04 Windows 11 | Partial visual only | Endpoint and PowerShell are visible; no step-by-step OS install history. |
| 05 Wazuh Agent | Yes | Install, start and service verification are captured. |
| 06 Sysmon | Yes | Directory, downloads, installation and service verification are captured. |
| 07 YARA | **NOT ENOUGH HISTORICAL EVIDENCE** | No command or end-to-end evidence. |
| 08 Networking | Partial visual and command evidence | IP/routing design and ping/firewall inspection exist; full adapter/routing history is absent. |
| 09 SSH Management | **NOT ENOUGH HISTORICAL EVIDENCE** | OpenSSH selection is visible, not operational command history. |
| 10 Detection Rules | Yes for WFP only | Syntax/analyzer checks and WFP validation commands are documented; other rules lack equivalent evidence. |
| 11 Validation | Yes for WFP; partial elsewhere | WFP has documented positive/negative validation; Sysmon, FIM, YARA and brute force remain incomplete. |

See the [evidence matrix](../../evidence/evidence-matrix.md) for the claim boundary of each capability.
