---
paths:
  - "utils/skills/mirrors/**"
---

# Changing the mirrors skill

- After changing `fetch_mirrors.py`, `fetch_pages.py` or `fetch_web.py`, check whether it adds or changes something a user or agent can do (a flag, a manifest field, a default, an output line they act on). If so, update `SKILL.md` and the script's docstring (`--help`), then `README.md` and its guides (`mirrors-docs.md`).
- After any change, run `python3 -m unittest discover -s utils/skills/mirrors/tests -v` (offline, ~20 s). Web tests skip without Defuddle: `npm ci --prefix utils/skills/mirrors --ignore-scripts` first.
- A fixed bug gets a test that fails without the fix; check it by reverting the fix once.
- Keep tests offline: local git repos (`file://`) and the local `Server`, never real sites.
- Delete `__pycache__/` before committing; it would be copied into users' installed skill.
