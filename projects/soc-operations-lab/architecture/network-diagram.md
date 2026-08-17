# Home SOC Lab network diagram

```text
                         MANAGEMENT — 192.168.57.0/24

 Kali .1  ---------------- SSH / administration ---------------- Wazuh .10
     |                                                              |
     +---------------------- Windows endpoint .20 -----------------+

                           ATTACK/LAB — 192.168.56.0/24

 Kali .1  ---------------- controlled telemetry ---------------- Windows .20
     |                                                              |
     +------------------------- Wazuh .10 -------------------------+

                               NAT — 10.0.2.0/24
                         Manager .3 / Endpoint .15
```

The ATTACK/LAB plane is the only source range eligible for the WFP port-scan
base rule. Management traffic supports administration and NAT supports normal
connectivity; both remain available as telemetry but are excluded from this
specific detector. This separation lets the case studies test detection logic
without turning normal administration into port-scan alerts.
