# Quanto custa uma sessão (e o que faz o valor subir)

Os guias anteriores explicam **por que** uma conversa longa fica cara: o
contexto inteiro vai junto a cada pedido
([entenda](./a-cada-mensagem-o-contexto-vai-junto.md)), e o cache barateia a
parte repetida ([como](./cache-de-prompt.md)). Este guia põe **números**
nisso: preços, a conta de um turno e onde ver o seu consumo.

Valores de outubro/2026. Preços mudam: confira na página oficial (em
[Fontes](#fontes)) antes de decidir algo grande.

## Os preços

Em dólares por milhão de tokens, na API:

| Modelo | Entrada | Saída | Leitura do cache |
|---|---|---|---|
| Fable 5.1 | $10 | $50 | 0,025× a entrada ($0,25) |
| Opus 5.5 | $4 | $20 | 0,05× ($0,20) |
| Sonnet 5.5 | $2 | $10 | 0,05× ($0,10) |
| Haiku 5.5 (prompt até 100 mil tokens) | $0,10 | $0,50 | 0,1× ($0,01) |
| Haiku 5.5 (prompt acima de 100 mil) | $0,50 | $2,50 | 0,1× ($0,05) |

- A **saída custa 5 vezes a entrada** em todos esses modelos.
- **Gravar** no cache custa 1,25× a entrada (cache de 5 minutos) ou 2× (cache
  de 1 hora). Ler sai por uma fração: a última coluna.
- Um token tem uns 3,5 caracteres de texto em inglês nos modelos antigos.
  A partir do Opus 4.7, o tokenizer novo gera **cerca de 30% mais tokens**
  para o mesmo texto. Contas feitas com `tiktoken` (da OpenAI) não valem para
  o Claude.

## O que entra na conta

| Parcela | O que é | No dev-sandbox |
|---|---|---|
| Entrada | Instruções, ferramentas, tudo o que foi lido e a conversa até agora | Inclui o `/etc/claude-code/CLAUDE.md` da imagem e o `CLAUDE.md`/`AGENTS.md` do projeto, em todo pedido |
| Ferramentas MCP | Só os nomes e as instruções de cada servidor, até a ferramenta ser usada | Cada servidor MCP ligado soma um pouco a todo pedido |
| Saída de comandos | Até ~30 mil caracteres entram direto; acima disso, vai para um arquivo e entra uma prévia de 2 mil | Uma suíte de testes que imprime muito pesa em todo pedido seguinte. Comando que falha mostra ~10 mil caracteres |
| Saída | O que o Claude escreve **e o raciocínio**, mesmo quando ele não aparece na tela | Não dá para desligar o raciocínio no Opus 5.5, Sonnet 5.5, Haiku 5.5 e Fable. O controle é o esforço ([modelo e esforço](../modelo-e-esforco.md)) |

O limite de 30 mil caracteres muda com a variável `BASH_MAX_OUTPUT_LENGTH`
(até 150 mil).

## A conta de um turno

```text
custo do turno = entrada nova           × preço de entrada
               + gravação no cache      × 1,25 × preço de entrada   (2× no cache de 1 hora)
               + leitura do cache       × multiplicador × preço de entrada
               + saída (com raciocínio) × preço de saída
```

Exemplo (conta minha, com os preços acima): um turno no meio da sessão, com
80 mil tokens de contexto, sendo 75 mil lidos do cache, 3 mil gravados, 2 mil
novos e 1.500 de saída. Cache de 5 minutos.

| | Opus 5.5 | Sonnet 5.5 |
|---|---|---|
| Cache **quente** (leu os 75 mil) | ~$0,07 | ~$0,03 |
| Cache **frio** (pausa maior que o TTL: grava os 78 mil de novo) | ~$0,43 | ~$0,21 |
| Quanto o cache frio custa a mais | ~6 vezes | ~6 vezes |

Cinquenta turnos assim, com cache quente, somam uns $3,40 no Opus 5.5. Para
comparar: a média que a Anthropic publica para empresas é de **~$13 por
desenvolvedor por dia de uso** (90% ficam abaixo de $30).

## Assinatura ou chave de API

| | Assinatura (Pro, Max, Team) | Chave de API ou nuvem |
|---|---|---|
| Como paga | Desconta de uma janela de **5 horas** e de uma **semanal**, compartilhadas com o chat do Claude e entre todos os modelos | Por token, nos preços acima |
| Trocar de modelo ao bater o limite | Só adianta no limite de uma família (`Opus limit`, `Sonnet limit`); nas janelas de 5 horas e semanal, não ([limite de uso](../limite-de-uso.md)) | Não se aplica |
| Cache da conversa principal | **1 hora** dentro do uso do plano; **5 minutos** ao passar a usar créditos de uso | **5 minutos**. `promptCacheTtl: "1h"` pede 1 hora, com gravação a 2× |
| O valor em dólares do `/usage` | Só informativo | Estimativa; a fatura oficial está na Console |
| Passou do limite | `/usage-credits` configura créditos de uso | Não se aplica |

Os créditos mensais de API que vêm com o Max e o Team servem para os **seus**
programas na API, não para o Claude Code. E o Fable, dependendo do plano, pode
ser cobrado de créditos de uso em vez do limite do plano.

## Ver o seu consumo

| Comando | Mostra |
|---|---|
| `/usage` (ou `/cost`) | Tokens da sessão e uma estimativa em dólares feita localmente, a preço de tabela. Na assinatura: as barras do limite e quanto gastaram skills, subagentes, plugins e servidores MCP |
| Linha `Prompt cache (main)` do `/usage` | Quanto da entrada veio do cache e se ele está quente agora (Claude Code 2.1.251 ou mais novo) |
| `/context all` | O que ocupa a janela agora, item por item: instruções, ferramentas, MCP, arquivos, conversa |

## O que reduz o custo no dev-sandbox

| Situação | Faça |
|---|---|
| Pausa no meio do trabalho com chave de API | O cache de 5 minutos expira: a mensagem seguinte grava tudo de novo (~6 vezes o turno). Trabalhe em blocos, ou use `promptCacheTtl: "1h"` |
| Pesquisar documentação | Use o espelho local com `grep` em vez de buscar páginas na web: ~700 tokens em vez de ~30 mil ([base de conhecimento](../base-de-conhecimento.md)) |
| Ler muitas fontes para uma resposta curta | Um subagente lê no contexto dele e devolve só a conclusão. Ele também custa: o pesquisador gastou 58 mil tokens para conferir 17 fatos (medido em outubro/2026) |
| Sessões em paralelo | Na **mesma pasta**, elas podem aproveitar o cache uma da outra; em pastas diferentes, não ([escopo do cache](./cache-de-prompt.md#escopo-do-cache)) |
| Testes que imprimem muito | Peça para filtrar ("rode e mostre só as falhas") ou crie um hook que filtre: a saída longa é paga em todo pedido seguinte |
| Assunto novo | `/clear`. Numa tarefa longa, `/compact` com um foco |

## Fontes

Ponto de partida: o artigo
[O que são tokens no Claude Code? Veja a conta](https://www.ssdnodes.com/learn/lang/pt/claude-code-token-usage-explained)
(Matt Connor, SSD Nodes, 24/10/2026), adaptado e conferido fato a fato.

Conferido em outubro/2026 (Claude Code 2.1.310) nas páginas oficiais:
[preços](https://platform.claude.com/docs/en/about-claude/pricing),
[raciocínio](https://platform.claude.com/docs/en/build-with-claude/thinking),
[prompt caching da API](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
[contagem de tokens](https://platform.claude.com/docs/en/build-with-claude/token-counting),
[glossário](https://platform.claude.com/docs/en/about-claude/glossary),
[créditos de API para assinantes](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers),
[custos do Claude Code](https://code.claude.com/docs/en/costs),
[prompt caching do Claude Code](https://code.claude.com/docs/en/prompt-caching),
[ferramentas](https://code.claude.com/docs/en/tools-reference),
[configuração de modelo](https://code.claude.com/docs/en/model-config),
[comandos](https://code.claude.com/docs/en/commands).

Contas minhas: os valores do exemplo e o "~6 vezes". O "~700 tokens em vez
de ~30 mil" é estimativa (4 caracteres por token).
