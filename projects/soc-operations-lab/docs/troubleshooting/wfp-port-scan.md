# WFP Port Scan Detection

## Problem

WFP events `5152`/`5157` reached the manager, but initially the custom rule did not receive the real events. After correcting the path, a single scan generated repeated alerts.

## Evidence

- Windows Security EventChannel followed `60000 -> 60001`.
- `60104` (AUDIT_FAILURE) was a level-5 sibling.
- A scan of 15 filtered ports produced 34 WFP events and 15 distinct raw destination ports.

## Root cause

1. Level-1 base `100500` was shadowed by level-5 `60104`.
2. WFP generated multiple records per port, and Wazuh correlation does not maintain an exact set of unique ports.

## Solution

- Base `100500`: level 6, `if_sid=60001`, ATTACK/LAB filters, and `no_log`.
- Correlations `100501` and `100502`: `ignore=60` throttling.
- `100502` threshold `frequency=14` is an observed compensation for sibling frequency-rule interaction; it is not exact cardinality.

## Validation

The real test produced one `100501` alert and one `100502` alert without feeding the detector from NAT or MANAGEMENT. WFP telemetry remained available in archives.

## Lesson learned

Validate against the real EventChannel and separate telemetry (`60104`) from the detection verdict. For forensic detail and limitations, see the [validated WFP rule](../../detection-rules/WFP_PortScan_Detection_Final.md).
