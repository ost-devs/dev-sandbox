# Bati no limite de uso: o que fazer

Este guia responde: qual limite eu atingi, o que devolve o acesso, o que não
adianta e como não perder o trabalho no dev-sandbox. Vale para quem usa o
Claude Code com uma **assinatura** (Pro, Max, Team). Com chave de API não há
janela de uso: paga-se por token ([quanto custa](./por-baixo-dos-panos/quanto-custa.md)).

## Qual limite é

A mensagem diz qual é e quando volta:

| Mensagem | Limite | Trocar de modelo (`/model`) adianta? |
|---|---|---|
| `You've hit your session limit · resets 3:45pm` | Janela de **5 horas** | Não: vale para todos os modelos |
| `You've hit your weekly limit · resets Mon 12:00am` | Janela **semanal** | Não: vale para todos os modelos |
| `You've hit your Opus limit` ou `...Sonnet limit` | Limite **de uma família** de modelos | **Sim**: troque para um modelo de outra família e a sessão continua |

As janelas são da sua **conta**: o chat do claude.ai, o Cowork e o Claude
Code gastam da mesma. Se o limite volta às 15h45, é uma pausa para o café.
Se volta na segunda-feira, planeje o resto da semana.

Trocar de modelo tem um custo escondido: cada modelo tem o seu cache, então o
pedido seguinte relê a conversa inteira sem desconto
([cache de prompt](./por-baixo-dos-panos/cache-de-prompt.md)). Troque entre
tarefas, depois de um `/clear`.

## Ver o medidor antes de supor

`/usage` mostra as barras da janela de 5 horas e da semanal, e quanto do uso
recente veio de cada skill, subagente, plugin e servidor MCP. `d` mostra as
últimas 24 horas, `w` os últimos 7 dias. Ele também recomenda mudanças para
o que responde por 10% ou mais do uso recente, como contexto longo ou cache
perdido.

O detalhamento vem do histórico de sessões **desta máquina**: o que você fez
no claude.ai ou em outro computador gastou a janela, mas não aparece. No
dev-sandbox, o `~/.claude` do host é montado no container, então as sessões
do host e as do container aparecem juntas (dedução: a documentação fala em
histórico local, e é o mesmo `~/.claude`).

## O que devolve o acesso

| Opção | Como | Observação |
|---|---|---|
| Esperar | O horário está na mensagem | `/clear`, conversa nova ou apagar conversas **não** devolvem nada: o uso é da conta |
| Deixar o Claude esperar e continuar | Numa sessão interativa aberta, com o limite voltando em até 24 horas, ele espera e continua a tarefa sozinho (Claude Code 2.1.234 ou mais novo). Limite mais distante: escolha "Wait here, then continue automatically" em `/rate-limit-options` | Não funciona em `claude -p`, em sessões em background nem com chave de API. Liga e desliga em `/config` ("Continue automatically at usage limit") |
| Créditos de uso | `/usage-credits` (precisa estar logado com a assinatura, não com chave de API). O teto mensal fica em Settings > Usage no claude.ai | Cobra nos preços da API. A partir daí, o cache da conversa cai de 1 hora para 5 minutos |
| Trocar de modelo | Só no limite de uma família (tabela acima) | |

Para não ficar com o terminal aberto esperando, rode o `dev-docker` dentro de
um `tmux` no host ([passo a passo](./projetos.md#6-sessões-longas-e-limites-de-uso)),
ou saia e retome depois com `claude --continue`
([sessões e persistência](./sessoes-e-persistencia.md#retomar-trabalho-em-vez-de-esperar-com-o-terminal-aberto)).

## Para durar mais da próxima vez

| Hábito | Por quê |
|---|---|
| Sonnet para o dia a dia, Opus quando travar numa decisão | O padrão do Claude Code é o Opus 5.5, que gasta a janela mais rápido ([modelo e esforço](./modelo-e-esforco.md)) |
| `/clear` entre assuntos | Uma pergunta de uma linha numa sessão aberta desde cedo relê a sessão inteira. `/clear` não custa nada |
| `/compact` só no meio de uma tarefa | Compactar lê a conversa toda: num contexto grande, é um pedido grande |
| Esforço menor em tarefas simples (`/effort`) | O raciocínio é cobrado como saída, a parte mais cara, e não dá para desligá-lo nos modelos atuais |
| Testes e logs longos num subagente | A saída bruta fica no contexto dele; só o resumo volta |
| Modo de plano antes de mudança grande (Shift+Tab alterna os modos até chegar nele) | Um caminho errado custa um plano, não horas de edição |

## Armadilha: uma chave de API esquecida

Se a variável `ANTHROPIC_API_KEY` existir, o Claude Code pode usá-la no lugar
da assinatura, e você paga por token sem perceber:

- numa sessão interativa, ele pergunta **uma vez** se deve usar a chave e
  lembra a resposta (muda em `/config`, "Use custom API key");
- com `claude -p`, ele **sempre** usa a chave, sem perguntar.

No dev-sandbox, o `dev-docker` não repassa variáveis do host para o
container ([`dev-docker`](../../dev-docker), as linhas `--env`). A chave só
aparece se alguém a definir **dentro** do container, por exemplo no
`.bashrc` da home persistente. Para conferir qual credencial está em uso:
`/status`.

## Fontes

Pontos de partida, adaptados e conferidos fato a fato:
[Limite do Claude atingido: o que fazer agora](https://www.ssdnodes.com/learn/lang/pt/claude-limit-reached-what-to-do)
(Matt Connor, SSD Nodes, 21/10/2026) e
[Qual modelo Claude usar?](https://www.ssdnodes.com/learn/lang/pt/opus-sonnet-haiku-which-model)
(23/07/2026; preços e modelos desatualizados, e erra ao dizer que trocar de
modelo não invalida o cache de forma documentada).

Conferido em outubro/2026 (Claude Code 2.1.310):
[erros e limites](https://code.claude.com/docs/en/errors#youve-hit-your-session-limit),
[custos](https://code.claude.com/docs/en/costs),
[modo interativo: esperar o limite](https://code.claude.com/docs/en/interactive-mode#wait-for-a-usage-limit-to-reset),
[autenticação](https://code.claude.com/docs/en/authentication),
[variáveis de ambiente](https://code.claude.com/docs/en/env-vars),
[prompt caching: trocar de modelo](https://code.claude.com/docs/en/prompt-caching#switching-models),
[configuração de modelo](https://code.claude.com/docs/en/model-config),
[modo interativo: atalhos](https://code.claude.com/docs/en/interactive-mode).

Ficaram de fora por não terem fonte oficial: os "resets grátis" e os créditos
mensais de API do Max cobrindo o `claude -p`.
