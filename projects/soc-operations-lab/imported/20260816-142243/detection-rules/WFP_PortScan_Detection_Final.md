# Wazuh WFP Port Scan Detection

## 1. Lab architecture

| Network | CIDR | Kali | Wazuh Manager (Ubuntu) | Windows 11 endpoint | Purpose |
|---|---|---|---|---|---|
| MANAGEMENT | `192.168.57.0/24` | `192.168.57.1` | `192.168.57.10` | `192.168.57.20` | SSH, SCP/SFTP, WinRM and administration |
| ATTACK/LAB | `192.168.56.0/24` | `192.168.56.1` | `192.168.56.10` | `192.168.56.20` | Controlled reconnaissance and detection tests |
| NAT/INTERNET | `10.0.2.0/24` | n/a | `10.0.2.3` | `10.0.2.15` | Updates and external connectivity |

Only inbound TCP Windows Firewall events from `192.168.56.0/24` to
`192.168.56.20` are eligible for this detector. MANAGEMENT and NAT telemetry is
retained but is deliberately outside its base rule.

## 2. Problem

The original objective was to detect a controlled TCP port scan against the
Windows endpoint using Windows Filtering Platform (WFP) events `5152` and
`5157`, while excluding normal administration and NAT traffic. Initial rules
either did not receive live Windows EventChannel events or produced repeated
alerts for one scan.

## 3. Root cause #1: rule priority on the Windows EventChannel branch

Live Windows Security events follow this branch:

```text
windows_eventchannel
  -> 60000
     -> 60001 (Security channel)
        -> 60104 (AUDIT_FAILURE, level 5)
        -> 100500 (custom WFP base)
```

With `100500` at level 1, sibling rule `60104` was selected first and the custom
base did not receive the live WFP event. A reversible production test proved
that `100500` at level 6 wins this sibling comparison and receives the event.
This is why the final base rule is level 6. Rule `60104` remains unmodified: it
is standard WFP audit-failure telemetry, not a port-scan verdict.

## 4. Root cause #2: one Nmap scan creates repeated WFP records per port

The final controlled scan targeted 15 filtered TCP ports. WFP produced 34
records, not 15:

- `5152`: 30 events.
- `5157`: 4 events.
- Destination ports: 15 distinct values.
- Every Windows `eventRecordID` was unique.
- Thirteen ports had two `5152` events. Ports `443` and `5985` had two `5152`
  plus two `5157` events each.

Therefore `eventRecordID` cannot deduplicate logical ports: the repeated WFP
records have distinct record IDs.

## 5. Final WFP architecture

```text
Windows EventChannel
  -> 60000
     -> 60001
        -> 100500  (WFP ATTACK/LAB tracking base; no_log)
           -> 100501  (level 10 correlation)
           -> 100502  (level 13 correlation)
```

The rules are custom rules in `/var/ossec/etc/rules/local_rules.xml` on Wazuh
4.14.7. The official ruleset and Windows Firewall configuration are unchanged.

## 6. Final rules

```xml
<rule id="100500" level="6">
  <if_sid>60001</if_sid>
  <field name="win.system.channel">^Security$</field>
  <field name="win.system.eventID">^5152$|^5157$</field>
  <field name="win.eventdata.direction">^%%14592$</field>
  <field name="win.eventdata.protocol">^6$</field>
  <field name="win.eventdata.sourceAddress">^192\.168\.56\.</field>
  <field name="win.eventdata.destAddress">^192\.168\.56\.20$</field>
  <options>no_log</options>
</rule>

<rule id="100501" level="10" frequency="10" timeframe="60" ignore="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>win.eventdata.sourceAddress</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>

<rule id="100502" level="13" frequency="14" timeframe="60" ignore="60">
  <if_matched_sid>100500</if_matched_sid>
  <same_field>win.eventdata.sourceAddress</same_field>
  <different_field>win.eventdata.destPort</different_field>
</rule>
```

`frequency="14"` on `100502` is an established compensation for an event
consumed by the level-10 sibling during the earlier correlation design. It must
not be interpreted as a count-distinct-ports primitive.

