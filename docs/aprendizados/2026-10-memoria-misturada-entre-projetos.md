# Memória e histórico do Claude misturados entre projetos

- **Data:** 2026-10
- **Ambiente:** Claude Code 2.1.30x no dev-sandbox v0.1

## Sintoma
Uma memória gravada numa sessão de diagnóstico de disco (com a raiz do host
montada) apareceu na pasta de memória usada pelo repositório dev-sandbox.
O `/resume` listava sessões de projetos diferentes juntas.

## Causa
O Claude Code separa memória automática e transcrições por **caminho do
projeto**: `~/.claude/projects/<caminho-com-traços>/`. O `dev-docker` v0.1
montava qualquer repositório em `/workspace`, então para o Claude todos os
projetos eram um só: `~/.claude/projects/-workspace/`.

## Solução
Montar o repositório no **mesmo caminho do host** dentro do container.

## O que mudou no dev-sandbox
`dev-docker` v0.2. Guia: [memória e instruções](../claude-code/memoria-e-instrucoes.md#3-memória-dentro-do-dev-sandbox).
