# Sysmon Network / Event ID 3

> **Status: PARTIALLY VALIDATED — direct ATTACK/LAB EID 3; replay-validated multi-port threshold**

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
| ATTACK/LAB | A controlled TCP connection `192.168.56.1 -> 192.168.56.20:22` generated a real EID 3 and matched direct rule `100004`. A 15-port Sysmon fixture reached `100420` at the tenth port in `wazuh-logtest`; that threshold was not claimed as a live 10-connection result. |

The ATTACK source signal is now demonstrated for the scoped direct rule `100004`. The reusable base `100409` and correlation `100420` have replay coverage, but a live multi-port Sysmon sequence has not been demonstrated; this remains the primary validation gap.

## Identified Technical Risks

1. **Heuristic cardinality.** `frequency`, `timeframe`, and `different_field` are not native `COUNT(DISTINCT destinationPort)`. The same limitation documented for WFP applies to this chain's correlation engine.
2. **Sibling frequency rules.** `100420` and `100421` share `if_matched_sid=100409`; they may compete for events in the same window.
3. **No throttling.** No correlation rule has `ignore="60"`, so a flow that does correlate could repeat alerts.
4. **Potential shadowing.** More-specific official rules `92104`, `92105`, `92107`, and `92110`, and local level-12 rule `100004` for `192.168.56.1 -> :22`, may win for event subsets. The direct `100004` path was demonstrated with a real ATTACK EID 3; broader correlation competition remains a structural consideration.

## Current Decision

WFP remains the validated source for blocked-port scans. Sysmon now has a real scoped ATTACK/LAB EID 3 validation through `100004`; before claiming a live multi-port Sysmon detector, run and archive a controlled multi-port connection test. Preserve the existing MANAGEMENT/NAT exclusions and verify rule competition and alert repetition in that run. Supporting evidence is in [the cardinality run report](../evidence/cardinality/run-20260815-205438/cardinality_report.md).

Do not raise the level of `100409` by intuition: it could shadow more-specific official rules.
