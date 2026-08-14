# 07 — SSH Management

Management tasks use the MANAGEMENT Network. Public material does not contain SSH aliases, private keys, `known_hosts` files, or local user configurations.

Documented Practices:

- Use key authentication and `IdentitiesOnly` where applicable.
- Keep keys outside the repository.
- Confirm that a management connection generates telemetry without feeding detectors designed for ATTACK/LAB.
- Transfer configurations through management channels, never through the attack-simulation network.
