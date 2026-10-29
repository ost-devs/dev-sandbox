---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Em `claims.md` há 24 afirmações sobre as funções do pacote `calc/` (4 módulos). Confira todas rodando o código, não só lendo: cada veredito precisa de uma checagem reproduzível (entradas fixas, ou geradas com semente registrada) gravada em `checks/`, que qualquer pessoa possa rodar de novo e obter o mesmo resultado. Use subagentes, um por módulo, em paralelo. No fim, escreva `report.md` com uma tabela: id, veredito (verdadeira/falsa), contraexemplo quando falsa, e o comando que reproduz a checagem.

Input files: calc/, claims.md
