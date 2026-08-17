# Endpoint telemetry query result

The command execution returned its unique exercise marker. Follow-up,
read-only queries found no matching records in these sources:

- Sysmon Operational, Event ID 1 (Process Create)
- PowerShell Operational, Event ID 4104 (Script Block Logging)
- Windows Security, Event ID 4688 (Process Creation)

The empty JSONL files in this directory record the corresponding query result.
They are not evidence that the command failed; `command-output.txt` establishes
execution. They demonstrate that the current endpoint configuration does not
produce the telemetry required for a manager-side PowerShell detection.
