#!/usr/bin/env bash
# Run as root on the manager. The caller supplies already-validated candidate paths.
set -euo pipefail

active=${1:?active rules path required}
candidate=${2:?candidate rules path required}
stamp=${3:?timestamp required}
pretest="${active}.pretest-${stamp}"
analysis_out="/tmp/wazuh-analysisd-${stamp}.out"

cp -p "$active" "$pretest"
restore() {
  cp -p "$pretest" "$active"
  echo "ROLLBACK=restored ${pretest} to ${active}" >&2
}

trap 'restore' ERR
install -o wazuh -g wazuh -m 0660 "$candidate" "$active"
if ! /var/ossec/bin/wazuh-analysisd -t >"$analysis_out" 2>&1; then
  cat "$analysis_out" >&2
  exit 1
fi
if grep -nE 'WARNING|ERROR|CRITICAL' "$analysis_out"; then
  cat "$analysis_out" >&2
  exit 1
fi
sha256sum "$active" "$pretest"
echo "ANALYSISD_VALID=1"
echo "ANALYSISD_OUTPUT=${analysis_out}"
trap - ERR
