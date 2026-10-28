# Cache de prompt: por que reler é mais barato

Como o contexto inteiro vai junto a cada pedido
([entenda](./a-cada-mensagem-o-contexto-vai-junto.md)), o Claude Code usa o
**cache de prompt** da API: o que já foi processado é reaproveitado e cobrado
a um preço menor, e só o que mudou é processado por inteiro. Ele é automático.

## Como funciona: o início tem que ser idêntico

O cache compara o **começo** de cada pedido (o *prefixo*) com o que foi
processado há pouco. A comparação é exata: mudou algo no meio, tudo o que vem
depois é recalculado. Por isso o Claude Code monta o pedido em camadas, da que
menos muda para a que mais muda:

| Camada | Conteúdo | Muda quando |
|---|---|---|
| Instruções do sistema | Instruções básicas e ferramentas | O conjunto de ferramentas muda |
| Contexto do projeto | `CLAUDE.md`, memória, rules sem `paths:` | A sessão começa, ou depois de `/clear` ou `/compact` |
| Conversa | Suas mensagens, respostas, resultados de ferramentas | A cada turno |

Numa conversa normal só o final é novo, então quase tudo vem do cache.

## Por quanto tempo o cache vale

Ele expira depois de um tempo sem uso (o *TTL*), e cada uso renova o relógio.
Existem dois tempos: **5 minutos** e **1 hora** (a hora cobra mais para gravar
o cache). Por padrão, o Claude Code pede 1 hora para a conversa principal
**só numa assinatura Claude, dentro do uso incluído no plano**; com chave de
API, provedor de nuvem ou créditos de uso, são 5 minutos. Subagentes, compactação
e similares ficam com 5 minutos por padrão. Dá para escolher (`promptCacheTtl`,
`CLAUDE_CODE_PROMPT_CACHE_TTL`).

Na prática: a **primeira mensagem depois de uma pausa longa** é mais lenta e
mais cara, porque o cache já expirou.

## Quanto ele economiza

Em relação ao preço normal de entrada do modelo:

| Operação | Custa |
|---|---|
| Gravar no cache de 5 minutos | 1,25× |
| Gravar no cache de 1 hora | 2× |
| Ler do cache | 0,1× na maioria dos modelos; 0,05× no Opus 5.5 e no Sonnet 5.5; 0,025× no Fable 5.1 |

No cache de 5 minutos, uma leitura já paga o custo extra da gravação; no de
1 hora, são precisas duas (conta minha). Os preços de cada modelo e a
conta de um turno com e sem cache estão em [quanto custa](./quanto-custa.md).

## O que invalida o cache (próximo pedido sai caro)

- trocar de modelo com `/model` (cada modelo tem o seu cache);
- mudar o nível de esforço (em alguns modelos);
- ligar o modo rápido;
- conectar ou remover um servidor MCP, ou negar uma ferramenta inteira
  (quando as ferramentas não são carregadas sob demanda);
- compactar a conversa;
- acumular muitas imagens;
- atualizar o Claude Code.

## O que **não** invalida

Editar arquivos do repositório, trocar o modo de permissão, usar skills e
comandos, `/recap`, `/rewind`, chamar um subagente, e editar o `CLAUDE.md`
(a edição simplesmente não vale até o próximo `/clear`, `/compact` ou reinício).

## Como ver se está funcionando

`/usage` mostra uma linha `Prompt cache (main)` com a parcela de tokens vinda
do cache, quantas falhas houve e se o cache está "quente" agora (Claude Code
2.1.251 ou mais novo).

## Escopo do cache

O cache vale para uma máquina e uma pasta. O pedido embute o caminho da
memória e a pasta de trabalho, então sessões em **pastas diferentes** não
aproveitam o cache uma da outra. Sessões paralelas **na mesma pasta** podem.

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[custos](https://code.claude.com/docs/en/costs),
[preços da API](https://platform.claude.com/docs/en/about-claude/pricing).
