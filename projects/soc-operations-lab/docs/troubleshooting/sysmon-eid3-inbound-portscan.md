# Sysmon Event ID 3: inbound port-scan decision

## Finding

During the controlled ATTACK/LAB TCP SYN scan, the endpoint did not emit
Sysmon Event ID 3 records whose `sourceIp` was `192.168.56.1`, whose
`destinationIp` was `192.168.56.20`, and whose destination ports matched the
scan. Other Sysmon EID 3 records were present, which proves collection was
working but does not satisfy the inbound port-scan use case.

## Validation performed

1. Confirmed that generic Sysmon EID 3 telemetry reached Wazuh archives.
2. Tested a narrow, temporary Sysmon `NetworkConnect` inclusion for the
   ATTACK/LAB source range.
3. Repeated a controlled SYN scan to the endpoint.
4. Observed no qualifying EID 3 records and restored the timestamped Sysmon
   configuration backup.

## Decision

Do not deploy a Sysmon EID 3 correlation rule for inbound port scans on this
endpoint. A correlation rule without matching base telemetry would create an
unverifiable control.

Use Windows Filtering Platform Security events 5152/5157 as the authoritative
source for this inbound scenario. A subsequent TCP Connect test confirmed that
Sysmon EID 3 can enrich the case for a completed inbound connection (22/TCP,
`initiated:false`), but it does not represent the filtered scan ports.

Sysmon is therefore retained as contextual confirmation of successful inbound
connections, not combined with the WFP port-scan correlation. It may also
support separate, validated outbound-connection use cases.
