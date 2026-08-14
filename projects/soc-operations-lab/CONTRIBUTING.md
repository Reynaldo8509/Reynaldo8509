# Contribute Safely

This SOC HomeLab documents real configurations and tests. Before proposing a change:

1. Preserve the MANAGEMENT, ATTACK/LAB, and NAT boundaries.
2. Do not claim a validated detection without real events and a relevant negative test.
3. Validate Wazuh rules with `wazuh-analysisd -t` before restarting a service.
4. Distinguish ingestion (`archives.json`), alert creation (`alerts.json`), and indexing/visualization.
5. Do not add secrets, private keys, environment backups, full transcripts, or unreviewed screenshots.

Detection improvements must explain their evidence, expected false positives, limitations, and rollback plan. Do not make automatic commits or pushes from validation procedures.
