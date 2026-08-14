# 02 — Ubuntu and Wazuh Manager

## Verified Status

- Wazuh Manager: `4.14.7`.
- Role: Windows EventChannel telemetry reception, analysis, correlation, and alert generation.
- MANAGEMENT Network: `192.168.57.10`.
- ATTACK/LAB Network: `192.168.56.10`.
- NAT/INTERNET Network: `10.0.2.3`.

## Verifiable Procedure

A ruleset modification must follow this order:

```bash
# Validar un fragmento local_rules.xml sin alterar su estructura fragmentada
{ printf '%s\n' '<ruleset>'; sudo cat /var/ossec/etc/rules/local_rules.xml; printf '%s\n' '</ruleset>'; } > /tmp/local_rules.xml.xmllint-wrapper
xmllint --noout /tmp/local_rules.xml.xmllint-wrapper
sudo /var/ossec/bin/wazuh-analysisd -t
```

After an authorized and validated modification, verify the service and logs. `ossec.conf`, manager backups, and files that may contain secrets are not published without a specific review.

## Reproducibility Limitation

The exact installation, Indexer dependencies, and certificates were not exported as sanitized public configuration. This section describes the validation process, not a complete installer.
