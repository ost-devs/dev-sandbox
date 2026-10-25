# Compactação: quando a conversa vira um resumo

Quando a [janela de contexto](./janela-de-contexto.md) está quase cheia, o
Claude Code **resume a conversa** e continua a partir do resumo. Isso se chama
compactação. Uma sessão com a janela cheia não termina por causa disso.

## Quando acontece

| Jeito | Como |
|---|---|
| Automática | Ao chegar perto do limite do modelo |
| Manual | `/compact` (aceita um foco: `/compact foque na correção do login`) |
| Parcial | `/rewind`, escolher uma mensagem e **Summarize from here** ou **Summarize up to here** |
| Antecipada | `/autocompact 500k` define quanto a janela pode encher antes da automática |
| Por ociosidade | Uma conversa deixada parada pode ser compactada (configuração `idleCompaction`, 2.1.290 ou mais novo) |

O ponto da compactação automática depende do modelo: por padrão, modelos com
janela de 1 milhão compactam em torno de 967 mil tokens; modelos de 200 mil
(ou 1 milhão desligado) compactam na marca de 200 mil.

## O que sobrevive

| O quê | Depois da compactação |
|---|---|
| Instruções do sistema e estilo de saída | Continuam valendo |
| `CLAUDE.md` da raiz do projeto e rules sem `paths:` | **Relidos do disco** |
| Memória automática | Relida do disco |
| Descrições das skills | Reconstruídas e reinseridas |
| Plano feito no modo plano | Relido do disco |
| `CLAUDE.md` de subpastas e rules com `paths:` | Recarregados sob demanda, quando o Claude mexer nos arquivos correspondentes |
| Arquivos que o Claude leu ou editou | Até 5 são relidos, os mais recentes primeiro (arquivo com mais de 5 mil tokens volta só como referência) |
| Texto das skills usadas | Reinserido, com teto de 5 mil tokens por skill e 25 mil no total |
| Comandos e subagentes em segundo plano | Continuam rodando |
| **O restante da conversa** | **Vira resumo** |

## O que se perde

O resumo guarda seus pedidos e trechos de código importantes, mas
"detailed instructions from early in the conversation may be lost" (instruções
detalhadas do começo da conversa podem se perder).

Se uma instrução sumiu depois da compactação, a causa é uma destas: ela foi
dada **só na conversa**; está num `CLAUDE.md` de subpasta que ainda não
recarregou; ou é uma rule com `paths:` que ainda não casou com nenhum arquivo.
A solução: coloque no `CLAUDE.md` da raiz do projeto o que precisa ficar.

## Guiar o que o resumo guarda

No `CLAUDE.md`:

```markdown
# Compact instructions

When you are using compact, please focus on test output and code changes
```

## Quanto custa compactar

O resumo é produzido por um pedido à parte, que lê a conversa inteira.
Com o cache quente, custa uma fração do que o tamanho sugere. Depois de uma
pausa maior que a vida do cache, o histórico é reprocessado do zero, e é aí
que a compactação mais custa (por exemplo, ao retomar uma sessão antiga).
O pedido seguinte à compactação é barato, porque o resumo é curto.

Dica da documentação: compacte em **pausas naturais** entre tarefas, em vez de
esperar a automática disparar no meio de uma tarefa.

## Compactar ou limpar?

| | `/compact` | `/clear` |
|---|---|---|
| Continuidade | Mantém um resumo | Começa do zero |
| Custo | Um pedido grande | Nada |
| Use quando | Vai seguir no mesmo assunto | Vai mudar de assunto |

## Se o contexto reencher logo depois

Se um único arquivo ou saída é tão grande que o contexto reenche após cada
resumo, o Claude Code para de compactar sozinho depois de algumas tentativas e
mostra um erro, em vez de ficar em laço. Delegar a leitura grande a um
[subagente](./subagentes-o-que-herdam.md) evita isso.

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[janela de contexto](https://code.claude.com/docs/en/context-window),
[como o Claude Code funciona](https://code.claude.com/docs/en/how-claude-code-works),
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[configuração de modelo](https://code.claude.com/docs/en/model-config),
[memória](https://code.claude.com/docs/en/memory).
