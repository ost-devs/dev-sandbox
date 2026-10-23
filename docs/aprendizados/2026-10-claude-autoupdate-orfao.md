# Auto-update do Claude baixava versões que nunca eram usadas

- **Data:** 2026-10
- **Ambiente:** Claude Code instalado na imagem (`/root/.local/bin/claude`, 2.1.304)

## Sintoma
`~/.cache/dev-sandbox/home/.local/share/claude/` com 836 MB e três versões
(2.1.306, 2.1.308, 2.1.309), mas `claude --version` continuava 2.1.304.

## Causa
O auto-update grava a versão nova em `$HOME/.local/share/claude` e o link em
`$HOME/.local/bin/claude`. Dentro do container `$HOME` é persistente, então os
downloads ficavam. Só que `$HOME/.local/bin` não está no `PATH`: o que vale é
`/root/.local/bin`, da imagem. A cada sessão: baixa, guarda, ignora.

Colocar `$HOME/.local/bin` no `PATH` "resolveria", mas abriria outro problema:
um binário persistente, gravável pelo agente, na frente dos comandos do sistema.

## Solução
`DISABLE_AUTOUPDATER=1` na imagem e atualização por rebuild
(`--build-arg AGENTS_REFRESH=$(date +%s)`). Apagar a pasta órfã no host.

## O que mudou no dev-sandbox
`Dockerfile` v0.2. Guia: [sessões e persistência](../claude-code/sessoes-e-persistencia.md#atualizações-do-claude-code).
