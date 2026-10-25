# A cada pedido, o contexto inteiro vai junto

O modelo de IA **não guarda memória entre um pedido e outro**. Para ele
"lembrar" da conversa, o Claude Code manda a conversa inteira de novo, toda vez.

> "The model doesn't remember anything between requests, so Claude Code
> re-sends the full context: the system prompt, your project context, every
> prior message and tool result, and your new message."
> (página de [prompt caching](https://code.claude.com/docs/en/prompt-caching))

Isso vale para **cada mensagem sua** e também para **cada uso de ferramenta**:

> "Claude Code sends your full conversation with every request, and each time
> Claude uses tools it sends another request carrying that batch of tool results."
> (página de [custos](https://code.claude.com/docs/en/costs))

## Exemplo

Você escreve: "corrija os testes que falham". Para resolver, o Claude faz:

| Passo | O que o Claude Code envia |
|---|---|
| 1. Rodar os testes | conversa inteira + sua mensagem |
| 2. Ler o erro e abrir um arquivo | conversa inteira + resultado do passo 1 |
| 3. Editar o arquivo | conversa inteira + o arquivo lido |
| 4. Rodar os testes de novo | conversa inteira + a edição |
| 5. Responder a você | conversa inteira + o resultado |

Uma mensagem sua virou **cinco pedidos**, e cada um leva tudo o que veio antes.

## Então o custo explode?

Não tanto, graças ao **cache de prompt**
([como funciona](./cache-de-prompt.md)). A parte repetida é relida a um preço
menor ("cached token rate"), em vez de ser processada do zero. Mesmo assim:

- o custo **cresce junto com o tamanho do contexto**;
- uma pergunta de uma linha, numa sessão aberta o dia todo, ainda gasta o
  equivalente a reler a sessão inteira:

> "a one-line question in a session that has been open all day still draws
> usage for the whole conversation."

## O que mais pesa numa sessão longa

A documentação de custos lista, entre outros motivos para o uso subir:

- **contexto longo**: tudo acima;
- **cache perdido**: a primeira mensagem depois de uma pausa maior que a vida
  do cache reprocessa o contexto todo;
- **subagentes**: cada um faz seus próprios pedidos, além dos da conversa principal;
- **tarefas agendadas e check-ins** numa sessão parada: cada disparo manda o contexto inteiro;
- **compactação**: resumir um contexto grande é, ela mesma, um pedido grande.

## O que fazer com isso

- Troque de assunto com `/clear` (use `/rename` antes se quiser voltar depois).
- Peça coisas específicas: "adicione validação na função de login em `auth.ts`"
  faz menos leituras que "melhore o código".
- Veja [vários pedidos de uma vez ou um por um](./varios-pedidos-de-uma-vez.md).

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[custos](https://code.claude.com/docs/en/costs).
