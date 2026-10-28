# Claude Code por baixo dos panos

Como o Claude Code funciona por dentro: o que ele carrega, o que manda a cada
pedido, o que acontece quando a conversa enche e o que os subagentes recebem.
Cada arquivo é curto e responde **uma** pergunta.

Tudo foi conferido na [documentação oficial](https://code.claude.com/docs) em
outubro/2026 (Claude Code 2.1.310). Onde há dedução minha, está marcado.

## Leia nesta ordem

| Guia | Responde |
|---|---|
| [A janela de contexto](./janela-de-contexto.md) | O que o Claude "sabe" agora? O que fica lá dentro? |
| [Quando cada coisa carrega](./quando-cada-coisa-carrega.md) | O `CLAUDE.md` é relido a cada mensagem? Quando entram subpastas, rules, memória, skills? |
| [A cada pedido o contexto vai junto](./a-cada-mensagem-o-contexto-vai-junto.md) | Por que uma conversa longa fica cara? Cada ferramenta é um pedido novo? |
| [Cache de prompt](./cache-de-prompt.md) | Como o reenvio fica mais barato? O que quebra o cache? |
| [Quanto custa](./quanto-custa.md) | Quanto custa um turno em dólares? Assinatura ou chave de API? Onde vejo o meu consumo? |
| [Compactação](./compactacao.md) | O que acontece quando a conversa enche? O que sobrevive, o que se perde? |
| [Subagentes](./subagentes-o-que-herdam.md) | O subagente recebe o `CLAUDE.md`? E o que eu disse na conversa? |
| [Vários pedidos de uma vez](./varios-pedidos-de-uma-vez.md) | Juntar pedidos relacionados economiza? |
| [Tarefa grande: conversa ou partes](./tarefa-grande-conversa-ou-em-partes.md) | Por que traduzir um arquivo dentro da conversa gasta tanto? |

## Em uma frase cada

- O `CLAUDE.md` é lido **uma vez**, no início da sessão. Mas a conversa inteira,
  inclusive ele, **vai junto a cada pedido** (e o cache torna isso mais barato).
- Cada uso de ferramenta é um pedido novo com o contexto inteiro.
- Compactar resume a conversa. O que precisa sobreviver deve estar no `CLAUDE.md`.
- O subagente recebe o `CLAUDE.md`, mas **não** a sua conversa.

Relacionados: [memória e instruções](../memoria-e-instrucoes.md),
[sessões e persistência](../sessoes-e-persistencia.md),
[modelo e esforço](../modelo-e-esforco.md).
