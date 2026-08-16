# Sanitization actions

- High-confidence sensitive-pattern findings in tracked project content: **0**.
- An initial publication-safety invocation was accidentally scoped outside the project and produced an out-of-scope log. That log was quarantined under `GitBackup/secret_leaks_auto-audit-20260815-234701/`, removed from the audit candidate, and is not tracked or published.
- The same publication-safety check was rerun from the canonical project directory and passed.
- `gitleaks` was not installed. The report records the coverage gap without embedding scanner output containing possible secret values.
- A private audit directory was placed under `GitBackup/auto-audit-20260815-234701/`; no project credential file was moved because the scoped pattern audit found none.
- Local repository paths are represented only as logical checkout labels in `full_report.json`.

**Urgent action:** retain the scoped-working-directory guard for all future scans. If a later scanner finds a project secret, preserve a local-only backup, redact/revoke the credential, and do not add the original artifact to Git.
