# O Write e o Edit do Claude se recusam a escrever num link simbólico

- **Data:** 2026-10
- **Ambiente:** Claude Code 2.1.310, dentro do dev-sandbox
- **Base:** evidência: teste no scratchpad em 28/10/2026, um link para um arquivo, Write e Edit
  chamados no caminho do link

## Sintoma
Ao planejar memórias compartilhadas por link simbólico, o medo era o de sempre: um editor que
salva "atômico" (escreve um arquivo novo e renomeia) troca o link por um arquivo comum, e a
sincronização quebra sem aviso. O teste mostrou outra coisa. As duas ferramentas recusam:

```text
Refusing to write .../proj/a.md: it is a symbolic link. Write to the link's target path
instead: .../loja/a.md.
```

O Read segue o link normalmente.

## Causa
É uma proteção do próprio Claude Code: ele não escreve através de links e diz qual é o destino.
O modelo então escreve no destino. Não achamos isso descrito na documentação de ferramentas
(análise: pode mudar sem aviso numa versão nova).

## Solução
Aproveitar: uma cópia única e um link em cada lugar que precisa dela fica sincronizada por
construção, porque toda edição feita pelo Claude cai na cópia. Comandos de shell (`sed -i`)
continuam trocando o link por arquivo; isso precisa de conserto à parte.

## O que mudou no dev-sandbox
A skill [`compartilhar-memorias`](../../utils/skills/compartilhar-memorias/SKILL.md) foi
desenhada sobre isso ([guia](../claude-code/compartilhar-memorias.md)); a rule dela manda
reconferir o comportamento.
