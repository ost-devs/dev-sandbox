# Vários pedidos de uma vez ou um por um?

Pergunta: se eu tenho **coisas relacionadas** para pedir, é melhor mandar tudo
numa mensagem ou uma de cada vez?

> **Atenção ao que é fato e o que é dedução.** A documentação oficial **não
> traz uma regra nem um número** comparando as duas formas. Abaixo, a parte
> "O que a documentação diz" é citação; a parte "O que se deduz" é raciocínio
> em cima dela, e está marcada como tal.

## O que a documentação diz

1. Cada mensagem sua gera um novo pedido à API com o contexto inteiro
   ([a cada mensagem](./a-cada-mensagem-o-contexto-vai-junto.md)).
2. Cada uso de ferramenta dentro do trabalho do Claude também gera um pedido
   com o contexto inteiro.
3. O contexto repetido é lido do cache a um preço menor, mas "the first message
   after a break longer than the cache lifetime misses the cache and
   reprocesses your full context" ([cache](./cache-de-prompt.md)).
4. Pedidos específicos economizam: "Specific requests like 'add input
   validation to the login function in auth.ts' let Claude work efficiently
   with minimal file reads."
5. Trocar de assunto: use `/clear`, porque "stale context wastes tokens on
   every subsequent message".
6. Você pode **digitar uma mensagem enquanto o Claude trabalha**: ela fica na
   fila e ele a lê assim que as ferramentas em andamento terminam, dentro do
   mesmo turno, e ajusta antes do próximo passo.

## O que se deduz (não é citação)

- **Vários pedidos relacionados numa mensagem** poupam o "começo de turno" de
  cada um: menos mensagens separadas, menos releituras do contexto por causa
  delas, e o Claude planeja tudo junto.
- **Mas a economia tem limite.** O trabalho dentro de cada turno (cada leitura,
  edição ou comando) continua gerando pedidos. Juntar pedidos não reduz isso.
- **O fator dominante é o tamanho do contexto**, e não o número de mensagens.
  Uma sessão pequena com muitas mensagens pode custar menos do que uma sessão
  inchada com poucas.
- **Misturar assuntos sem relação** numa só mensagem enche o contexto de
  coisas que não se ajudam, e o que sobra depois vai junto a cada pedido
  seguinte. Para esses casos, a regra da documentação (5) é melhor: uma
  conversa por assunto, com `/clear` no meio.
- **Pausas** pesam mais que a forma de enviar: um pedido novo depois de uma
  pausa longa reprocessa tudo, não importa se foi um ou cinco itens.

## Guia prático (baseado nas duas partes acima)

| Situação | Sugestão |
|---|---|
| Itens relacionados (mesmo arquivo, mesma tarefa, passos de uma sequência) | Uma mensagem, numerada, com o resultado esperado de cada item |
| Itens sem relação | Conversas separadas, ou `/clear` entre eles |
| Lembrou de algo no meio do trabalho do Claude | Digite e envie: entra na fila |
| Vai ficar horas sem mexer na sessão | Considere `/compact` antes de sair, ou comece uma sessão nova depois |
| Tarefa em lote, repetitiva e independente | Veja [uma tarefa grande na conversa ou em partes independentes](./tarefa-grande-conversa-ou-em-partes.md) |

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[custos](https://code.claude.com/docs/en/costs),
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[como o Claude Code funciona](https://code.claude.com/docs/en/how-claude-code-works)
(seção *Interrupt and steer*).
