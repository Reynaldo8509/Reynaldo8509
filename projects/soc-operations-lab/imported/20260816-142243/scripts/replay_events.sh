#!/usr/bin/env bash
# Reproduce exactamente los 34 eventos raw de artifacts/events-34.json en Wazuh.
# No ejecutado durante la fase de inventario. Requiere ejecutarse EN el manager.
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
events_file="${repo_dir}/artifacts/events-34.json"
logtest_bin="${WAZUH_LOGTEST_BIN:-/var/ossec/bin/wazuh-logtest}"

[[ -x "$logtest_bin" ]] || { echo "FAIL: wazuh-logtest no existe: $logtest_bin" >&2; exit 1; }
[[ -r "$events_file" ]] || { echo "FAIL: falta $events_file" >&2; exit 1; }

# El artefacto debe ser una exportación de archives.json y preservar raw_event.
# Se rechaza deliberadamente una exportación de Dashboard CSV: no es una entrada
# reproducible para logtest.
python3 - "$events_file" <<'PY' | "$logtest_bin" -v
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as handle:
    payload = json.load(handle)
events = payload.get("events", [])
if len(events) != 34:
    raise SystemExit(f"FAIL: se esperaban 34 eventos; hay {len(events)}")
for index, event in enumerate(events, 1):
    raw = event.get("raw_event")
    if not isinstance(raw, str) or not raw.strip():
        raise SystemExit(
            f"FAIL: evento {index} no incluye raw_event de archives.json; "
            "no se puede reproducir fielmente desde un CSV de Dashboard"
        )
    print(raw)
PY
