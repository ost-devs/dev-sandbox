# Como a `token-economy` foi feita e testada

Este artigo responde: de onde veio a skill
[`token-economy`](../../utils/skills/token-economy/SKILL.md), como ela foi
escrita, como foi testada e o que os números mostram, inclusive o que **não**
mostram. Para só usar a skill, leia o [guia](./economia-de-tokens.md).

**Conclusão atual:** em tarefa grande com 8 subagentes, a skill custou cerca de
15% menos, com a mesma qualidade. Em tarefa menor, não houve diferença clara.
O "39% mais barato" das primeiras rodadas não se confirmou: veja a
[rodada 4](#7-rodada-4-sonnet-mais-repetições-e-regra-escrita-antes).

As rodadas 1 a 3 foram feitas em 29/10/2026, com Opus 5.5. A rodada 4 foi feita
em 01/11/2026, com Sonnet 5.5. Todas usaram Claude Code 2.1.310. Os dados
brutos estão em [`benchmarks/`](../../utils/skills/token-economy/benchmarks/)
e cada teste pode ser repetido (veja [Repetir](#repetir)).

## 1. O problema: milhares de tokens queimados

Num projeto anterior do mantenedor (o *ferrum*, um port de bibliotecas para
Rust com auditoria de paridade), uma versão antiga do trabalho queimou
milhares de tokens. Parte foi planejamento ruim da IA, parte foi falta de
orientação. O diário do projeto (`LEARNINGS.md`, 26/10/2026) registrou:

| Lição | O que aconteceu |
|---|---|
| L2 | A auditoria de afirmações custou ~300 mil de ~2,35 milhões de tokens (13%). De 488 afirmações, 397 eram verdadeiras e só uma descoberta durou |
| L10 | 7 subagentes em paralelo bateram no limite de uso **ao mesmo tempo**. Só sobreviveu o que já estava gravado em arquivo |
| L11 | Cada subagente lia ~25 mil tokens de instruções |
| L16 | Montar o ambiente de cada subagente era barato. Caro era **cada um dos 6 escrever o seu** gerador de números, leitor de JSON, comparador e reexecutor |
| L17 | A sessão principal lia saídas enormes que só precisavam virar contagens |
| L18 | Cada lote custava 240 a 320 mil tokens, e ninguém mediu antes de dividir |

A regra que o projeto adotou depois foi: *"economia de tokens nunca vem antes
da qualidade do resultado"*.

## 2. A armadilha das duas direções

O mantenedor viu o risco da frase:

> só falar em economia de tokens levaria a IA a tomar péssimas decisões só
> para economizar tokens. Falar em qualidade (...) pode levar ela a querer
> queimar tokens só para garantir essa "qualidade".

E a regra do ferrum pende para o segundo lado: pode fazer a IA *"não buscar
meios eficazes que economizam tokens sem perda da eficácia do resultado"*.
O objetivo proposto foi outro:

> O mesmo resultado com menos tokens.

Daí a forma da skill. O resultado fica **fixo**; os tokens são a variável.
E ela nomeia os **dois** erros, para que fugir de um não empurre o Claude
para o outro:

- **Economizar cortando o resultado:** pular o passo que produz evidência,
  ler menos do que a tarefa precisa. O retrabalho custa mais.
- **Gastar por garantia:** checagens que nunca acham nada, ler tudo "por
  via das dúvidas", agentes demais. Custo sem resultado.

Essa lição virou regra para escrever qualquer skill deste repositório
([`.claude/rules/skills.md`](../../.claude/rules/skills.md)): *quando o
assunto pode dar errado em dois sentidos opostos, nomeie os dois*.

Outra preocupação: regras demais podem piorar o que o modelo já faz bem.
Por isso a skill é curta (cerca de 30 linhas), escrita para o modelo atual,
sem passo a passo que ele já saberia deduzir.

## 3. Rodada 1: só planos

O primeiro teste usou o método da skill `skill-creator` da Anthropic: o
mesmo pedido, uma vez **com** a skill e uma vez **sem**, e uma lista de
critérios verificáveis para cada caso. Três casos, cada um mirando um erro:

| Caso | Pedido (resumo) | Testa |
|---|---|---|
| Auditoria grande | Conferir 480 afirmações contra 12 crates Rust (60 mil linhas) com subagentes; só o plano | Se ela divide bem o trabalho |
| Gasto por garantia | Revisar 38 páginas, "roda cada verificação 3 vezes, cada um lê a documentação inteira, por garantia" | Se ela avisa do custo sem cortar a revisão |
| Corte de qualidade | "tô quase no limite... pode pular a rodada final dos testes, usar haiku em tudo e não precisa conferir nada" | Se ela protege o resultado sem desobedecer |

Resultado:

| Caso | Com a skill | Sem a skill |
|---|---|---|
| Auditoria grande | 6/6 | 3/6: sem lote-piloto medido, sem instruções montadas uma vez, sem gravação aos poucos |
| Gasto por garantia | 4/4 | 4/4 |
| Corte de qualidade | 4/4 | 3/4: aceitou o haiku sem discutir onde ele serve |
| **Total** | **14/14** | **10/14** |

Os planos ficaram melhores, mas os tokens ficaram iguais (~35 mil de cada
lado). Aqui veio a segunda lição: **um plano não gasta o que a execução
gasta**. Um teste que só pede planos mostra a qualidade, não o custo. Também
virou regra em `.claude/rules/skills.md`.

O mantenedor leu os planos e preferiu os da skill, porque ela manteve as
verificações por padrão e deixou a escolha com ele.

Depois, os planos foram relidos pelo conteúdo, e não pela nota. A nota de 14 a
10 exagerava a distância:

| Caso | Leitura do conteúdo |
|---|---|
| Auditoria grande | Com a skill, melhor na mecânica de custo (piloto, gravação aos poucos, limite de paralelos). Sem ela, mais rigoroso na verificação. Cada um ganhou em uma parte |
| Gasto por garantia | Empate |
| Corte de qualidade | Com a skill, claramente melhor: manteve os testes. Sem ela, obedeceu ao "haiku em tudo" e pulou os testes |

## 4. O que faltava: o orquestrador monta, os subagentes usam

Antes da rodada 2, a skill ganhou duas ideias do ferrum (L16 e a seção de
orquestração da auditoria de paridade):

- **Montar uma vez o que todos precisam.** Antes de abrir subagentes que
  fazem o mesmo tipo de trabalho, o orquestrador monta o ambiente e os
  ajudantes (gerador de entradas, executor, comparador) e um cartão curto
  de instruções. Cada subagente só roda a sua parte. Passar tudo pelo
  orquestrador seria pior: toda a saída cairia no maior contexto.
- **Evidência que qualquer um roda de novo.** Entradas geradas com semente
  registrada, cada checagem é um script. Rodar o script outra vez custa
  zero token de modelo; reler para conferir custa.

## 5. Rodada 2: execução de verdade

Um caso novo, feito para ser executado e corrigido por máquina:

- um pacote Python pequeno, `calc/`, com 4 módulos;
- 24 afirmações sobre ele, das quais **11 são falsas**, e só o gabarito
  ([`truth.json`](../../utils/skills/token-economy/evals/verify-claims-subagents/truth.json))
  sabe quais;
- o pedido: conferir todas **rodando o código**, com um subagente por
  módulo, cada veredito com uma checagem reproduzível.

Quatro sessões reais de `claude -p`, duas com a skill e duas sem, todas ao
mesmo tempo. Um script corrigiu os vereditos contra o gabarito e rodou
**duas vezes** cada comando de reprodução, para ver se dava o mesmo resultado.

| | Com 1 | Com 2 | Sem 1 | Sem 2 |
|---|---|---|---|---|
| Vereditos certos | 24/24 | 24/24 | 24/24 | 24/24 \* |
| Checagens estáveis rodando 2 vezes | 24/24 | 24/24 | 24/24 | 24/24 |
| Ajudantes montados uma vez | sim | sim | não | não |
| Custo | US$ 0,75 | US$ 0,67 | US$ 1,22 | US$ 1,09 |
| Tokens de saída | 17,4 mil | 15,5 mil | 27,3 mil | 25,0 mil |
| Tempo | 114 s | 84 s | 134 s | 125 s |

\* Esta sessão marcou também a afirmação C2 como falsa (a função quebra com
itens que não podem virar chave de dicionário). É uma leitura mais rígida,
e dá para defender.

**Em média: 39% mais barato e 38% menos tokens de saída, com o mesmo
resultado.** A [rodada 4](#7-rodada-4-sonnet-mais-repetições-e-regra-escrita-antes)
não confirmou esse número.

### O que a skill mudou

Com ela, o orquestrador escreveu `checks/harness.py` (gerador com semente,
executor e formato de saída únicos) **antes** de abrir os subagentes. Numa
das sessões escreveu também um cartão de instruções e um `run_all`. Os
subagentes só escreveram as próprias checagens.

Sem ela, o orquestrador só combinou a semente e o formato no texto do pedido,
e **cada subagente escreveu o seu gerador e o seu executor**. Foi o L16 do
ferrum se repetindo, agora medido.

### O que confunde a conta

- **O modelo dos subagentes.** Com a skill, o orquestrador escolheu o Sonnet
  para os subagentes. A skill não fala de modelo. Parte da economia em
  dólares vem daí. Refazendo a conta como se tudo fosse Opus, a diferença
  cai para uns 10%. Os tokens de saída caíram 38%, mas o total ficou igual.
- **O total de tokens engana.** Somando tudo, os dois lados ficam perto de
  650 mil. Quase tudo é leitura de cache, que custa um décimo do preço
  normal ([cache de prompt](./por-baixo-dos-panos/cache-de-prompt.md)).
  O que pesa no custo é a saída.
- **As mensagens finais erraram a contagem.** As 4 sessões disseram 12, 13
  ou 14 falsas no chat, mas as tabelas do `report.md` estavam certas, com
  11. Quem confere o relatório pelo resumo do chat se engana com ou sem a
  skill.

## 6. Rodada 3: ela entra quando deve?

Uma skill que não entra não economiza nada. Uma que entra em tudo custa
contexto à toa. Foram montados 20 pedidos realistas
([`trigger-eval.json`](../../utils/skills/token-economy/evals/trigger-eval.json)):
10 que deveriam acionar a skill e 10 parecidos que não deveriam (preço do
Opus, prompt caching na API, statusline com custo, bundle do Next, query
lenta no Postgres, um contador de tokens num app).

### Um tropeço do método

O script de acionamento do `skill-creator` deu **0 de 60**, inclusive nos
pedidos óbvios. Suspeito, e era o método: ele não instala a skill, cria um
comando falso em `.claude/commands`, e nesta versão do Claude Code o modelo
nunca o chamou. Além disso, ele só conta a skill se ela for a **primeira**
ferramenta usada.

O teste foi refeito com a skill **instalada de verdade**, anotando cada
ferramenta que o modelo chamou:

| | Execuções | Acionou |
|---|---|---|
| Não deveriam acionar | 19 | **0** (dois foram para a `claude-api`, como deviam) |
| Deveriam acionar | 16 | **9** |

Nos que ficaram de fora (a auditoria do port em Rust e a tradução de 95
arquivos), o modelo começou explorando os arquivos. A descrição dizia
"use ao **planejar**", e diante de "traduz os 95 arquivos" ele não se via
planejando. Ela passou a dizer "ao **executar ou planejar**".

O mantenedor parou por aí: nenhum falso acionamento é o que mais importa, e
quem quiser a skill sempre pode pedi-la (`/token-economy ...`) ou mandar
usá-la no `CLAUDE.md` do seu projeto ([guia](./economia-de-tokens.md#ajustar-ao-seu-projeto)).

## 7. Rodada 4: Sonnet, mais repetições e regra escrita antes

As rodadas anteriores tinham dois extremos: casos absurdos, que o treino normal
do modelo já pega, ou um caso real pequeno demais, com 2 execuções de cada
lado. O mantenedor pediu um teste mais realista, com amostra suficiente para um
veredito, *"sem viés de confirmação"*: *"a fonte da verdade são os dados"*.

### Como foi feito

- **Caso novo:** 152 afirmações, 39 delas falsas, sobre 8 módulos, com um
  subagente por módulo. É grande o bastante para pesar o custo fixo de cada agente.
- **Interrupção simulada:** um vigia matava a execução inteira ao passar de
  metade do custo médio. Depois, a sessão era retomada com o pedido de continuar.
- **Caso anterior repetido:** as 24 afirmações da rodada 2, agora 6 vezes de
  cada lado.
- **Sonnet em tudo**, para o modelo não misturar as causas.
- **Regra de decisão escrita antes do lote:** razão entre as médias, com
  intervalo de 95%. Abaixo de 0,5 é abismo; de 0,5 a 0,75, grande diferença;
  de 0,75 a 0,9, diferença pequena; de 0,9 a 1, quase páreo.

O piloto de cada caso não entrou no lote. O grupo sem skill foi conferido
execução por execução: a skill não apareceu em nenhuma.

### Resultado

| Tarefa | Execuções | Custo com ÷ sem (unidades) | Intervalo de 95% | p | Em dólar | Qualidade | Veredito pela regra |
|---|---|---|---|---|---|---|---|
| 152 afirmações | 4+4 | **0,87** | 0,83 a 0,91 | 0,029 | 0,85 | 152/152 em todas | Diferença pequena a favor da skill |
| 152 afirmações, interrompida | 4+4 | **0,82** | 0,69 a 0,97 | 0,114 | sem dado | 152/152 em todas | Diferença pequena, evidência fraca |
| 24 afirmações | 6+6 | **1,08** | 0,93 a 1,32 | 0,738 | 0,88 | 24/24 em todas | Inconclusivo |

"Unidades" é o custo em tokens com o peso de preço de cada tipo. Só é proporcional
ao custo em dólar quando há um único modelo.

### O que os números mostram

- **Não é abismo, mas é ganho.** "Diferença pequena" é a faixa da régua, não um
  juízo de valor: 13% a 15% a menos, com o mesmo resultado e quase nenhum custo
  de contexto, é economia que vale ter. Na tarefa grande, as 4 execuções com a
  skill saíram mais baratas que as 4 sem ela (16 de 16 pares). Com 4+4,
  p=0,029 é o menor valor possível, então a amostra não permite mais precisão.
- **A direção é a mesma, a força não.** Ganhando em pares de execuções: 16 de 16
  na tarefa grande, 14 de 16 na interrompida e, na de 24 afirmações, 25 de 36 em
  dólar e 17 de 36 em unidades, que é cara ou coroa. Em dólar, nenhum grupo ficou
  com média pior com a skill. Na tarefa menor, quase todo o ganho em dólar vem da
  execução no Haiku: sem ela, a razão fica em 0,96.
- **O piloto exagerou:** deu 0,72 numa execução de cada lado. Com mais
  execuções, ficou em 0,87.
- **A perda ao retomar não mudou de forma comprovada.** Custou 21% a mais com a
  skill e 29% a mais sem ela. Com só 4 execuções, essa distância fica dentro do
  ruído. Era a hipótese principal da interrupção, e ela não se confirmou.
- **Montar ajudantes uma vez nem sempre compensa.** Nas 24 afirmações, a skill
  fez os ajudantes compartilhados nas 6 execuções, e o grupo sem skill em nenhuma.
  Mesmo assim, não houve diferença clara. Com 4 módulos, os tokens que a IA
  gasta escrevendo os ajudantes podem empatar com os que ela economiza depois
  (dedução, não medição).

### Uma correção da regra

Em uma execução com a skill, o orquestrador mandou os subagentes para o Haiku.
Ela deu 295 mil unidades, mas custou só US$ 0,165, a mais barata de todas. Isso
explica por que unidades e dólar discordam na tabela. Sem essa execução, a razão
em unidades fica em 0,97.

A leitura em dólar foi incluída depois de ver esse caso, então é complementar.
O veredito segue a regra original. O motivo da escolha do Haiku não foi investigado.

### A hipótese do mantenedor

Ao ver os resultados, o mantenedor apontou que o Claude já parece bastante
competente, e que estes testes são objetivos e lógicos, justamente onde ele
brilha. Os dados combinam com isso: sem a skill, o Sonnet já paralelizou e
acertou tudo. Mas a rodada não testa o outro lado. Nenhum caso executado foi uma
tarefa aberta, sem gabarito. Não dá para dizer se ali a skill ajuda mais ou menos.
Há também um teto: com todo mundo acertando 100%, estes casos não conseguem
mostrar ganho de qualidade. O único indício fora da lógica pura é o plano do
corte de qualidade (rodada 1), a favor da skill, mas foi um caso só e não executado.

## 8. O que dá para concluir, e o que não

| Dá para dizer | Ainda não dá |
|---|---|
| Em tarefa grande com 8 subagentes no Sonnet, a skill custou uns 15% menos, sem perder qualidade | Que a economia vale para qualquer tarefa: foram 2 casos do mesmo tipo |
| O Sonnet sem a skill acertou tudo e já paralelizou quando o pedido mandou | Que a skill melhora a qualidade em execução: nos testes, os dois lados acertaram tudo |
| Em tarefa com 4 subagentes, o tamanho da economia não ficou claro | Se ela reduz a perda ao retomar depois de um limite |
| Nos planos, ela protegeu mais o resultado no caso de corte de qualidade | Se isso se repete quando o pedido é executado |
| Ela não entrou em nenhum pedido em que não devia | Se a nova descrição ("executar ou planejar") aciona mais |
| O método de acionamento do `skill-creator` não funciona nesta versão do Claude Code | Quanto ela rende em tarefas abertas, sem gabarito, ou com outros modelos |

Outro limite: o corretor confere os vereditos e repete os comandos, mas não
avalia a profundidade de cada verificação.

## Repetir

Os testes moram na pasta da skill:

| Pasta | O que tem |
|---|---|
| [`evals/`](../../utils/skills/token-economy/evals/) | Os 7 casos (pedido, critérios, arquivos de entrada, gabarito) e os 20 pedidos de acionamento |
| [`benchmarks/iteration-1/`](../../utils/skills/token-economy/benchmarks/iteration-1/) | Rodada 1: os planos, as notas e o `RUN.md` |
| [`benchmarks/iteration-2/`](../../utils/skills/token-economy/benchmarks/iteration-2/) | Rodada 2: relatórios, checagens, `result.json` de cada sessão e o comando exato no `RUN.md` |
| [`benchmarks/trigger-1/`](../../utils/skills/token-economy/benchmarks/trigger-1/) | Rodada 3: o script de acionamento e as ferramentas chamadas em cada execução |
| [`benchmarks/iteration-3/`](../../utils/skills/token-economy/benchmarks/iteration-3/) | Rodada 4: regra de decisão e resultados no `RUN.md`, `compare.json` e cada execução |
| [`benchmarks/harness/`](../../utils/skills/token-economy/benchmarks/harness/) | Rodada 4: scripts que rodam, corrigem e comparam (`small_batch.sh` repete o lote) |

As rodadas 1 a 3 têm uma página `review.html` com os pedidos, as saídas e as
notas lado a lado. O GitHub mostra só o código da página; abra no
navegador, **no host**:

```bash
xdg-open ~/dev-sandbox/utils/skills/token-economy/benchmarks/iteration-2/review.html
```

As checagens geradas na rodada 2 usam semente: dentro de
`benchmarks/iteration-2/verify-claims-subagents/with_skill/run-1/outputs/`,
`python3 checks/check_mathutil.py` dá a mesma saída sempre. As sessões do
modelo não têm semente: repetir dá planos e custos parecidos, não iguais.
Compare as taxas de acerto e os custos, não as palavras.

Para repetir a rodada 4, rode no container ou no host. O lote gasta o seu limite
de uso (cerca de US$ 18) e pula o que já tem resultado, então mova antes as
pastas de execução de `iteration-3/` ou copie o caso para outra iteração:

```bash
WORK_ROOT=~/.cache/token-economy-runs bash utils/skills/token-economy/benchmarks/harness/small_batch.sh
```
