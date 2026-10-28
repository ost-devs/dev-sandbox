---
paths:
  - "docs/claude-code/mirrors*.md"
  - "docs/claude-code/base-de-conhecimento.md"
  - "utils/skills/mirrors/README.md"
---

# Mirrors docs

- `utils/skills/mirrors/README.md` (one table per source kind, plus one for all) mirrors the usage tables of `mirrors.md`, `mirrors-de-sites.md` and `mirrors-de-artigos.md`. When a command or task changes in one, update the others.
- Usage table: `| Você quer | Peça ao Claude | Ou rode \`python3 ~/.claude/skills/mirrors/fetch_mirrors.py ...\` |`; command cells start with `...`. The header says it all: no legend paragraph before the table, no "Rode é ..." note after it.
- "Peça ao Claude" is what a practical user types, so Claude acts without guessing: `/mirrors check` when a slash command does it; otherwise a direct request with the real URL and name ("espelhe https://github.com/rust-lang/book como rust-book, sempre atualizado"). Not vague paraphrases ("espelhe o livro do Rust"), not placeholders for the subject.
- Command cells stay short: real names and flags, `<url>` for an address already shown in the request. Flags from `SKILL.md` only.
- dev-sandbox examples are welcome where they make sense to the reader (the Claude Code docs, which this repo mirrors). Avoid only examples that mean nothing outside this repo's history.
- `base-de-conhecimento.md` names all three source kinds and links to their guides.
