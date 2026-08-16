#!/usr/bin/env python3
"""Reconstruct a port-scan sequence from an exported Wazuh Dashboard CSV.

The tool preserves selected original rows in JSON, orders them by timestamp, and
counts destination ports exactly per (source, destination, protocol) session.
It does not alter Wazuh data or rules.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


TIMESTAMP_FORMATS = ("%d %b , %Y @ %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%f%z")
FIELDS = {
    "timestamp": ("timestamp",),
    "source": ("data.win.eventdata.sourceAddress", "sourceAddress", "source_ip", "srcip"),
    "destination": ("data.win.eventdata.destAddress", "destAddress", "destination_ip", "dstip"),
    "port": ("data.win.eventdata.destPort", "destPort", "dest_port", "destPortNumber"),
    "protocol": ("data.win.eventdata.protocol", "protocol"),
    "event_id": ("data.win.system.eventID", "eventID", "event_id"),
    "rule_id": ("rule.id", "rule_id"),
}


def value(row: dict[str, Any], field: str) -> str:
    for key in FIELDS[field]:
        candidate = row.get(key)
        if candidate not in (None, ""):
            return str(candidate).strip()
    return ""


def timestamp(value_: str) -> datetime:
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value_, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported timestamp: {value_!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", default="192.168.56.1")
    parser.add_argument("--destination", default="192.168.56.20")
    parser.add_argument("--limit", type=int, default=34)
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for raw in rows:
        source, destination, port = value(raw, "source"), value(raw, "destination"), value(raw, "port")
        if source != args.source or destination != args.destination or not port:
            continue
        try:
            port_number = int(port)
            parsed_time = timestamp(value(raw, "timestamp"))
        except ValueError:
            continue
        selected.append((parsed_time, port_number, raw))
    selected.sort(key=lambda item: item[0])
    selected = selected[: args.limit]
    if len(selected) != args.limit:
        raise SystemExit(f"Expected {args.limit} matching events; found {len(selected)}")

    args.output.mkdir(parents=True, exist_ok=True)
    raw_path = args.output / "raw_selected_events.json"
    raw_path.write_text(json.dumps([raw for _, _, raw in selected], indent=2) + "\n", encoding="utf-8")

    seen: dict[tuple[str, str, str], set[int]] = defaultdict(set)
    sequence = []
    for index, (event_time, port, raw) in enumerate(selected, start=1):
        source, destination = value(raw, "source"), value(raw, "destination")
        protocol = value(raw, "protocol") or "unknown"
        session = (source, destination, protocol)
        is_new = port not in seen[session]
        seen[session].add(port)
        sequence.append({
            "event_index": index,
            "timestamp": event_time.isoformat(),
            "source_ip": source,
            "destination_ip": destination,
            "protocol": protocol,
            "destination_port": port,
            "is_unique_port_for_session": is_new,
            "unique_port_count": len(seen[session]),
            "event_id": value(raw, "event_id"),
            "rule_id": value(raw, "rule_id"),
            "raw_csv_row": raw,
        })

    csv_path = args.output / "sequence_unique_ports.csv"
    columns = [key for key in sequence[0] if key != "raw_csv_row"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: row[key] for key in columns} for row in sequence)

    summaries = [{"source_ip": key[0], "destination_ip": key[1], "protocol": key[2], "unique_destination_ports": len(ports), "ports": sorted(ports)} for key, ports in seen.items()]
    (args.output / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")
    report = [f"INPUT={args.input}", f"TOTAL_EVENTS={len(sequence)}", f"SESSIONS={len(summaries)}"]
    for summary in summaries:
        report.append("SESSION=" + json.dumps(summary, sort_keys=True))
    for target in (9, 10):
        event = sequence[target - 1]
        report.extend((f"EVENT_{target}_METADATA=" + json.dumps({key: value for key, value in event.items() if key != "raw_csv_row"}, sort_keys=True), f"EVENT_{target}_RAW_CSV=" + json.dumps(event["raw_csv_row"], sort_keys=True)))
    (args.output / "cardinality_report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