## 7. Cardinality analysis of the real scan

The scan ran from `2026-08-14T00:14:22Z` to approximately
`2026-08-14T00:14:32Z` using:

```bash
nmap -Pn -sT -p 20,21,23,25,53,80,110,143,161,389,443,636,993,995,5985 192.168.56.20
```

The following is the complete chronological sequence selected from
`archives.json` for source `192.168.56.1`, destination `192.168.56.20`, and
Event IDs `5152`/`5157`. `unique` is a separate forensic count of distinct raw
`destinationPort` values observed through that event; it is not Wazuh's internal
correlation counter.

| # | UTC timestamp | Event ID | Port | EventRecordID | unique | Final rule |
|---:|---|---:|---:|---:|---:|---:|
| 1 | 00:14:28.077 | 5152 | 53 | 670300 | 1 | 100500 |
| 2 | 00:14:28.080 | 5152 | 143 | 670301 | 2 | 100500 |
| 3 | 00:14:28.081 | 5152 | 25 | 670302 | 3 | 100500 |
| 4 | 00:14:28.083 | 5152 | 443 | 670303 | 4 | 100500 |
| 5 | 00:14:28.086 | 5157 | 443 | 670304 | 4 | 100500 |
| 6 | 00:14:28.088 | 5152 | 80 | 670305 | 5 | 100500 |
| 7 | 00:14:28.089 | 5152 | 995 | 670306 | 6 | 100500 |
| 8 | 00:14:28.090 | 5152 | 21 | 670307 | 7 | 100500 |
| 9 | 00:14:28.092 | 5152 | 23 | 670308 | 8 | 100500 |
| 10 | 00:14:28.093 | 5152 | 993 | 670309 | **9** | **100501** |
| 11 | 00:14:28.102 | 5152 | 110 | 670310 | 10 | 100500 |
| 12 | 00:14:29.457 | 5152 | 110 | 670324 | 10 | 100500 |
| 13 | 00:14:29.472 | 5152 | 993 | 670325 | 10 | 100500 |
| 14 | 00:14:29.489 | 5152 | 23 | 670326 | 10 | 100500 |
| 15 | 00:14:29.504 | 5152 | 21 | 670327 | 10 | 100500 |
| 16 | 00:14:29.520 | 5152 | 995 | 670328 | **10** | **100502** |
| 17 | 00:14:29.536 | 5152 | 80 | 670329 | 10 | 100500 |
| 18 | 00:14:29.551 | 5152 | 443 | 670330 | 10 | 100500 |
| 19 | 00:14:29.567 | 5157 | 443 | 670331 | 10 | 100500 |
| 20 | 00:14:29.582 | 5152 | 25 | 670332 | 10 | 100500 |
| 21 | 00:14:29.598 | 5152 | 143 | 670333 | 10 | 100500 |
| 22 | 00:14:29.641 | 5152 | 53 | 670334 | 10 | 100500 |
| 23 | 00:14:31.070 | 5152 | 20 | 670335 | 11 | 100500 |
| 24 | 00:14:31.073 | 5152 | 5985 | 670336 | 12 | 100500 |
| 25 | 00:14:31.076 | 5157 | 5985 | 670337 | 12 | 100500 |
| 26 | 00:14:31.078 | 5152 | 161 | 670338 | 13 | 100500 |
| 27 | 00:14:31.080 | 5152 | 389 | 670339 | 14 | 100500 |
| 28 | 00:14:31.081 | 5152 | 636 | 670340 | **15** | 100500 |
| 29 | 00:14:32.071 | 5152 | 636 | 670341 | 15 | 100500 |
| 30 | 00:14:32.074 | 5152 | 389 | 670342 | 15 | 100500 |
| 31 | 00:14:32.076 | 5152 | 161 | 670343 | 15 | 100500 |
| 32 | 00:14:32.079 | 5152 | 5985 | 670344 | 15 | 100500 |
| 33 | 00:14:32.082 | 5157 | 5985 | 670345 | 15 | 100500 |
| 34 | 00:14:32.086 | 5152 | 20 | 670346 | 15 | 100500 |

