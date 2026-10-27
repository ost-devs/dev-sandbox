---
name: skill-extra-files
description: Official position on README/extra files inside a skill dir, and what loads
metadata:
  type: reference
---

- No official source found (Claude Code skills page, Agent Skills best-practices, skill-creator SKILL.md text) that advises against a README.md in a skill dir; the skill-creator anatomy lists only SKILL.md + scripts/ references/ assets/. (The "no extraneous docs" rule seen elsewhere is absent: raw skill-creator SKILL.md at anthropics/skills dbd4588 has no "README", "CHANGELOG" or "installation".) 2026-10-27, 2.1.310.
- Startup loads only name+description; other files cost zero context until read ("No context penalty for large files... don't consume context tokens until actually read"). Files not linked from SKILL.md are simply not known to Claude, but it can still read them if it explores the folder. best-practices page (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), 2026-10-27.
- Sharing: personal `~/.claude/skills/<n>/`, project `.claude/skills/` (commit), plugin `<plugin>/skills/`; live change detection without restart, except a brand-new top-level skills dir needs `/reload-skills`. skills page, 2026-10-27, 2.1.310.
