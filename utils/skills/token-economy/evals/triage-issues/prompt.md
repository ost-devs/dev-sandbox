---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Exportei as 80 issues abertas do repositório para `issues.json`. Classifica cada uma em bug, feature ou dúvida e marca as duplicadas (mesmo problema contado por outra pessoa), apontando a original, que é a de número menor. Salva em `triage.csv` com as colunas `number,tipo,duplicada_de` (tipo: `bug`, `feature` ou `duvida`; `duplicada_de` vazio quando não for duplicada).

Input files: issues.json
