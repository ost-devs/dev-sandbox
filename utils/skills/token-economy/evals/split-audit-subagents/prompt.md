---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenho um documento `docs/paridade.md` com 480 afirmações do tipo "a função X do crate Y se comporta como Z", e preciso conferir cada uma contra o código-fonte de 12 crates Rust espelhados em `mirrors/` (umas 60 mil linhas no total). Monte o plano de execução com subagentes: como dividir, quantos em paralelo, o que cada um lê, o que volta para a conversa principal. Não execute nada ainda, só escreva o plano em plan.md.
