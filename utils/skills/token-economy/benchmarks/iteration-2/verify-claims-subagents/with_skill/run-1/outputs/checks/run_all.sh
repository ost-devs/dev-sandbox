#!/bin/sh
# Re-run every claim check. Output: ID<TAB>TRUE|FALSE<TAB>detail
cd "$(dirname "$0")" && for f in check_*.py; do python3 "$f"; done
