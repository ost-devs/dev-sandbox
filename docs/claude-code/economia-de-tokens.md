# Economia de tokens: o mesmo resultado gastando menos

Este guia responde: o que a skill [`token-economy`](../../utils/skills/token-economy/SKILL.md)
faz, quando ela entra, como instalar e como ajustá-la ao seu projeto.
A história de como ela foi feita e testada, com todos os números, está em
[Como a `token-economy` foi feita e testada](./economia-de-tokens-o-experimento.md).

## Resumo honesto

Sem a skill, o Claude já faz bem o trabalho. Nos testes com execução real, ele
dividiu a tarefa entre subagentes, rodou o código e acertou todas as afirmações,
**com ou sem ela**. O ganho medido da skill é de custo, não de qualidade.

Em tarefa grande com vários subagentes, ela custou uns **15% a menos** com o
mesmo resultado, e toda execução com a skill saiu mais barata que toda execução
sem ela. É uma economia modesta, mas de graça: a skill ocupa uns 90 tokens de
contexto até ser usada. Em tarefa menor, o tamanho do ganho ainda não está
claro. Os números estão em [Quanto economiza](#quanto-economiza).

## O que ela faz

Ela orienta **como** o Claude organiza um trabalho grande, não **o que** ele
entrega. O resultado continua sendo o que você pediu; a skill busca o caminho
que chega lá gastando menos.

Ela nomeia dois erros opostos, para que fugir de um não empurre para o outro:

| Erro | Exemplo | Por que sai caro |
|---|---|---|
| Economizar cortando o resultado | Pular os testes, ler menos do que a tarefa precisa, usar um modelo fraco demais | O retrabalho custa mais que a economia |
| Gastar por garantia | Rodar cada checagem 3 vezes "para ter certeza", ler tudo "por via das dúvidas", abrir mais agentes do que o trabalho se divide | Custo sem resultado |

E aponta onde costuma dar para economizar:

| Onde | O que ela pede ao Claude |
|---|---|
| Trabalho feito duas vezes | Antes de abrir vários subagentes, montar **uma vez** o que todos precisam (ajudantes e um cartão curto de instruções) |
| Evidência que se roda de novo | Usar entradas com semente registrada e fazer cada checagem como script: rodar um script de novo não gasta tokens |
| Saída que ninguém lê | Mandar logs e relatórios longos para arquivo |
| Tamanho medido | Rodar uma parte primeiro, ver quanto custou e só então dividir o resto |
| Trabalho que uma falha perderia | Gravar o resultado aos poucos, para perder menos se bater o limite de uso |
| Checagens pelo que rendem | Se uma checagem gasta muito e acha pouco, **avisar você** e propor reduzir, sem cortar sozinho |

Isso é o que a skill pede, não o que foi provado. O efeito medido foi só o do
conjunto. Nem o ganho contra perda por limite de uso ficou demonstrado.

Escolhas que trocam resultado por tokens ficam com você: ele deve dizer quanto
cada caminho custa e o que perde.

## Quanto economiza

Teste com o Sonnet em tarefas reais, cada grupo rodado várias vezes:

| Tarefa | Execuções | Custo médio com a skill | Custo médio sem a skill | Veredito |
|---|---|---|---|---|
| Conferir 152 afirmações em 8 módulos, com 8 subagentes | 4 de cada lado | US$ 0,72 | US$ 0,85 | Diferença pequena: cerca de 15% mais barato |
| A mesma tarefa, parando no meio por limite de uso simulado | 4 de cada lado | só em unidades | só em unidades | Cerca de 18% menos, com evidência fraca |
| Conferir 24 afirmações em 4 módulos, com 4 subagentes | 6 de cada lado | US$ 0,31 | US$ 0,36 | Inconclusivo: média menor em dólar, mas com a skill houve execuções mais caras |

A qualidade foi igual em todas: **todas as execuções acertaram tudo**.

O que isso quer dizer na prática:

- **Tarefa grande com muitos subagentes:** 15% a menos sem perder qualidade é
  dinheiro de verdade, ainda mais em quem repete esse tipo de trabalho.
- **Tarefa menor:** em nenhum grupo a média em dólar ficou pior com a skill, mas
  a amostra não mostra de quanto é o ganho. Conte como possível, não como certo.
- **Tarefas sem subagentes ou que não acionam a skill:** não medimos o suficiente.
- **Tarefas abertas, como arquitetura ou decisões de produto:** não testamos.
  Estes testes são objetivos e lógicos, com resposta certa que se confere
  rodando código. É o tipo de trabalho em que o Claude costuma ir bem sozinho.
  Por isso, eles não dizem se a skill ajuda mais ou menos em tarefas abertas.

Um teste anterior deu "39% mais barato", mas com só 2 rodadas de cada lado e
subagentes em modelos diferentes. Esse número não vale mais. Detalhes e limites
no [artigo do experimento](./economia-de-tokens-o-experimento.md).

## Vale instalar?

| Seu caso | Sugestão |
|---|---|
| Roda tarefas grandes com vários subagentes | Vale: uns 15% a menos, sem perda de qualidade nos testes |
| Bate no limite de uso nesse tipo de tarefa | Vale: 15% a menos é mais trabalho dentro do mesmo limite |
| Faz só tarefas pequenas e médias | Instale se quiser: custa quase nada, mas o ganho ali não está medido com clareza |

## Instalar

No **host**, trocando `~/dev-sandbox` pelo lugar onde você clonou o repositório:

```bash
~/dev-sandbox/utils/skills/install-skill.sh token-economy
```

Vai só o `SKILL.md`, que é o que o Claude usa. Os testes e resultados
(`evals/`, `benchmarks/`) ficam no dev-sandbox. Para atualizar, rode de novo.

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
