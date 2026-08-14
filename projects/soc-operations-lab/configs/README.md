# Publishable Configurations

This directory is reserved for sanitized, reproducible configurations. Active Wazuh, Sysmon, YARA, and Windows files are not currently exported because they may contain environment-specific paths, identifiers, or sensitive material.

A future published configuration must include:

1. the component purpose and version;
2. variables or values the reader must replace;
3. reproducible validation;
4. a secret review before it is added to the repository.

The documented WFP rules are maintained in [detection-rules](../detection-rules/), not as a copy of the active `local_rules.xml`.
