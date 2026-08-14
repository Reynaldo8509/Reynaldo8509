# Sysmon Event ID 3: Validation Gap

## Problem

A custom chain was configured to correlate Event ID 3 from ATTACK/LAB to Windows, but the reviewed archive does not contain a real event from that flow.

## Evidence

- MANAGEMENT and NAT did generate real EID 3 events.
- The official path `60000 -> 60004 -> 61600 -> 61605` was confirmed.
- No real EID 3 `192.168.56.1 -> 192.168.56.20` appeared during the review.

## Root cause / current limit

The detector does not have a real ATTACK signal to correlate. It has not been demonstrated whether the absence stems from blocked-connection semantics, additional Sysmon filters, or both factors.

## Solution status

No correction was applied. The next phase must generate an authorized ATTACK event and first verify the real rule path. Raising levels or copying the WFP design without this evidence could shadow more-specific official Sysmon rules.

## Lesson learned

The fact that Sysmon is enabled does not demonstrate that it emits the signal required for a specific use case. See the [audit report](../../detection-rules/sysmon-network.md).
