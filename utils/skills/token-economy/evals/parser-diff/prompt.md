---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Reescrevi o parser de linha CSV: o antigo está em `csvline/old.py` e o novo em `csvline/new.py`, os dois com `parse(line) -> list[str]`. Antes de trocar um pelo outro, quero saber onde o novo se comporta diferente. Gera uns 200 casos de entrada, roda nos dois e grava cada diferença em `diffs.jsonl` (uma linha JSON por caso: `input`, `old`, `new`). Em `diff-report.md`, agrupa as diferenças por tipo, com um exemplo mínimo de cada, e põe o comando que gera tudo de novo: quero poder repetir depois e obter o mesmo resultado.

Input files: csvline/