The first raw count of 10 distinct ports is event 11. The first raw count of
15 is event 28. Nevertheless, the level-10 alert occurred at event 10 with nine
raw distinct ports, and the level-13 alert occurred at event 16 with ten. This
is direct evidence that these rules do **not** implement exact cardinality.

Per-port distribution:

| Ports | WFP pattern | Repetition interval |
|---|---|---|
| 20, 21, 23, 25, 53, 80, 110, 143, 161, 389, 636, 993, 995 | 2 × 5152 each | 990–1,564 ms |
| 443 | 2 × 5152 and 2 × 5157 | 3 ms, 1,465 ms, 16 ms |
| 5985 | 2 × 5152 and 2 × 5157 | 3 ms, 1,003 ms, 3 ms |

## 8. What the correlations actually mean

Wazuh documents `different_field` as requiring the current field value to
differ from values in previous matching events. In the Wazuh 4.14.7 source,
`Search_LastSids()` iterates earlier `100500` events. It rejects a prior event
only if its `destPort` equals the *current* event's port, then counts every other
prior event. It does not construct or persist a set of unique ports across the
window. Thus two previous records for port 443 can both contribute when the
current port is 993.

Consequently:

- `100501` means: a rapid WFP pattern with enough prior base events from the
  same source whose ports differ from the current port.
- `100502` means the analogous, higher-frequency pattern.
- They are useful high-signal **heuristic** port-scan alerts, not proof of
  exactly 10 or exactly 15 unique destination ports.

`ignore="60"` starts when a rule triggers and suppresses that rule for 60
seconds. It solved the alert flood in the observed scan: 32 archived events
ended at `100500`, with exactly one `100501` and one `100502`, each
`firedtimes: 1`. It does not deduplicate WFP records or turn the counter into a
unique-port set.

## 9. Large scans

For a fast scan such as `1-100` or `100-1000` that completes within 60 seconds,
each correlation rule can emit at most one visible alert after it triggers,
because of `ignore="60"`. The exact event and raw unique-port count at which it
triggers depend on WFP repetition and ordering, so they must not be predicted
as exactly 10 and 15.

For a scan lasting more than 60 seconds, a rule becomes eligible again after its
ignore interval. Because the correlation timeframe is also 60 seconds, a
continuous qualifying stream can produce roughly one alert per rule per
60-second ignore interval, potentially immediately after re-enablement if the
rolling history still qualifies. This is throttling, not a once-per-attacker
or once-per-scan guarantee.

## 10. False-positive controls

The base rule's narrow filters are the control:

- MANAGEMENT (`192.168.57.0/24`) is excluded. A legitimate
  `192.168.57.1 -> 192.168.57.20:22` session still produced Sysmon Event ID 3,
  while `100501` and `100502` remained zero.
- NAT traffic remains archived, including Windows audit-failure telemetry to
  `10.0.2.15`, while `100501` and `100502` remained zero.
- ATTACK/LAB traffic from `192.168.56.1` to `192.168.56.20` is the only tested
  path eligible for this WFP detector.

No normal telemetry was globally silenced.

## 11. Validation evidence

The permanent rules were checked with a temporary `<ruleset>` wrapper for
`xmllint`, because `local_rules.xml` intentionally contains multiple top-level
`<group>` fragments. The real file was validated by:

```bash
/var/ossec/bin/wazuh-analysisd -t
systemctl is-active wazuh-manager
```

Both passed at the time of deployment, and the manager was active. The controlled
scan yielded 34 WFP events / 15 raw ports, `100500=32`, `100501=1`,
`100502=1`, and `60104=0` for the scan. `alerts.json` therefore proves alert
creation; `archives.json` proves event ingestion.

Filebeat, Wazuh Indexer, and Wazuh Dashboard services were active, and
`filebeat test output` established its TLS connection to the Indexer. An
authenticated document query of `wazuh-alerts-*` and a Dashboard UI search were
not performed in this validation, so alert indexing/display must be treated as
**service-health checked, not directly verified**.

