# Operations: Validation Workflow

## Evidence Principle

| Layer | What It Demonstrates | What It Does Not Demonstrate |
|---|---|---|
| `archives.json` | The manager ingested and decoded the event. | That a rule created an alert or that Dashboard displays it. |
| `alerts.json` | A rule created a visible alert. | That Indexer and Dashboard received it. |
| Filebeat / Indexer | Indexing-pipeline health. | That a specific query or dashboard shows the document. |
| Authenticated query / Dashboard | Actual indexing and visualization. | The quality or semantics of the detection. |

## Rule-Change Workflow

1. Back up the affected file and record a hash where appropriate.
2. Validate XML through a wrapper if the ruleset is a multi-group fragment.
3. Run `wazuh-analysisd -t` and treat new warnings as failures to investigate.
4. Restart only the authorized service.
5. Test with real telemetry in the authorized scope.
6. Validate the positive path and MANAGEMENT/NAT negative paths.
7. Review `archives.json`, `alerts.json`, and, if access is available, the index/Dashboard.

## Using wazuh-logtest

`wazuh-logtest` is useful for validating syntax and correlation concepts. It does not replace the real event: manually pasted JSON can follow the `json` decoder rather than the real `windows_eventchannel` path.
