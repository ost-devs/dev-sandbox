---
paths:
  - "docs/claude-code/mirrors*.md"
  - "docs/claude-code/base-de-conhecimento.md"
  - "utils/skills/mirrors/README.md"
---

# Mirrors docs

- `utils/skills/mirrors/README.md` has one table per source kind (repositories, doc sites, web articles, plus a short shared one) mirroring the usage tables of `mirrors.md`, `mirrors-de-sites.md` and `mirrors-de-artigos.md`. When a command or task changes in one, update the others.
- Every guide's usage part uses the table `| Você quer | Peça ao Claude | Ou rode |`, with real commands from `utils/skills/mirrors/SKILL.md`; never invent a flag.
- Examples are general (a popular library, docs site or article any dev cares about), not dev-sandbox internals; a named site must really work with the skill.
- `base-de-conhecimento.md` names all three source kinds and links to their guides.
