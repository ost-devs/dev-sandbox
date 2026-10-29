---
paths:
  - "utils/skills/**/SKILL.md"
  - ".claude/skills/**/SKILL.md"
---

# Writing a SKILL.md

- Single responsibility: the skill covers its own job, nothing before or after it. What to do with its output (how to cite it, whether to edit it, project policies) belongs to the project or the caller. State facts about what the skill produces ("copies are read-only"), not rules for using them.
- The reader is Claude Code on Opus or Sonnet: write for it, not for a human (the human docs are `README.md` and `docs/`). Only Claude Code; no other tools or vendors.
- One step: put the commands and the essential, non-obvious facts in the skill itself, so it acts at once. Don't make it run `--help` or read another file first, and don't explain what a capable model infers.
- Defaults live in the tool's data (a manifest field, a flag default), not in instructions every caller must repeat.
- When you finish, if this work taught something about writing skills that this file lacks or gets wrong, suggest the lines to add or revise to the user. Don't edit this file without their approval.
