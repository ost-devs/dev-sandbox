#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
for i in 1 2 3 4 5 6; do python3 -I checks/textutil/check_T$i.py; done
