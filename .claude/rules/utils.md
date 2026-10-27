---
paths:
  - "utils/**"
---

# Shareable skills and agents

- Users install a skill by copying its whole folder into `~/.claude/skills/`. Keep in it only files the model uses (SKILL.md, scripts, templates). Human guides go to `docs/claude-code/<skill>.md` (Portuguese, same shape as `montar-consultor.md`), linked from the `utils/README.md` table.
- Not an official Claude Code rule (checked 10/2026): an unreferenced file costs no context, but Claude may read it when it explores the folder.
