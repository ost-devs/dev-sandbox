# Qual modelo e qual esforço usar (esboço)

> Status: **esboço para lapidar com experiência**. A parte "o que a
> documentação diz" vem das fontes oficiais lidas em outubro/2026
> ([configuração de modelo](https://code.claude.com/docs/en/model-config),
> [artigo do time do Claude Code](https://claude.com/blog/claude-model-and-effort-level-in-claude-code),
> 7/jul/2026). A parte "projeção" é análise, não medição: está aqui para ser
> confirmada ou derrubada pelo [diário de campo](#diário-de-campo) e pelas
> [experiências da comunidade](#compartilhe-a-sua).

## O princípio: duas variáveis, e a bazuca

São duas escolhas independentes:

- **Modelo ≈ quão capaz.** "Modelos menores para tarefas rotineiras, maiores
  para tarefas complexas ou ambíguas."
- **Esforço ≈ quão minucioso.** "O nível de esforço controla quanto trabalho o
  Claude faz no pedido como um todo", não só quanto ele "pensa".

Os nomes dos modelos mudam várias vezes por ano; as faixas ficam. Pense em
faixas e confira no `/model` qual modelo está em cada uma hoje:

| Faixa | Alias no Claude Code | Hoje (out/2026, API Anthropic) | Para |
|---|---|---|---|
| Rápido | `haiku` | Haiku 5.5 | tarefas simples, muito volume |
| Generalista | `sonnet` | Sonnet 5.5 | o dia a dia de código |
| Especialista | `opus` | Opus 5.5 (o padrão nos planos Pro, Max, Team e Enterprise) | raciocínio complexo |
| Topo | `fable` (ou `best`) | Fable 5.1 | os problemas mais difíceis e mais longos; nos planos por assinatura é cobrado em créditos de uso, e o `/model` mostra "Requires usage credits" |

Um modelo de topo com outro nome, de outra oferta ou de um acesso especial,
cabe na mesma tabela: o raciocínio abaixo é sobre faixas, não sobre nomes.
Exemplo: os modelos **Mythos** (Mythos 5.1, Mythos 5, Mythos Preview) têm a
mesma capacidade do Fable, mas só para organizações verificadas pela
Anthropic, e não aparecem no `/model` do Claude Code (conferido em 28/out/2026
nas páginas de [escolha de modelo](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
e de [configuração de modelo](https://code.claude.com/docs/en/model-config)).
Se for o seu caso, ponha-o na faixa de topo e registre no diário.

Não usar bazuca para matar mosca já é meio caminho: o modelo maior e o
esforço máximo **não** são sempre melhores. A própria documentação avisa que
`max` "pode ter retorno decrescente e tende a pensar demais".

## O que a documentação diz

**Níveis de esforço** (Opus 5.5, Sonnet 5.5, Haiku 5.5 e Fable têm todos):

| Nível | Para (texto oficial, traduzido) |
|---|---|
| `low` | trocas rápidas em que você revisa cada resultado: brainstorm, primeiro rascunho, mudança pequena como um rename |
| `medium` | **padrão** no Opus 5.5, Sonnet 5.5 e Haiku 5.5. No Opus e no Sonnet, serve para o trabalho de engenharia do dia a dia com escopo claro, como implementar uma feature |
| `high` | trabalho em que verificar importa ou casos de borda são prováveis, como corrigir um bug numa base de código existente |
| `xhigh` | raciocínio mais profundo, com mais tokens |
| `max` | problemas difíceis que você quer que o Claude resolva sem você, como achar vulnerabilidades de segurança. Teste antes de adotar em geral |

"Ultracode" não é um nível de esforço: é um modo em que o Claude orquestra
fluxos com vários subagentes, no esforço da sessão.

**Calibração oficial:** "Opus 5.5 em `medium` iguala ou supera Opus 5 em
`high`" nas avaliações de código da Anthropic. O padrão `medium` não é
economia de qualidade: é o ponto em que o modelo escala o gasto conforme a
tarefa.

**Sinais para mudar** (do artigo do time):

1. **Antes de mexer em qualquer um:** olhe o contexto (o pedido, as
   ferramentas, as skills). Muitas falhas são de contexto, não de modelo.
2. **Errou por pular algo** (um arquivo, os testes, um passo de um refactor
   longo) → **mais esforço**.
3. **Tinha o contexto, tentou de verdade e errou mesmo assim**, ou erra com
   confiança qualquer que seja o contexto → **modelo maior**.
4. Use o esforço como **preferência geral**, não decidida tarefa a tarefa.

**Custo:** modelo maior custa mais por token, mas numa tarefa difícil "o custo
total por tarefa pode sair menor" (menos voltas). O esforço molda o consumo,
não o limita. Nos planos por assinatura, sessões, subagentes e sessões na
nuvem gastam o mesmo limite de uso. Preços e a conta de um turno:
[quanto custa](./por-baixo-dos-panos/quanto-custa.md).

O modelo barato sai caro quando **verificar a resposta é difícil**: cada
tentativa errada volta como contexto na seguinte, e no fim você sobe de
modelo do mesmo jeito (o argumento é do artigo
[Qual modelo Claude usar?](https://www.ssdnodes.com/learn/lang/pt/opus-sonnet-haiku-which-model),
da SSD Nodes; os preços dele, de julho, estão velhos). Se o erro aparece num
segundo, vá de modelo pequeno; se exige ler um diff com cuidado, não.

Troque de modelo **entre tarefas**, depois de um `/clear`: cada modelo tem o
seu cache, e trocar no meio da conversa relê tudo sem desconto
([prompt caching](https://code.claude.com/docs/en/prompt-caching#switching-models)).

## Como trocar

| Onde | Como |
|---|---|
| Na sessão | `/model` (as setas mudam o esforço), `/effort high`, `/effort auto` (volta ao padrão) |
| Ao abrir | `claude --model opus --effort high` |
| Sempre | `effortLevel` em `~/.claude/settings.json` (aceita até `xhigh`; `max` não), ou a variável `CLAUDE_CODE_EFFORT_LEVEL` |
| Por subagente ou skill | `model:` e `effort:` no cabeçalho do arquivo do agente ou da skill |
| Planejar num, executar noutro | `/model opusplan`: Opus no modo de planejamento, Sonnet na execução |

## Projeção (análise; para confirmar no campo)

Ponto de partida, sempre no padrão primeiro e subindo só com um dos sinais
acima:

| Tarefa | Começar com | Subir para | Sinal para subir |
|---|---|---|---|
| Rename, ajuste pequeno, pergunta sobre o código | generalista, `low`/`medium` | — | quase nunca |
| Feature com escopo claro, docs, scripts | especialista ou generalista, `medium` | `high` | pulou testes ou arquivos |
| Bug numa base existente, refactor com casos de borda | especialista, `high` | `xhigh` | corrigiu o sintoma, não a causa |
| Desenho com decisões ambíguas (arquitetura, layout de repositório, convenções) | especialista, `high` | topo | trocou de ideia várias vezes sem nova evidência |
| Trabalho longo e autônomo (auditoria, migração grande) com subagentes | sessão principal especialista `high`; subagentes por papel | subagentes de leitura em `medium`, verificador em `high` | o verificador acha erros sistemáticos de um papel |
| Busca de vulnerabilidades, problema que ninguém resolveu | especialista `xhigh`/`max`, ou topo | — | — |

Duas hipóteses ainda sem teste:

- Para tarefas de desenho, **mais esforço reduz voltas** mais do que um
  modelo maior (o erro típico é decidir rápido demais, não faltar capacidade).
- Em fluxos com muitos subagentes, **o esforço dos subagentes pesa mais no
  limite de uso** do que o da sessão principal, porque são muitos.

## Diário de campo

Registre aqui o que acontece de verdade. Compare com a projeção: onde bate,
onde não bate, e os cenários que ela nem previu.

| Data | Tarefa (tipo da tabela acima) | Modelo / esforço | Resultado | Uso (tokens, % do limite, tempo) | Bate com a projeção? O que eu aprendi |
|---|---|---|---|---|---|
| 2026-10 | Sessão longa de docs e infraestrutura: diagnóstico de disco, revisão de um sandbox Docker, reorganização de instruções para IA e dos espelhos de um projeto | Opus 5.5 / `medium` | bom no fim; no desenho do caminho dos espelhos mudou de ideia três vezes antes de medir, e só acertou depois de levantar os fatos | não medido | Em parte: o escopo parecia claro e não era. A projeção diria `high` para "desenho com decisões ambíguas"; se teria evitado as voltas, ainda é hipótese |
| 2026-10 | Tarefas grandes (ex.: implementação de auditoria) | Opus 5.5 / `high` | "fabuloso" (relato do mantenedor) | — | Bate |
| | | | | | |

## Compartilhe a sua

Abra uma *issue* com o modelo **"Experiência: modelo e esforço"** (ou uma
discussão, se o repositório tiver Discussions ligado) contando tarefa, plano,
modelo, esforço e resultado. Com experiências suficientes, a projeção acima
vira uma tabela baseada em evidência.
