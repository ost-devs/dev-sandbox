# Economia de tokens: o mesmo resultado gastando menos

Este guia responde: o que a skill [`token-economy`](../../utils/skills/token-economy/SKILL.md)
faz, quando ela entra, como instalar e como ajustá-la ao seu projeto.
A história de como ela foi feita e testada, com todos os números, está em
[Como a `token-economy` foi feita e testada](./economia-de-tokens-o-experimento.md).

## O que ela faz

Ela muda **como** o Claude organiza um trabalho grande, não **o que** ele
entrega. O resultado é fixo: o que você pediu, com a qualidade que você
espera. O que varia é quantos tokens se gastam para chegar lá.

Ela evita dois erros opostos:

| Erro | Exemplo | Por que sai caro |
|---|---|---|
| Economizar cortando o resultado | Pular os testes, ler menos do que a tarefa precisa, usar um modelo fraco demais | O retrabalho custa mais que a economia |
| Gastar por garantia | Rodar cada checagem 3 vezes "para ter certeza", ler tudo "por via das dúvidas", abrir mais agentes do que o trabalho se divide | Custo sem resultado |

E procura economia onde ela não tira nada do resultado:

| Onde | O que o Claude faz |
|---|---|
| Trabalho feito duas vezes | Antes de abrir vários subagentes, monta **uma vez** o que todos precisam (gerador de entradas, executor, comparador, um cartão curto de instruções). Cada um só faz a sua parte |
| Evidência que se roda de novo | Entradas geradas com semente registrada; cada checagem é um script. Rodar um script de novo não gasta tokens; reler para conferir gasta |
| Saída que ninguém lê | Logs e relatórios longos vão para arquivo; a conversa recebe só o que a próxima decisão precisa |
| Tamanho medido | Roda uma parte primeiro, vê quanto custou, e só então divide o resto |
| Trabalho que uma falha perderia | Os agentes gravam o resultado aos poucos: se bater o limite de uso, perde-se o item em andamento, não a rodada |
| Checagens pelo que rendem | Se uma checagem gasta muito e acha pouco, ele **te avisa** e propõe reduzir. Não corta sozinho |

Escolhas que trocam resultado por tokens ficam com você: ele diz quanto cada
caminho custa e o que perde.

## Quanto economiza

No teste com execução real (conferir 24 afirmações sobre um pacote Python
pequeno, com um subagente por módulo, 2 rodadas de cada lado):

| | Com a skill | Sem a skill |
|---|---|---|
| Vereditos certos | 24/24 nas duas | 24/24 nas duas |
| Custo | US$ 0,75 e 0,67 | US$ 1,22 e 1,09 |
| Tokens de saída | 17 mil e 16 mil | 27 mil e 25 mil |

Cerca de **39% mais barato com o mesmo resultado**. É um caso só e pequeno:
mostra a direção, não é prova. Detalhes, limites e como repetir no
[artigo do experimento](./economia-de-tokens-o-experimento.md).

## Instalar

No **host**, trocando `~/dev-sandbox` pelo lugar onde você clonou o repositório:

```bash
mkdir -p ~/.claude/skills
cp -r ~/dev-sandbox/utils/skills/token-economy ~/.claude/skills/
```

A pasta traz junto os testes e resultados (`evals/`, `benchmarks/`). O Claude
só lê o `SKILL.md`; o resto não gasta contexto. Para uma cópia enxuta, copie
só ele:

```bash
mkdir -p ~/.claude/skills/token-economy
cp ~/dev-sandbox/utils/skills/token-economy/SKILL.md ~/.claude/skills/token-economy/
```

Conferir: numa sessão nova, digite `/token` e a skill deve aparecer. Skills
em `~/.claude/skills/` valem em todos os projetos, e o Claude só lê o
corpo do `SKILL.md` quando a usa
([skills](https://code.claude.com/docs/en/skills); conferido em outubro/2026,
Claude Code 2.1.310).

## Quando ela entra

Sozinha, quando o Claude vai **executar ou planejar** um trabalho de custo
grande ou repetido: vários subagentes, a mesma tarefa sobre muitos itens,
leituras ou saídas grandes, sessões longas, ou quando você fala em custo ou
em limite de uso. Ela fica quieta em tarefas pequenas e em perguntas sobre
preço de modelo ou cache da API (essas são da skill `claude-api`).

No teste de acionamento, ela **nunca entrou onde não devia** (0 de 19), e
entrou em 9 de 16 execuções onde devia. Quando ela não entra sozinha, peça:

| Você quer | Peça ao Claude |
|---|---|
| Usar a skill numa tarefa | `/token-economy traduz os 95 arquivos de docs/ pra inglês` |
| Só o plano, com o custo de cada caminho | `/token-economy monta o plano pra auditar os 12 crates, sem executar` |
| Revisar um plano que já existe | `/token-economy revisa o plan.md: onde dá pra gastar menos sem perder nada?` |

## Ajustar ao seu projeto

A skill é curta de propósito e vale para qualquer projeto. O que é só do
seu projeto vai no `CLAUDE.md` ou numa rule em `.claude/rules/`, não nela.
Exemplos:

| Você quer | Escreva no `CLAUDE.md` ou numa rule |
|---|---|
| Que ela entre em todo trabalho com muitos arquivos | `Before any task over more than 20 files, use the token-economy skill.` |
| Um teto de subagentes em paralelo | `At most 4 subagents in parallel: they hit the usage limit together.` |
| Um modelo para subagentes de execução | `Subagents that run checks use Sonnet; reviews stay on Opus.` |

## Relacionados

- [Limite de uso](./limite-de-uso.md): o que fazer quando ele chega.
- [Quanto custa](./por-baixo-dos-panos/quanto-custa.md) e
  [subagentes](./por-baixo-dos-panos/subagentes-o-que-herdam.md): por que
  dividir o trabalho muda o custo.
