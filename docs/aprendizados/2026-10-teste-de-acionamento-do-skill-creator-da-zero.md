# O teste de acionamento do `skill-creator` dá zero mesmo quando a skill aciona

- **Data:** 2026-10
- **Ambiente:** Claude Code 2.1.310, Opus 5.5, dentro do dev-sandbox; skill `skill-creator` da Anthropic
- **Base:** evidência: 29/10/2026, skill `token-economy`, 20 pedidos medidos pelos dois métodos
  ([dados](../../utils/skills/token-economy/benchmarks/trigger-1/RUN.md))

## Sintoma
O `run_eval` do `skill-creator` (e o `run_loop`, que otimiza a descrição em cima dele) mediu
**0 de 60** acionamentos, inclusive em pedidos óbvios para a skill. Na rodada anterior, com a
skill instalada, ela tinha acionado sozinha nas duas sessões.

## Causa
O script não instala a skill: cria um comando falso em `.claude/commands/` com a descrição
dela e procura uma chamada a esse nome. Nesta versão, o modelo nunca chamou o comando falso.
Além disso, ele só conta a skill se ela for a **primeira** ferramenta; se o modelo abre um
arquivo antes, a execução é encerrada como "não acionou".

## Solução
Medir com a skill instalada de verdade (um link em `.claude/skills/<nome>` durante o teste) e
anotar todas as ferramentas que o modelo chama, com `claude -p --output-format stream-json
--verbose --max-turns 2`. Assim a `token-economy` acionou em 9 de 16 execuções que deviam, e
em 0 de 19 que não deviam. O script está em
[`trigger_seq.py`](../../utils/skills/token-economy/benchmarks/trigger-1/trigger_seq.py).
Não use o `run_loop` enquanto o `run_eval` der zero: ele otimizaria a descrição contra uma
medida quebrada.

## O que mudou no dev-sandbox
Nada na imagem. O teste da `token-economy` passou a usar o método acima
([artigo do experimento](../claude-code/economia-de-tokens-o-experimento.md#6-rodada-3-ela-entra-quando-deve)).
