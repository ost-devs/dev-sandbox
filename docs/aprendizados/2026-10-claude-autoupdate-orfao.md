# Auto-update do Claude baixava versões que nunca eram usadas

- **Data:** 2026-10 (atualizado em 2026-11)
- **Ambiente:** Claude Code instalado na imagem (`/root/.local/bin/claude`, 2.1.304)
- **Base:** evidência (a linha do `PATH` e a versão instalada foram conferidas no container)

## Sintoma
`~/.cache/dev-sandbox/home/.local/share/claude/` com 836 MB e três versões
(2.1.306, 2.1.308, 2.1.309), mas `claude --version` continuava 2.1.304.

## Causa
O auto-update grava a versão nova em `$HOME/.local/share/claude` e o link em
`$HOME/.local/bin/claude`. Dentro do container `$HOME` é persistente, então os
downloads ficavam. Só que a imagem não coloca `$HOME/.local/bin` no `PATH`: o que
vale é `/root/.local/bin`. A cada sessão: baixa, guarda, ignora.

Colocar `$HOME/.local/bin` no começo do `PATH` "resolveria", mas abriria outro
problema: um binário persistente, gravável pelo agente, na frente dos comandos
do sistema.

## Solução
`DISABLE_AUTOUPDATER=1` na imagem e atualização por rebuild
(`--build-arg AGENTS_REFRESH=$(date +%s)`). Apagar a pasta órfã no host.

## O problema voltou ao contrário (2026-11)
Em 2026-11 o rebuild instalou a 2.1.316 na imagem, mas `claude --version`
continuava 2.1.310.

- O link `$HOME/.local/bin/claude` tinha sobrado do auto-update, porque a pasta
  órfã nunca foi apagada.
- O instalador de uma skill pessoal (`traduzir`) pôs
  `export PATH="$HOME/.local/bin:$PATH"` no `~/.bashrc`, para achar o próprio
  comando. Isso colocou a pasta **antes** da imagem.

Sozinha, nenhuma das duas coisas fazia mal. Juntas, a cópia velha escondeu a da
imagem, e nenhum rebuild resolveria, porque a home fica fora da imagem.

Correção: link apagado, e a linha do `PATH` agora põe a pasta no **fim**:
`export PATH="$PATH:$HOME/.local/bin"`. Comandos pessoais continuam funcionando,
e nada nessa pasta passa na frente da imagem. Vale para qualquer instalador que
você rode dentro do container.

## O que mudou no dev-sandbox
`Dockerfile` v0.2. Guias: [sessões e persistência](../claude-code/sessoes-e-persistencia.md#atualizações-do-claude-code)
e [atualização](../guias/atualizacao.md#2-só-os-agentes), que agora manda conferir com `which claude`.
