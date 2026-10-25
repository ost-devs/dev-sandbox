# A janela de contexto: tudo o que o Claude "sabe" agora

A **janela de contexto** é o espaço onde fica tudo o que o Claude enxerga
numa sessão. Se uma informação não está lá, para ele ela não existe.

## O que fica dentro

Segundo a documentação oficial, a janela guarda:

- o histórico da conversa;
- o conteúdo dos arquivos que ele leu;
- a saída dos comandos que ele rodou;
- os seus `CLAUDE.md`;
- a memória automática;
- as skills carregadas;
- as instruções do sistema.

Há também conteúdo que **nunca aparece no seu terminal**, como o texto que
o próprio Claude Code acrescenta por conta própria (por exemplo, um aviso de
que um arquivo mudou no disco).

## Ela começa vazia a cada sessão

> "Each Claude Code session begins with a fresh context window."

Uma sessão nova **não** traz a conversa da anterior. O que atravessa de uma
sessão para outra são só os arquivos de instruções (`CLAUDE.md`) e a memória
automática (veja [quando cada coisa carrega](./quando-cada-coisa-carrega.md)).

Retomar uma sessão (`claude --continue` ou `--resume`) é outra coisa: ela
reabre a **mesma** conversa e acrescenta mensagens ao final.

## Ela enche, e tem um limite

Cada arquivo lido, cada resposta e cada saída de comando ocupa espaço. O
tamanho do limite depende do modelo: alguns têm janela de 1 milhão de tokens;
outros, 200 mil (**token** é o pedaço de texto que o modelo conta; uma palavra
em português costuma ser 1 a 3 tokens). Quando chega perto do limite, o Claude
Code resume a conversa sozinho: é a [compactação](./compactacao.md).

## Como ver o que está lá dentro

| Comando | Mostra |
|---|---|
| `/context` | Quanto espaço cada categoria ocupa, e quais `CLAUDE.md` e arquivos de memória carregaram (lista "Memory files") |
| `/memory` | Os arquivos de instruções e de memória, para abrir e editar |
| `/usage` | Os tokens e o custo da sessão |

## Por que isso importa

- O que você quer que o Claude respeite sempre deve estar num arquivo de
  instruções, e não só dito na conversa: a conversa pode ser resumida e perder
  detalhes ([compactação](./compactacao.md)).
- Contexto cheio custa: o conteúdo inteiro vai junto a cada pedido
  ([a cada mensagem](./a-cada-mensagem-o-contexto-vai-junto.md)).

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[como o Claude Code funciona](https://code.claude.com/docs/en/how-claude-code-works),
[explore a janela de contexto](https://code.claude.com/docs/en/context-window),
[memória](https://code.claude.com/docs/en/memory),
[configuração de modelo](https://code.claude.com/docs/en/model-config).
