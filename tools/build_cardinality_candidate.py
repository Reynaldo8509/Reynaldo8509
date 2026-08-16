#!/usr/bin/env python3
"""Create a narrow, reviewable candidate from local_rules.xml.

The change is deliberately limited to making the Sysmon EID 3 base rule
independent of a decoder group while retaining the same ATTACK/LAB predicate.
It does not claim exact set cardinality; that requires the architecture
documented in the accompanying proposal.
"""

from __future__ import annotations

import argparse
from pathlib import Path


OLD_SYSMON = '''  <rule id="100409" level="1">
    <if_group>sysmon_event3</if_group>
    <field name="win.eventdata.protocol">^tcp$</field>
'''
NEW_SYSMON = '''  <rule id="100409" level="1">
    <field name="win.system.providerName">^Microsoft-Windows-Sysmon$</field>
    <field name="win.system.channel">^Microsoft-Windows-Sysmon/Operational$</field>
    <field name="win.system.eventID">^3$</field>
    <field name="win.eventdata.protocol">^tcp$</field>
'''
def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one {label} target; found {text.count(old)}")
    return text.replace(old, new, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    text = args.source.read_text(encoding="utf-8")
    text = replace_once(text, OLD_SYSMON, NEW_SYSMON, "Sysmon base")
    args.candidate.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
