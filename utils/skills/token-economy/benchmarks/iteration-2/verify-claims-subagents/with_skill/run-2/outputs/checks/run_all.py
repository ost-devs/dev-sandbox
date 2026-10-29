"""Run every checks/<module>/check_*.py and print one JSON line per claim."""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for path in sorted(glob.glob(os.path.join(HERE, "*", "check_*.py"))):
    r = subprocess.run([sys.executable, path], capture_output=True, text=True)
    sys.stdout.write(r.stdout if r.returncode == 0 else f'{{"script": "{path}", "error": {r.stderr!r}}}\n')
