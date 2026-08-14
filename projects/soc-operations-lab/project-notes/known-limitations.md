# Known limitations

## WFP Port Scan

- `100501` and `100502` are high-signal heuristic thresholds; they do not count unique ports exactly.
- `ignore=60` limits repeated alerts, but does not guarantee a single alert per attacker throughout a long campaign.
- Final Dashboard visibility was not tested through an authenticated query to the index during the documented validation; pipeline health was checked.

## Sysmon Network

- Real ATTACK EID 3 evidence from Kali to Windows is missing.
- Existing correlations have no throttling and share a base, creating cardinality and competition risks.
- More-specific official rules can shadow event subsets.

## Other Detectors

- IP-based brute force for OpenSSH requires reliable source fields.
- YARA does not have a selected publishable validation package.
- FIM requires end-to-end revalidation with sanitized evidence.
