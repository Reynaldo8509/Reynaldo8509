# Future improvements

1. Validate Sysmon Event ID 3 with an authorized ATTACK signal before modifying its rules.
2. Implement stateful normalization outside the native rules engine if exact `COUNT(DISTINCT destinationPort)` is required.
3. Publish Wazuh/Sysmon/YARA configurations only after sanitizing them and creating validation tests.
4. Run an authenticated query to Wazuh Indexer and a Dashboard check to complete the visualization chain.
5. Create reproducible, sanitized evidence for FIM, YARA, and brute force.
6. Replace empty brute-force evidence placeholders through a controlled test, or remove them in a future authorized cleanup.
