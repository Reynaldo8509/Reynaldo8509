# Persistent Master Context — SOC HomeLab

> Purpose: technical starting point for future sessions. It summarizes only persistent decisions, status, and boundaries; it does not replace evidence or active configurations. Last consolidation: 2026-08-13.

## 1. SOC HomeLab Objective

Build a reproducible SOC HomeLab based on VirtualBox that supports designing and validating Windows detections with verifiable evidence. The project criterion is to clearly separate received telemetry from a created alert, run authorized and controlled scenarios, and not declare a detection validated until its behavior has been verified with real events.

The main completed use case is heuristic reconnaissance/port-scan detection through Windows WFP events. Sysmon EID 3, brute force, YARA, and FIM retain distinct statuses and must not be presented as equivalent to that validation.

## 2. Architecture

| Component | Persistent Role |
|---|---|
| Kali Linux | Management from MANAGEMENT and controlled-scenario execution from ATTACK/LAB. |
| Ubuntu / Wazuh Manager 4.14.7 | Receives Windows EventChannel, analyzes and correlates events, stores local files, and feeds the alert pipeline. |
| Windows 11 Endpoint | Monitored endpoint with Wazuh Agent, Windows Security EventChannel, Sysmon, and FIM. |
| VirtualBox | SOC HomeLab virtualization platform and adapter/network segmentation. |

Telemetry flow:

```text
Windows Security / Sysmon -> Wazuh Agent -> Ubuntu Wazuh Manager
  -> archives.json (ingestion) -> ruleset/correlation -> alerts.json (alert)
  -> Filebeat -> Wazuh Indexer -> Wazuh Dashboard
```

`archives.json` proves that the manager ingested and decoded the event. `alerts.json` proves that a rule created an alert. Indexing and Dashboard visualization are an independent layer that require an authenticated query to the index or a visible UI check.

## 3. Three Networks

| Network | CIDR | Kali | Ubuntu / Wazuh | Windows 11 |
|---|---|---:|---:|---:|
| MANAGEMENT | `192.168.57.0/24` | `192.168.57.1` | `192.168.57.10` | `192.168.57.20` |
| ATTACK/LAB | `192.168.56.0/24` | `192.168.56.1` | `192.168.56.10` | `192.168.56.20` |
| NAT/INTERNET | `10.0.2.0/24` | — | `10.0.2.3` | `10.0.2.15` |

## 4. Purpose of Each Network

- **MANAGEMENT:** management, SSH, SCP/SFTP, WinRM, maintenance, and file transfer. It is legitimate telemetry and must not be classified as attack activity by default.
- **ATTACK/LAB:** the only network plane intended for reconnaissance and controlled detection tests against SOC HomeLab assets. For the WFP detector, only traffic from this network to Windows is eligible.
- **NAT/INTERNET:** updates, repositories, and normal external connectivity. Its telemetry is retained for investigation but does not feed the WFP port-scan detector.

## 5. Wazuh

- **Manager version:** `4.14.7`.
- **Manager location:** Ubuntu VM; addresses `192.168.57.10`, `192.168.56.10`, and `10.0.2.3` by network plane.
- **Active local rules:** `/var/ossec/etc/rules/local_rules.xml` on the manager.
- **Operational evidence files:** `/var/ossec/logs/archives/archives.json` and `/var/ossec/logs/alerts/alerts.json`.

### Rule Validation

`local_rules.xml` can contain fragments with multiple top-level groups, so the fragment is validated through a temporary wrapper without modifying the real file:

```bash
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
```

Treat any new `wazuh-analysisd -t` warning as a failure that must be investigated, even if the process returns zero. After an authorized change, validate with real EventChannel and check both `archives.json` and `alerts.json`; neither `wazuh-logtest` nor Filebeat health is sufficient.

## 6. WFP Port Scan

**Status: VALIDATED.** It is a high-signal, throttled detector for the SOC HomeLab, not an exact unique-port counter.

### Rules and Effective Path

```text
windows_eventchannel -> 60000 -> 60001 -> 100500 -> 100501 / 100502
```

The rules are in the manager's `local_rules.xml`:

| ID | Function | Key Parameters/Scope |
|---:|---|---|
| `100500` | Silent tracking base | Level 6; `if_sid=60001`; Security EID `5152`/`5157`; inbound (`%%14592`), TCP (`6`), source `192.168.56.0/24`, destination `192.168.56.20`; `no_log`. |
| `100501` | High-signal correlation | Level 10; `if_matched_sid=100500`; same `sourceAddress`; different `destPort`; `frequency=10`, `timeframe=60`, `ignore=60`. |
| `100502` | Higher-signal correlation | Level 13; same logic; `frequency=14`, `timeframe=60`, `ignore=60`. |

### Technical Meaning of Parameters

