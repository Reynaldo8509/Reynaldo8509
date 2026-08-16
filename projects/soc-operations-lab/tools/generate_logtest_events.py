#!/usr/bin/env python3
"""Generate minimal, non-sensitive WFP or Sysmon Event ID 3 JSONL for logtest."""

from __future__ import annotations

import argparse
import json


def wfp(port: int) -> dict:
    return {"win": {"system": {"providerName": "Microsoft-Windows-Security-Auditing", "eventID": "5152", "channel": "Security"}, "eventdata": {"direction": "%%14592", "protocol": "6", "sourceAddress": "192.168.56.1", "destAddress": "192.168.56.20", "destPort": str(port)}}}


def sysmon(port: int) -> dict:
    return {"win": {"system": {"providerName": "Microsoft-Windows-Sysmon", "eventID": "3", "channel": "Microsoft-Windows-Sysmon/Operational"}, "eventdata": {"protocol": "tcp", "sourceIp": "192.168.56.1", "destinationIp": "192.168.56.20", "destinationPort": str(port)}}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("wfp", "sysmon"), required=True)
    parser.add_argument("--count", type=int, default=15)
    parser.add_argument("--ports", help="comma-separated explicit port sequence")
    args = parser.parse_args()
    create = wfp if args.kind == "wfp" else sysmon
    ports = [int(port) for port in args.ports.split(",")] if args.ports else range(10001, 10001 + args.count)
    for port in ports:
        print(json.dumps(create(port), separators=(",", ":")))


if __name__ == "__main__":
    main()