Useful forensic commands:

```bash
# Validate the fragment without changing it
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t

# Select WFP events for the scan; archive timestamps are UTC
jq -c 'select(.data.win.eventdata.sourceAddress == "192.168.56.1" and .data.win.eventdata.destAddress == "192.168.56.20" and (.data.win.system.eventID == "5152" or .data.win.system.eventID == "5157"))' /var/ossec/logs/archives/archives.json

# Inspect visible correlation alerts
jq -c 'select(.rule.id == "100501" or .rule.id == "100502")' /var/ossec/logs/alerts/alerts.json
```

## 12. Before versus after

| Aspect | Before final stabilization | After level 6 and `ignore=60` |
|---|---|---|
| Live WFP base path | `60104` eclipsed level-1 custom base | `100500` receives real WFP events |
| Visible scan alerts | Repeated threshold alerts | One level-10 and one level-13 alert in the observed scan |
| NAT / MANAGEMENT | Must remain visible but not scans | Telemetry retained; no `100501` / `100502` |
| Cardinality claim | Assumed exact unique-port threshold | Proven heuristic, not exact count-distinct |

## 13. Limitations and options considered

There is no native Wazuh 4.14.7 rule option in this ruleset engine that keeps a
deduplicated, source/destination/window-scoped set and returns `COUNT(DISTINCT
win.eventdata.destPort)`. `same_field`, `different_field`, `if_matched_sid`,
and `if_matched_group` are correlation filters over matching event history, not
a general aggregation engine.

Alternatives were assessed but not implemented:

1. **Filter only Event ID 5152.** This removes the four `5157` records in this
   sample but leaves the repeated `5152` events for every port, so exact
   cardinality is still not guaranteed.
2. **Use EventRecordID.** Not useful for deduplication here because all 34 IDs
   are unique.
3. **Use a custom decoder or intermediate rule.** A decoder is stateless and a
   normal Wazuh intermediate rule retains the same correlation behavior.
4. **Use Sysmon Event ID 3.** It is an independent telemetry source and may be
   evaluated separately, but it was intentionally not changed as part of this
   WFP detector.
5. **External stateful normalization.** A dedicated integration storing a key
   such as `(sourceAddress, destAddress, destPort, rolling window)` could make
   exact `COUNT(DISTINCT)` semantics possible. It adds state, failure handling,
   and operational complexity and is outside the final WFP rules-only scope.

The current XML also produces the observed composite group string
`portscanreconnaissance` from nested group composition. It does not affect the
matching or false-positive filters and was not changed in this scope; searches
should use `rule.id` or the explicit inner groups where appropriate.

## 14. GitHub evidence checklist

When reproducing or extending this work:

1. Preserve the three-network boundaries and test only the ATTACK/LAB target.
2. Validate XML fragments with a wrapper and validate the real ruleset with
   `wazuh-analysisd -t`.
3. Use `archives.json` to calculate raw WFP cardinality independently of alert
   results.
4. Use `alerts.json` to establish rule creation.
5. Query the Indexer or Dashboard with authenticated access before claiming UI
   visibility.
6. Retest both negative paths: NAT and legitimate MANAGEMENT SSH/Sysmon.
7. Treat numeric WFP correlation levels as tuned heuristics unless a stateful
   distinct-count implementation is introduced and independently verified.

## 15. Final conclusion

The WFP detector is **production-ready for this HomeLab as a throttled,
high-signal heuristic**: it receives real WFP events, preserves NAT and
MANAGEMENT telemetry, and limits the observed 15-port scan to one level-10 and
one level-13 alert.

It is **not** an exact `10/15 unique destination ports` detector. The real
34-event forensic sequence proves that Wazuh 4.14.7 correlation with
`different_field` can alert before those raw unique-port counts are reached.
Any public documentation or dashboard label must describe `100501` and `100502`
as heuristic confidence thresholds until a separately designed stateful
normalization/count-distinct solution is deployed and validated.
