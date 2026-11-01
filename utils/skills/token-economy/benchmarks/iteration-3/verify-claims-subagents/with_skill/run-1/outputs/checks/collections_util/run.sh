#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
for i in 1 2 3 4 5 6; do python3 -I checks/collections_util/check_C$i.py; done > checks/collections_util/results.jsonl
cat checks/collections_util/results.jsonl
