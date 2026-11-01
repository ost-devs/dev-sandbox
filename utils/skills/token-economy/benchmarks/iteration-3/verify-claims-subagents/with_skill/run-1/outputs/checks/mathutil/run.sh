#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
for i in 1 2 3 4 5 6; do python3 -I checks/mathutil/check_M$i.py; done > checks/mathutil/results.jsonl
cat checks/mathutil/results.jsonl
