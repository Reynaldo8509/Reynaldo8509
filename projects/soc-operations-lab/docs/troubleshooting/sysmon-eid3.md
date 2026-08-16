# Sysmon Event ID 3: Updated Validation Boundary

## Problem

A custom chain was configured to correlate Event ID 3 from ATTACK/LAB to Windows. The historical archive lacked a real event from that flow; a later controlled TCP connection supplied one scoped validation case.

## Evidence

- MANAGEMENT and NAT did generate real EID 3 events.
- The official path `60000 -> 60004 -> 61600 -> 61605` was confirmed.
- The original archive did not contain a real EID 3 `192.168.56.1 -> 192.168.56.20`.
- A later authorized TCP connection from ATTACK/LAB to `:22` generated a real EID 3 and matched direct rule `100004`.
- A reproducible 15-port Sysmon fixture reached correlation `100420` at port 10; it is replay evidence, not proof of a live 10-connection sequence.

## Root cause / current limit

The direct scoped detector now has a real ATTACK signal. The remaining limit is correlation coverage: it has not been demonstrated whether a live multi-port sequence will follow the same path as the fixture, especially where more-specific rules can win.

## Solution status

The minimal correction to the `100409` scope was validated before the later run. The direct `100004` path is now demonstrated; a future phase must run an authorized multi-port TCP connection sequence and verify the final rule path before claiming live cardinality detection. Raising levels or copying the WFP design without that evidence could shadow more-specific official Sysmon rules.

## Lesson learned

The fact that Sysmon is enabled does not demonstrate that it emits the signal required for every use case. A direct EID 3 result and a replayed correlation threshold are different evidence levels. See the [audit report](../../detection-rules/sysmon-network.md) and [run report](../../evidence/cardinality/run-20260815-205438/cardinality_report.md).
