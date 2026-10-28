---
paths:
  - "docs/claude-code/mirrors*.md"
  - "docs/claude-code/base-de-conhecimento.md"
  - "utils/skills/mirrors/README.md"
---

# Mirrors docs

- `utils/skills/mirrors/README.md` (one table per source kind, plus one for all) mirrors the usage tables of `mirrors.md`, `mirrors-de-sites.md` and `mirrors-de-artigos.md`. When a command or task changes in one, update the others.
- Before the first usage table, the "Como ler as tabelas" block: `...` is `/mirrors` in a Claude session or `python3 ~/.claude/skills/mirrors/fetch_mirrors.py` in a terminal; `< >` marks what the reader replaces. Never explain it after the table.
- Table: `| Você quer | Peça ao Claude | Ou use o comando |`. The request is plain speech a beginner would type ("espelhe a documentação do <Claude Code>"), not a command. The command starts with `...` and uses real flags from `SKILL.md`.
- Keep cells short: placeholders with an example inside (`<rust-book>`, `<testes>`), never full URLs or long flag lists in a table.
- dev-sandbox examples are welcome where they make sense to the reader (the Claude Code docs, which this repo mirrors). Avoid only examples that mean nothing outside this repo's history.
- `base-de-conhecimento.md` names all three source kinds and links to their guides.
