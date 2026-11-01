#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
for i in 1 2 3 4 5 6; do python3 -I checks/dates/check_D$i.py; done > checks/dates/results.jsonl
cat checks/dates/results.jsonl
