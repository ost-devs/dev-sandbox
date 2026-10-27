# Claude Code no dev-sandbox

Guias sobre como o Claude Code se comporta dentro do container e como tirar
proveito dele. Valem também, em boa parte, fora do Docker.

| Guia | Responde |
|---|---|
| [Um consultor do projeto](./consultor-do-projeto.md) | Como uma conversa nova já começa sabendo o projeto: rules, skills, agente pesquisador, memória e `/consolidar` |
| [Instrução ou mecanismo](./instrucao-ou-mecanismo.md) | O que vai no `CLAUDE.md`/rules e o que vai em settings, hooks ou no Docker; o teste da linha, com o caso da v0.4 |
| [Memória e instruções](./memoria-e-instrucoes.md) | O que é a memória automática, como difere de `CLAUDE.md`/`AGENTS.md`/rules, como fica separada por projeto no container |
| [Sessões e persistência](./sessoes-e-persistencia.md) | O que sobrevive ao `exit`, a pasta `/tmp/claude-*`, como retomar trabalho depois do limite de uso, atualizações |
| [Trabalhar por projeto](./projetos.md) | O que é um projeto para o Claude, o que é guardado por projeto, projetos com vários repositórios, onde pôr cada instrução, o ciclo da memória, sessões longas |
| [Preservar conversas](./preservar-conversas.md) | O que o Claude apaga e quando, como guardar sessões valiosas (nome, `/export`, PKM) e um hook que arquiva tudo |
| [Migrar memórias](./migrar-memorias.md) | Levar memórias de uma pasta de projeto para outra (saída da v0.1, uso de `--nome`, projeto movido) |
| [Por baixo dos panos](./por-baixo-dos-panos/README.md) | Como o Claude Code funciona por dentro: janela de contexto, o que carrega e quando, reenvio a cada pedido, cache, compactação, subagentes |
| [Modelo e esforço](./modelo-e-esforco.md) | Qual modelo e qual nível de esforço usar, com um diário de campo para comparar com a prática (esboço) |

Relacionados: [backup e git](../guias/backup-e-git.md) (como não perder
`~/.claude`) e [sessões paralelas](../guias/portas-e-sessoes-paralelas.md)
(vários Claudes ao mesmo tempo).

## Como o Claude Code recebe as instruções do ambiente

A imagem copia [`sandbox/AGENTS.md`](../../sandbox/AGENTS.md) para
`/etc/claude-code/CLAUDE.md`, o local de instruções "managed" do Claude Code
no Linux. Ele carrega sozinho em todo projeto aberto **dentro do
container**, e só lá: o seu `~/.claude/CLAUDE.md` do host não é tocado
([prova de que carrega sozinho](../aprendizados/2026-10-etc-claude-md-carrega-sozinho.md)).

Ver se carregou: rode `/context` numa sessão e procure em *Memory files*.
