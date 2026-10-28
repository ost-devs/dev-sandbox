---
paths:
  - "utils/skills/compartilhar-memorias/**"
---

# Changing the compartilhar-memorias skill

- After any change, run `python3 -m unittest discover -s utils/skills/compartilhar-memorias/tests -v` (offline, ~1 s).
- A fixed bug gets a test that fails without the fix; check it by reverting the fix once.
- Tests use a fake `~/.claude` (`CLAUDE_CONFIG_DIR` in a temp folder); never touch the real one.
- The design rests on Write/Edit refusing to write through a symlink (checked 2026-10-28). If that changes, sync breaks silently: recheck it when the guide's stamp is refreshed.
- Delete `__pycache__/` before committing.
