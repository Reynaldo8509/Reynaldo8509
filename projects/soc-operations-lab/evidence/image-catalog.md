# HomeLab image catalog and publication decision

**Source reviewed:** `/mnt/DATOS/REY/Ciberseguridad/Proyecto SOC WASU/Capturas de pantalla/Ubuntu` on 2026-08-14. The directory currently contains **53** image files (not 57). Classification is intentional: **A** publish as evidence, **B** publish only after an exact safety-preserving crop, **C** internal only, **D** duplicate/not needed. “Source” names below are kept only in this catalog; source images remain outside Git.

The existing public set has eight curated images. Seven have an obvious source counterpart in the current directory; `windows-endpoint-attack-nat-connectivity.png` is a real technical capture already in the repository but its exact source file was not found in this particular directory, so it is retained and marked as **source-unmatched** rather than falsely attributed.

## Ubuntu / Kali source folder

| Source image (resolution, type) | Machine / component / event | Technical value and possible GitHub support | Decision |
|---|---|---|---|
| `1-Captura...214354.png` (1027×918 PNG) | Ubuntu VM installer / base selection | Shows installer choice only; no final configuration. | C — generic setup screen. |
| `2-Captura...214732.png` (964×898 PNG) | Ubuntu VM installer / interfaces | Early DHCP/disabled interface state; not final topology. | C — incomplete and potentially confusing. |
| `3-Captura...215737.png` (985×897 PNG) | Ubuntu VM installer / ATTACK interface | Historical static `192.168.56.10` configuration. NAT address differs from final documented plan. | B — crop only if documenting an intermediate state, not final architecture. |
| `4-Captura...215851.png` (984×913 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `5-Captura...220012.png` (967×911 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `6-Captura...220124.png` (959×922 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `7-Captura...220148.png` (962×910 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `8-Captura...220314.png` (969×906 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `9-Captura...221011.png` (977×923 PNG) | Ubuntu installer | Installation configuration step. | C — no distinct operational proof. |
| `10-Captura...221909.png` (968×923 PNG) | Ubuntu installer / OpenSSH selection | Shows OpenSSH selection and password-auth option, not final hardening. | C — do not imply secure SSH configuration. |
| `11-Captura...222046.png` (968×911 PNG) | Ubuntu installer / snap list | Package-selection screen. | C — low evidence value. |
| `12-Captura...222251.png` (974×896 PNG) | Ubuntu installer / snap list | Same package-selection sequence as 11. | D — duplicate sequence. |
| `13-Captura...222310.png` (977×925 PNG) | Ubuntu installer / progress | Install-progress output. | C — no final service evidence. |
| `14-Captura...222605.png` (977×965 PNG) | Ubuntu installer / progress | Continuation of 13. | D — duplicate progress. |
| `15-Captura...225127.png` (1049×958 PNG) | Ubuntu boot / cloud-init | Boot completion output. | C — generic and less useful than service checks. |
| `16-Captura...225149.png` (730×373 PNG) | Ubuntu login | Login prompt. | C — authentication screen. |
| `17-Captura...225346.png` (1044×945 PNG) | Ubuntu login / `soc-admin` | Login sequence includes a password prompt. | C — internal only. |
| `18-Captura...20260729_111029.png` (627×488 PNG) | Ubuntu / Wazuh installer | `sudo ./wazuh-install.sh -a` starts Wazuh 4.14.7 installation; includes sudo-password prompt. | C — command is documented, image stays internal. |
| `19-Captura...111103.png` (793×960 PNG) | Ubuntu / Wazuh installer | Larger view of the same installation sequence. | D — duplicates 18 and includes auth prompt. |
| `20-Captura...111238.png` (791×952 PNG) | Ubuntu / Wazuh installer output | Installation progress for Wazuh components. | B — crop candidate for installation history; not needed beside service evidence. |
| `21-Captura...123627.png` (803×975 PNG) | Ubuntu / Wazuh manager install | Manager/indexer completion output. | B — crop candidate; lower priority than active-service proof. |
| `22-Captura...123627.png` (774×955 PNG) | Ubuntu / Wazuh Manager | `systemctl status wazuh-manager --no-pager` shows active service. | B — strong manager proof after exact terminal crop. |
| `23-Captura...123627.png` (796×944 PNG) | Ubuntu / Wazuh Indexer/Dashboard | Service-status output for indexer and Dashboard. | B — useful only after crop; service health is not UI evidence. |
| `24-Captura...123904.png` (798×957 PNG) | Ubuntu / Wazuh Dashboard service | `systemctl status wazuh-dashboard --no-pager` shows active state. | B — useful crop candidate, but not published this pass. |
| `26-Captura...123904.png` (1646×969 PNG) | Wazuh Dashboard | Initial Wazuh landing/login context before agent evidence. | C — no endpoint/detection proof. |
| `28-Captura...123904.png` (1920×1376 JPEG) | Wazuh Dashboard | Overview explicitly shows no agents registered. | C — contradicts the portfolio’s intended proof. |
| `29-Captura...123904.png` (1728×934 PNG) | Wazuh Dashboard | Password-reset dialog with masked password fields. | C — authentication-related screen. |
| `30-Captura...123904.png` (933×749 PNG) | Ubuntu manager / networking | `ping 192.168.56.20` replies from endpoint. | B — supports point-in-time ATTACK/LAB reachability only. |
| `31-Captura...123904.png` (815×168 PNG) | Kali / Nmap | Start of `sudo nmap -Pn -sS -T4 -p- 192.168.56.20`. | B — too narrow; crop with outcome would be required. |
| `32-Captura...123904.png` (991×601 PNG) | Windows endpoint / firewall | `Get-NetFirewallProfile` shows profile and log settings. | B — useful configuration evidence, not WFP detection validation. |
| `33-Captura...123904.png` (777×938 PNG) | Windows endpoint / firewall log | `Get-Content ...pfirewall.log -Tail 20` includes external destinations and local backup names. | C — retain internally; public version would need careful review. |
| `34-Captura...123904.png` (820×997 PNG) | Ubuntu manager / raw WFP EventChannel | Source `192.168.56.1`, destination `192.168.56.20`, port and protocol fields. | A — published as [`wfp-eventchannel-attack-lab.png`](screenshots/wfp-eventchannel-attack-lab.png). |
| `35-Captura...123904.png` (781×747 PNG) | Kali / Nmap output | Broad controlled scan result against `192.168.56.20`. | B — supports reconnaissance but is not the 15-port WFP validation run. |
| `36-Captura...123904.png` (760×901 PNG) | Windows endpoint / firewall log | ATTACK/LAB blocked TCP records plus NAT context. | A — curated derivative published as [`wfp-blocked-connections-attack-lab.png`](screenshots/wfp-blocked-connections-attack-lab.png). |

## Wazuh subfolder

| Source image (resolution, type) | Machine / component / event | Technical value and possible GitHub support | Decision |
|---|---|---|---|
| `1-Wazuh-08-05-2026_09_10.jpg` (1920×1997 JPEG) | Wazuh Dashboard / deploy agent | Shows Windows agent deployment details for `WIN11-ENDPOINT` and `192.168.56.10`. | A — published as [`wazuh-windows-agent-enrollment.jpg`](screenshots/wazuh-windows-agent-enrollment.jpg). |
| `10-Wazuh-08-05-2026_10_21.jpg` (1920×1302 JPEG) | Wazuh Dashboard / endpoint | Active Windows agent summary and Wazuh 4.14.7 endpoint context. | A — published as [`wazuh-endpoint-summary.jpg`](screenshots/wazuh-endpoint-summary.jpg). |
| `11-Wazuh-08-05-2026_10_21.jpg` (1920×967 JPEG) | Wazuh Dashboard / MITRE | Historical MITRE view; contextual only, not a WFP/Sysmon validation. | A — curated derivative published as [`wazuh-mitre-dashboard.jpg`](screenshots/wazuh-mitre-dashboard.jpg). |
| `2-Captura...20260805_091128.png` (1022×888 PNG) | Windows endpoint | Opening elevated PowerShell. | C — setup action only. |
| `2-Verificar que Sysmon quedó instalado.png` (1014×949 PNG) | Windows endpoint / Sysmon | Combined Sysmon download, install and service view. | B — redundant with focused install evidence. |
| `3-Captura...20260805_091128.png` (1021×913 PNG) | Windows endpoint / PowerShell | Empty elevated shell. | C — no technical result. |
| `4-Captura...20260805_091128.png` (1013×911 PNG) | Windows endpoint / Wazuh agent | Agent install command entered. | B — supports command history; service-start capture is stronger. |
| `5-Captura...20260805_091405.png` (1023×916 PNG) | Windows endpoint / Wazuh agent | Agent install plus `NET START Wazuh` success. | B — useful after terminal crop; not added to avoid redundant visuals. |
| `6-Captura...20260805_091405.png` (1917×736 PNG) | Wazuh Dashboard | Dashboard state with browser chrome/bookmarks. | C — do not publish unedited browser context. |
| `7-Captura...20260805_091405.jpg` (1920×1395 JPEG) | Wazuh Dashboard | Endpoint Dashboard with browser chrome/bookmarks. | C — public cropped endpoint summary is superior. |
| `7-Captura...20260805_091405.png` (1026×922 PNG) | Windows endpoint / Wazuh agent | `Get-Service Wazuh` returns `Running`. | B — strong service proof after crop; no new image needed. |
| `8-Wazuh-08-05-2026_10_21.jpg` (1920×1222 JPEG) | Wazuh Dashboard / endpoint | Endpoint dashboard variant. | B — duplicate context of published endpoint summary. |
| `9-Wazuh-08-05-2026_10_21.jpg` (1920×4403 JPEG) | Wazuh Dashboard / event explorer | Historical endpoint event exploration. | A — curated derivative published as [`wazuh-events-explorer.jpg`](screenshots/wazuh-events-explorer.jpg). |
| `Crear el directorio de trabajo Sysmon.png` (1022×928 PNG) | Windows endpoint / Sysmon | `New-Item -ItemType Directory -Force -Path C:\Sysmon`. | C — setup step already covered by focused evidence. |
| `Descargar Sysmon (Microsoft Sysinternals).png` (1028×913 PNG) | Windows endpoint / Sysmon | Download/extract/config retrieval commands. | B — supports command history, but repeats the combined setup capture. |
| `Paso 2 - Instalar Sysmon.png` (1024×492 PNG) | Windows endpoint / Sysmon | `Sysmon64.exe -accepteula -i ...` reports successful install. | A — published as [`windows-sysmon-installation.png`](screenshots/windows-sysmon-installation.png). |
| `Verificar que Sysmon quedó instalado.png` (343×94 PNG) | Windows endpoint / Sysmon | `Get-Service Sysmon64` returns `Running`. | C — too small and redundant with install result. |
| `Wazuh-08-05-2026_09_35.jpg` (1920×1221 JPEG) | Wazuh Dashboard / threat hunting | Historical aggregate dashboard, not a case-specific alert. | B — dashboard-context alternative; current event explorer is more useful. |
| `Wazuh-08-05-2026_09_36.jpg` (1920×4405 JPEG) | Image collage | Contact sheet of other captures. | D — duplicate index, not technical evidence. |

## Published-set review

| Published asset | Review outcome |
|---|---|
| `wfp-eventchannel-attack-lab.png` | Highest-value visual: real ATTACK/LAB WFP fields. Retain. |
| `wfp-blocked-connections-attack-lab.png` | Useful supporting network evidence; retain but do not treat as correlation-alert proof. |
| `windows-sysmon-installation.png` | Strong setup evidence; retain with EID 3 pending label. |
| `wazuh-windows-agent-enrollment.jpg` and `wazuh-endpoint-summary.jpg` | Strong agent/endpoint evidence; retain. |
| `wazuh-events-explorer.jpg` and `wazuh-mitre-dashboard.jpg` | Contextual Dashboard evidence; retain after WFP/Windows evidence in presentation order. |
| `windows-endpoint-attack-nat-connectivity.png` | Strong real architecture evidence. Retain, but its exact original was not present in the specified current source directory. |

No generated decorative image displaces real evidence in the current repository. The chief visual gap is a reviewed screenshot or sanitised export directly showing `100501` and `100502` alert results; it should be added only after a new controlled validation capture, not reconstructed from text.
