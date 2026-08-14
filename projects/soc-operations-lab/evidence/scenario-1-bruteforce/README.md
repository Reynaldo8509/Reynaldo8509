# Scenario 1 — Brute Force (legacy marker)

This directory retains a sanitized export of five Windows Security `4625` events ([CSV](events-2026-08-08T18_46_56.179Z.csv)) and the historical scenario documentation marker. Three rows show NTLM failures from `192.168.56.1`; two are local failures from `127.0.0.1`. The file contains no passwords, tokens, or public addresses.

The CSV proves individual telemetry and historical rule `60122`; it does not prove a custom correlation, a brute-force alert, or a negative test. Future evidence must contain an authorized test, sanitized ingestion/alert fields, and a description of the effective rule. Until then, the brute-force status is **TELEMETRY OBSERVED / PENDING DETECTION VALIDATION**.
