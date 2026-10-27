---
paths:
  - "docs/**"
  - "README.md"
  - "DOCUMENTACAO.md"
  - "CHANGELOG.md"
---

# Writing the human docs

- Plain Brazilian Portuguese for beginners: short sentences, tables for comparisons, commands ready to paste, say where each command runs (host or container).
- One guide answers one question; its index row says what it answers (`docs/README.md`, `docs/claude-code/README.md`, `docs/aprendizados/README.md`). Add the row when you add a file.
- Claude Code facts: cite the official page (`code.claude.com/docs/en/...`), stamp "Conferido em <mês>/<ano> (Claude Code <versão>)", and mark deductions as such.
- Learnings follow the template in `docs/aprendizados/README.md`, including **Base** (evidência, documentação or análise).
- Link to `Dockerfile`/`dev-docker` and quote short excerpts; never paste copies that will drift.
- Anchors: GitHub keeps accents in heading anchors; explicit `<a id>` anchors in `DOCUMENTACAO.md` have none. Check the target before linking.
