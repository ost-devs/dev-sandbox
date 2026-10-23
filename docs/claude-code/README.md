# Claude Code no dev-sandbox

Guias sobre como o Claude Code se comporta dentro do container e como tirar
proveito dele. Valem também, em boa parte, fora do Docker.

| Guia | Responde |
|---|---|
| [Memória e instruções](./memoria-e-instrucoes.md) | O que é a memória automática, como difere de `CLAUDE.md`/`AGENTS.md`/rules, como fica separada por projeto no container |
| [Sessões e persistência](./sessoes-e-persistencia.md) | O que sobrevive ao `exit`, a pasta `/tmp/claude-*`, como retomar trabalho depois do limite de uso, atualizações |

Relacionados: [backup e git](../guias/backup-e-git.md) (como não perder
`~/.claude`) e [sessões paralelas](../guias/portas-e-sessoes-paralelas.md)
(vários Claudes ao mesmo tempo).

## Como o Claude Code recebe as instruções do ambiente

A imagem copia [`sandbox/AGENTS.md`](../../sandbox/AGENTS.md) para
`/etc/claude-code/CLAUDE.md`, o local de instruções "managed" do Claude Code
no Linux. Ele carrega sozinho em todo projeto aberto **dentro do
container**, e só lá: o seu `~/.claude/CLAUDE.md` do host não é tocado.

Ver se carregou: rode `/context` numa sessão e procure em *Memory files*.