- **Level 6 in `100500`:** required to win the sibling-rule comparison in the Security branch. At level 1, official level-5 rule `60104` shadowed the custom base. `60104` remains unchanged as WFP audit telemetry; it is not a port-scan verdict.
- **`frequency`:** the number of historical matches required by correlation within its window; it is not equivalent to a SQL count or unique ports.
- **`timeframe=60`:** 60-second rolling correlation window.
- **`ignore=60`:** after an alert, suppresses new alerts from that rule for 60 seconds. It limits flooding, but does not deduplicate WFP events or guarantee a single alert during long campaigns.
- **`if_matched_sid=100500`:** correlations count the filtered base chain, not any Windows event.
- **`same_field sourceAddress`:** restricts correlation to the same source.
- **`different_field destPort`:** compares the current event port with previous events. It does not build or maintain a set of distinct ports.

### Cardinality Limitation

The real validation observed 34 WFP events for 15 distinct raw destination ports; repetitions had unique `eventRecordID` values. In Wazuh 4.14.7, `different_field` filters history comparisons but does not implement `COUNT(DISTINCT destPort)`. Therefore, `100501` and `100502` are heuristic thresholds for rapid patterns, not claims of exactly 10 or 15 unique ports. `frequency=14` in `100502` is an empirical compensation for sibling-rule interaction and must not be reinterpreted as exact cardinality.

### Evidence and Negative Controls

The real ATTACK/LAB test produced 34 WFP events and one visible alert from each correlation rule (`100501` and `100502`), while the silent base received the remaining applicable events. MANAGEMENT and NAT retained telemetry without feeding these correlations. Filebeat, Indexer, and Dashboard health were checked at validation time, but no authenticated query to `wazuh-alerts-*` or UI search was performed to directly prove final visualization.

## 7. Sysmon EID 3

**Status: AUDITED / PENDING VALIDATION.** This chain is not a validated port-scan detector.

Audited official path:

```text
windows_eventchannel -> 60000 -> 60004 -> 61600 -> 61605 -> sysmon_event3
```

| ID | Documented Function |
|---:|---|
| `100409` | Silent level-1 base: `if_group=sysmon_event3`, TCP, source `192.168.56.0/24`, destination `192.168.56.20`. |
| `100420` | Level-10 correlation: `if_matched_sid=100409`, `frequency=10`, `timeframe=60`, same `sourceIp`, different `destinationPort`. |
| `100421` | Level-13 correlation: `if_matched_sid=100409`, `frequency=15`, `timeframe=60`, same `sourceIp`, different `destinationPort`. |

A real EID 3 was confirmed in MANAGEMENT (`192.168.57.1 -> 192.168.57.20:22`) and in NAT/INTERNET to external services; those cases did not feed `100409`. **There is still no archived evidence of a real ATTACK EID 3 from `192.168.56.1` to `192.168.56.20`.** Without that source event, `100409`, `100420`, and `100421` cannot be validated in the SOC HomeLab.

Outstanding risks: the same heuristic-cardinality limitation; sibling rules that may compete by sharing the base; no `ignore` in the correlations; and possible shadowing by more-specific official Sysmon rules or a local rule targeting port 22. Do not raise levels or redesign this chain by intuition before generating and archiving the authorized ATTACK signal.

## 8. Other Detectors

| Detector | Documented Status | Verified Fact / Gap |
|---|---|---|
| Windows brute force | TELEMETRY OBSERVED / PENDING DETECTION VALIDATION | Security EID `4625` provides failure visibility and official rule `60122` exists; a sanitized export contains historical failures, including three from ATTACK/LAB. For OpenSSH, some events leave `win.eventdata.ipAddress` as `-`, so IP-based correlation is not yet reliable or validated. |
| YARA | PENDING VALIDATION | There is no public sanitized rule, execution/collection configuration, or end-to-end evidence in `archives.json` and `alerts.json`. History is insufficient to claim coverage. |
| FIM / syscheck | CONFIGURED / REVALIDATION PENDING | A historical narrow adjustment exists to reduce noise in a test path while retaining FIM outside it. A sanitized package with configuration, a file change, ingestion evidence, and a final alert is missing. |

## 9. Key Lessons Learned

1. Separating MANAGEMENT, ATTACK/LAB, and NAT reduces false positives without losing useful telemetry.
2. A custom base rule can lose to a higher-level official sibling; validating the real EventChannel path is essential.
3. Standard telemetry (`60104`, for example) and the detection verdict are distinct concepts.
4. `wazuh-logtest` with pasted JSON can use the `json` decoder rather than the `windows_eventchannel` chain; it does not replace a real test.
5. `archives.json` demonstrates ingestion, `alerts.json` alert creation, and an authenticated query/UI demonstrates indexing/visualization.
6. `frequency`, `timeframe`, and `different_field` do not implement exact cardinality of distinct ports.
7. MANAGEMENT and NAT negative tests are part of validation, not an optional detail.
8. The absence of ATTACK EID 3 is an evidence gap, not confirmation that Sysmon or correlation works.

## 10. Known Limitations

