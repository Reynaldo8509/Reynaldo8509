# Detection: Controlled ATTACK/LAB port scan

## Summary

On 2026-08-16, a controlled TCP SYN scan ran from the isolated ATTACK/LAB
source `192.168.56.1` against the Windows endpoint `192.168.56.20`. The scan
tested 15 TCP ports at a moderate rate. The endpoint was reachable and exposed
TCP/5985 (WinRM); the remaining tested ports were filtered.

This is an evidence-generating lab exercise, not a finding against a production
asset. The current run generated the expected network activity and the manager
emitted one alert for each configured WFP correlation threshold.

## MITRE ATT&CK

- **T1046 – Network Service Discovery.** The controlled scan enumerates the
  network exposure of the endpoint.

## Evidence

- **Source / target:** `192.168.56.1` → `192.168.56.20` (ATTACK/LAB only).
- **Command profile:** TCP SYN scan, 15 selected ports, `-T3`,
  `--min-rate 100`, and one retry. The complete command and output are retained
  in the run artifacts, not repeated here as an attack recipe.
- **Network result:** `5985/tcp` was open; ports `20,21,23,25,53,80,110,143,
  161,389,443,636,993,995` were filtered.
- **Expected Windows telemetry:** Windows Filtering Platform Security events
  **5152** and/or **5157**, shipped through Windows EventChannel.
- **Expected Wazuh rule path:** `60001` → `100500` (silent tracking) →
  `100501` and/or `100502` (correlation heuristic). The active custom rules
  limit eligibility to `192.168.56.0/24` targeting `192.168.56.20`; MANAGEMENT
  and NAT telemetry remain out of scope.
- **Observed Wazuh results:** Windows Security Event ID **5152** matched
  `100501` (level 10) at `2026-08-16T23:42:43.831+0000` and `100502` (level
  13) at `2026-08-16T23:42:43.928+0000`; both alerts reported
  `firedtimes: 1`. The sanitized alert fields are preserved in
  [`wazuh-alerts-sanitized.jsonl`](../evidence/scenario-2-port-scan-20260816T234238Z/wazuh-alerts-sanitized.jsonl).
- **Current-run evidence:**
  [`metadata.txt`](../evidence/scenario-2-port-scan-20260816T234238Z/metadata.txt),
  [`nmap-15-ports.txt`](../evidence/scenario-2-port-scan-20260816T234238Z/nmap-15-ports.txt),
  and [`nmap-15-ports.xml`](../evidence/scenario-2-port-scan-20260816T234238Z/nmap-15-ports.xml).
- **Historical validation:** the prior controlled 15-port case is documented
  in [WFP Port Scan Detection](../detection-rules/WFP_PortScan_Detection_Final.md).
  It produced 34 WFP records and one local alert for each correlation rule.
- **Latest validation:** a controlled scan of TCP ports 1–20, all filtered by
  the endpoint, produced 20 unique WFP destination ports. Wazuh emitted
  `100501` at the 10th port and `100502` at the 15th. Sanitized artifacts are
  in [`scenario-2-port-scan-20260817T010730Z`](../evidence/scenario-2-port-scan-20260817T010730Z/).
- **Cross-source enrichment:** a later TCP Connect scan of ports 1–100
  generated WFP correlation alerts for the filtered ports and two Sysmon EID 3
  records for the completed inbound connection to 22/TCP. The source, target,
  timestamps, and field values are preserved in
  [`scenario-2-port-scan-20260817T014652Z`](../evidence/scenario-2-port-scan-20260817T014652Z/).

## Timeline

| UTC time | Event | Evidence / correlation |
|---|---|---|
| 2026-08-16 23:42:38 | Controlled scan began | `metadata.txt`; source interface `vboxnet0` (`192.168.56.1`). |
| 2026-08-16 23:42:43 | Scan completed | Nmap found the target up; TCP/5985 open and 14 selected ports filtered. |
| 2026-08-16 23:42:43.831 | Correlation alert | Wazuh `100501`, level 10, Windows Security 5152, source `192.168.56.1`, destination port `25`. |
| 2026-08-16 23:42:43.928 | High-confidence correlation alert | Wazuh `100502`, level 13, Windows Security 5152, source `192.168.56.1`, destination port `636`. |
| 2026-08-16 23:42:54 | Manager health confirmed | `wazuh-manager` was active; a privileged, read-only query exported the sanitized alert fields. |
| 2026-08-17 01:07:30 | Repeatable WFP validation | A TCP 1–20 scan generated `100501` at destination port 6 and `100502` at port 17; both used the same ATTACK/LAB source and endpoint target. |
| 2026-08-17 01:46:52.057 | WFP correlation alert | TCP Connect scan of ports 1–100 triggered `100501`; WFP Event ID 5152 identified source `192.168.56.1`, target `.20`, and the triggering destination port 78. |
| 2026-08-17 01:46:53.955 | High-confidence WFP alert | The same source-target sequence triggered `100502` at destination port 90. |
| 2026-08-17 01:46:56.808–.839 | Sysmon enrichment | Sysmon EID 3 recorded two completed inbound TCP connections from `.1` to `.20:22` with `initiated:false`. |

## Analysis

The source, target, scope, and cadence match an authorized reconnaissance
simulation. In a SOC queue, the same pattern against a non-lab endpoint would
be suspicious because it enumerates multiple services in seconds and reaches a
remote-management listener.

The current Wazuh implementation is intentionally a throttled correlation
control. This repeatable validation showed the desired 10- and 15-port alert
points when the input was one blocked WFP event per selected port. Repeated
WFP records can still affect correlation timing in other traffic patterns, so
the rules remain triage signals rather than a general-purpose persistent set
counter. See the forensic reconstruction in the linked historical case study.

Sysmon Event ID 3 enriches this case but is not the port-scan detector. A TCP
Connect scan produced EID 3 only for the successful connection to the exposed
SSH service (22/TCP); the 99 filtered ports did not complete connections and
did not produce the required variety of EID 3 destination ports. Consequently,
WFP remains the primary detection source, while Sysmon confirms the successful
connection that may warrant follow-up investigation. The documented boundary
is in [Sysmon EID 3 inbound port-scan decision](../docs/troubleshooting/sysmon-eid3-inbound-portscan.md).

## Risk Level

**Medium** in a production context: the activity is reconnaissance, and the
open WinRM service increases the value of follow-on credential or remote-access
monitoring. **Informational / authorized** in this HomeLab run.

## Recommendations

1. Give the SOC collection role read-only access to the sanitized Wazuh alert
   export (or provide a controlled dashboard query) so that future exercises
   can be confirmed without temporary privileged collection.
2. During triage, correlate Windows Security 5152/5157 with Sysmon Event ID 3
   using source, destination, port, and a narrow UTC window. Keep WFP as the
   detection trigger; treat EID 3 as confirmation of completed connections.
3. Treat `100501`/`100502` as triage signals. For a requirement of exact
   distinct-port cardinality, use the documented external stateful aggregator
   design rather than relying on `different_field`.
4. Review WinRM exposure and enforce least-privilege remote-management policy;
   retain the ATTACK/LAB exclusion boundaries for MANAGEMENT and NAT traffic.
