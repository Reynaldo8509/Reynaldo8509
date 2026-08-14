# Sysmon Network / Event ID 3

> **Status: AUDITED / PENDING VALIDATION**

This page documents an audit of the Sysmon EID 3 chain. It does not claim an operational port-scan detector.

## Observed Official Path

```text
windows_eventchannel
  -> 60000
     -> 60004  (Microsoft-Windows-Sysmon/Operational)
        -> 61600  (INFORMATION)
           -> 61605  (Event ID 3, group sysmon_event3)
```

## Audited Custom Rules

```text
100409  level 1, if_group sysmon_event3, TCP,
        sourceIp 192.168.56.0/24, destinationIp 192.168.56.20, no_log

100420  level 10, frequency 10 / timeframe 60,
        if_matched_sid 100409, same sourceIp, different destinationPort

100421  level 13, frequency 15 / timeframe 60,
        if_matched_sid 100409, same sourceIp, different destinationPort
```

`100409` is correctly anchored to `sysmon_event3` and is silent by design. It is eligible only for TCP from ATTACK/LAB to the ATTACK/LAB Windows endpoint.

## Audit Evidence

| Context | Result |
|---|---|
| MANAGEMENT | A real EID 3 was confirmed for `192.168.57.1 -> 192.168.57.20:22`; the telemetry did not feed `100409`. |
| NAT/INTERNET | A real EID 3 was confirmed from `10.0.2.15` to external services; it did not feed `100409`. |
| ATTACK/LAB | No real EID 3 `192.168.56.1 -> 192.168.56.20` was found in the reviewed archive. |

The missing ATTACK signal is the primary gap: without a real source event, it is not possible to validate that `100409`, `100420`, or `100421` work in the SOC HomeLab.

## Identified Technical Risks

1. **Heuristic cardinality.** `frequency`, `timeframe`, and `different_field` are not native `COUNT(DISTINCT destinationPort)`. The same limitation documented for WFP applies to this chain's correlation engine.
2. **Sibling frequency rules.** `100420` and `100421` share `if_matched_sid=100409`; they may compete for events in the same window.
3. **No throttling.** No correlation rule has `ignore="60"`, so a flow that does correlate could repeat alerts.
4. **Potential shadowing.** More-specific official rules `92104`, `92105`, `92107`, and `92110`, and local level-12 rule `100004` for `192.168.56.1 -> :22`, may win for event subsets. This is a structural consideration; it was not demonstrated with a real ATTACK EID 3.

## Current Decision

WFP remains the validated source for blocked-port scans. Before changing the Sysmon chain, a future controlled test must produce and archive a real ATTACK EID 3. The final rule path, potential competition with official rules, alert repetition, and MANAGEMENT/NAT negative tests must then be verified.

Do not raise the level of `100409` by intuition: it could shadow more-specific official rules.
