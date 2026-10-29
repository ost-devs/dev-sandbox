---
tags: [skill-creator]
max_turns: 120
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Antes do release preciso conferir o `claims.md`: são 152 afirmações sobre as funções do pacote `kit/` (8 módulos), escritas por gente diferente ao longo do tempo. Confira cada uma rodando o código, não só lendo: cada veredito precisa de uma checagem reproduzível (entradas fixas, ou geradas com semente registrada) gravada em `checks/`, que qualquer pessoa possa rodar de novo e obter o mesmo resultado. Divide o trabalho entre subagentes em paralelo, um por módulo. No fim, escreva `report.md` com uma tabela: id, veredito (verdadeira/falsa), contraexemplo quando falsa, e o comando que reproduz a checagem.

Input files: kit/, claims.md