- WFP `100501`/`100502` are heuristics and do not count unique ports exactly.
- `ignore=60` reduces repeated alerts, but a campaign lasting more than 60 seconds can generate alerts again.
- Final WFP visualization in Dashboard/Indexer was not directly verified through an authenticated query; only pipeline health and local alert creation were checked.
- Sysmon EID 3 does not have the required source ATTACK signal; its correlations have no throttling and can compete with more-specific rules.
- IP-based brute force in OpenSSH depends on having a real correlatable source field.
- YARA and FIM do not yet have public sanitized end-to-end evidence.

## 11. Important Operating Rules

- Do not mix MANAGEMENT with ATTACK/LAB: only ATTACK/LAB must participate in attack scenarios and the WFP base for this use case.
- NAT retains telemetry for investigation even when excluded from specific detectors.
- Do not assume exact cardinality from `frequency` or `different_field`.
- Validate the SOC HomeLab with real events in `archives.json` and alerts in `alerts.json`.
- Always distinguish `wazuh-logtest` from real EventChannel and the effective decoder/ruleset path.
- Before an authorized rule change: back up, use the `xmllint` wrapper, run `wazuh-analysisd -t`, perform a positive test and MANAGEMENT/NAT negative tests, and inspect evidence.
- Do not publish active Wazuh/Sysmon/YARA copies, transcripts, unreviewed screenshots, keys, passwords, tokens, or environment backups.

## 12. Repository Structure

```text
soc-operations-lab/
├── README.md                         # overview and statuses
├── PROJECT_CONTEXT.md                # this master context
├── configs/                          # sanitized configurations only (no active files yet)
├── detection-rules/                  # WFP, Sysmon, brute force, YARA, and FIM
├── docs/
│   ├── architecture/                 # network and component design
│   ├── operations/                   # validation workflow and inventory
│   ├── setup/                        # partial rebuild material
│   ├── timeline/                     # technical timeline
│   └── troubleshooting/              # WFP and Sysmon incidents
├── evidence/                         # inventory and sanitized/historical artifacts
├── project-notes/                    # lessons, improvements, and limitations
└── scripts/validation/               # publication-safety check
```

Public documentation does not contain active `ossec.conf`, Sysmon, or Wazuh configurations, and private historical artifacts remain outside the repository.

## 13. Current GitHub Status

- Configured remote: `origin` points to GitHub repository `Reynaldo8509/soc-operations-lab`.
- Current local branch: `main`.
- Observed local HEAD: `89502f8023c95290c95ae144985062b584aa711f` (`Auto sync: 2026-04-30 20:06:20`). The remote was not queried during this consolidation, so the current relationship between `main` and `origin/main` was not verified.
- The working tree already contained modifications, deletions, and untracked files before this context was created. They are user/project changes and must be preserved.
- This task did not run `git add`, `git commit`, or `git push`.

## 14. Completed Work

- Documented three-network architecture and its operating boundaries.
- Wazuh Manager 4.14.7 with Windows EventChannel reception in the SOC HomeLab.
- WFP detector `100500`/`100501`/`100502` validated with real ATTACK/LAB events, MANAGEMENT/NAT negative controls, and `archives.json`/`alerts.json` evidence.
- Documentation of cardinality limitation, rule priority, and WFP throttling.
- Audit of the official Sysmon EID 3 path and MANAGEMENT/NAT negative exclusions.
- Documentation structure, publication policy, and static secret-pattern check in the repository.

## 15. Pending Work

1. Generate an authorized Sysmon EID 3 ATTACK event `192.168.56.1 -> 192.168.56.20`; then confirm the final path, winning rules, alert repetition, and MANAGEMENT/NAT negatives.
2. Verify WFP indexing/visualization through an authenticated query to `wazuh-alerts-*` and/or a Dashboard search before claiming UI visibility.
3. Validate brute force with an authorized scenario and a genuinely usable source-IP field; document the alert and negative test.
4. Prepare a YARA rule with provenance/license, execution procedure, and sanitized ingestion, alert, and negative evidence.
5. Revalidate FIM with a controlled change, confirming that the limited exclusion does not hide paths outside its scope.
6. Publish reproducible configurations only after sanitization and review; replace or remove empty brute-force placeholders with authorization.
7. If exact distinct-port counting is required, design and validate stateful normalization outside the native rules engine.

## 16. What Must Not Change Without a New Technical Decision

- MANAGEMENT, ATTACK/LAB, and NAT boundaries and addressing.
- `100500`, `100501`, and `100502`, including level 6, ATTACK/LAB filters, thresholds, and `ignore=60`, without new real-event evidence and negative tests.
- Official Wazuh rules, Windows Firewall, and any active Wazuh/Sysmon configuration, including `ossec.conf`, except within explicitly authorized scope.
- MANAGEMENT or NAT telemetry through global suppression to reduce noise.
- Classification of Sysmon EID 3 as "validated" before capturing the required real ATTACK event.
- The claim that WFP counts unique ports exactly or that Dashboard displays alerts without direct proof.
- Publication of keys, secrets, active configurations, backups, full transcripts, or screenshots without sensitivity review.
