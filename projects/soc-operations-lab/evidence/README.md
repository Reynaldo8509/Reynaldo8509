# Evidence Inventory

## Curated Visual Screenshots

The following eight screenshots are curated artifacts derived from visually reviewed historical material. Some retain the original pixels and others are safe crops that remove irrelevant context; therefore, they are not described as unmodified copies. SOC HomeLab private addresses are retained because they document the ATTACK/LAB and NAT networks. Originals remain outside the repository.

| Image | Category | What it demonstrates |
|---|---|---|
| [windows-endpoint-attack-nat-connectivity.png](screenshots/windows-endpoint-attack-nat-connectivity.png) | Architecture / Windows endpoint | The Windows 11 endpoint has ATTACK/LAB interface `192.168.56.20`, NAT interface `10.0.2.15`, and connectivity to the ATTACK/LAB manager. |
| [wazuh-windows-agent-enrollment.jpg](screenshots/wazuh-windows-agent-enrollment.jpg) | Wazuh / enrollment | Dashboard shows the Windows agent enrollment flow and ATTACK/LAB manager `192.168.56.10`. |
| [wazuh-endpoint-summary.jpg](screenshots/wazuh-endpoint-summary.jpg) | Wazuh / endpoint | Historical summary of the Windows endpoint managed by Wazuh 4.14.7. |
| [wazuh-events-explorer.jpg](screenshots/wazuh-events-explorer.jpg) | Wazuh / event exploration | Historical Dashboard exploration of endpoint events; it provides observability context, not additional detector validation. |
| [wazuh-mitre-dashboard.jpg](screenshots/wazuh-mitre-dashboard.jpg) | Wazuh / MITRE | Historical Dashboard MITRE view that illustrates endpoint telemetry analysis; it is not attributed to WFP or Sysmon EID 3. |
| [wfp-eventchannel-attack-lab.png](screenshots/wfp-eventchannel-attack-lab.png) | WFP / raw EventChannel | Decoded ATTACK/LAB WFP event with source `192.168.56.1`, destination `192.168.56.20`, and TCP. It demonstrates the telemetry that feeds the detection. |
| [wfp-blocked-connections-attack-lab.png](screenshots/wfp-blocked-connections-attack-lab.png) | WFP / network evidence | Records of blocked TCP connections from Kali ATTACK/LAB to the Windows endpoint. It complements the published WFP evidence. |
| [windows-sysmon-installation.png](screenshots/windows-sysmon-installation.png) | Sysmon / endpoint | Successful Sysmon installation on Windows. It is endpoint-preparation evidence, not validation of the Sysmon Event ID 3 detection. |

The WFP Port Scan detection is **VALIDATED as a documented controlled run** by historical real-event results, `archives.json`, and `alerts.json`; the WFP screenshots provide visual support. Raw HomeLab logs are not published, so readers can review the method and reconstruction but not a raw-log package. Rules `100500`, `100501`, and `100502` are a high-signal heuristic detection, not an exact count of unique ports. Sysmon Event ID 3 remains **AUDITED / PENDING VALIDATION**: there is still no published evidence of a real ATTACK EID 3 `192.168.56.1 -> 192.168.56.20` that validates that scenario.

See the [evidence matrix](evidence-matrix.md) to understand which claim each artifact supports and the [complete image catalog](image-catalog.md) for the individual publication decision.

## Publication Decision

- **PUBLISH_AS_IS / CURATED_DERIVATIVE:** the eight images in the table received real visual review. The catalog identifies which correspond directly to the current source set and which are derived crops.
- **SANITIZE_AND_PUBLISH:** no new screenshot was added during this audit. Catalog B candidates require a crop that preserves technical meaning and a second review; they were not published because of evidence priority.
- **DO_NOT_PUBLISH:** the identified source directory currently contains 53 screenshots. The remaining images stay outside the repository because of login or session-reset screens, password prompts, personal paths or names, browser bookmarks, public addresses, unnecessary commands, contradiction with the final status, or low documentary value.
- **VISUAL_REVIEW_PENDING:** none of the published images.

Review of the eight copies found no passwords, tokens, private keys, cookies, authentication codes, or login screens. Complete HomeLab logs, transcripts, and historical material are not uploaded without a public purpose and individual review.

## Scenario Evidence

| Path | Type | Publication Status |
|---|---|---|
| `scenario-1-bruteforce/` | Historical authentication telemetry | Sanitized CSV of five `4625` events; it proves individual events, not a brute-force detection. |
