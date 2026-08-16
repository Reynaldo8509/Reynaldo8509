#!/usr/bin/env bash
set -euo pipefail

# Read-only pre-publication check. Review every reported match manually.
patterns='BEGIN [A-Z ]*PRIVATE KEY|Authorization:[[:space:]]*Bearer|password[[:space:]]*[:=][[:space:]]*[^[:space:]]+|passwd[[:space:]]*[:=][[:space:]]*[^[:space:]]+|api[_-]?key[[:space:]]*[:=][[:space:]]*[^[:space:]]+|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]+'

echo '== Content patterns requiring review =='
if rg -n -i --hidden \
  --glob '!.git/**' \
  --glob '!scripts/validation/check-publication-safety.sh' \
  --glob '!.gitignore' \
  "$patterns" .; then
  echo 'Potential secret-like content found. Review before publishing.' >&2
  exit 1
fi

echo '== Secret-like filenames requiring review =='
if find . -path './.git' -prune -o -type f \( \
  -iname '*.pem' -o -iname '*.key' -o -iname '*.p12' -o -iname '*.pfx' -o \
  -iname '*.kdbx' -o -iname '*.ovpn' \) -print | grep -q .; then
  find . -path './.git' -prune -o -type f \( \
    -iname '*.pem' -o -iname '*.key' -o -iname '*.p12' -o -iname '*.pfx' -o \
    -iname '*.kdbx' -o -iname '*.ovpn' \) -print
  exit 1
fi

echo 'PASS: no high-confidence secret patterns or secret-like filenames found.'
