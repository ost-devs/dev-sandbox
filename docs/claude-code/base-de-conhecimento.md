# Base de conhecimento sob demanda (esboço)

> Esboço na branch `experimento/mirrors-paginas`. O código funciona e foi
> testado; o fluxo dos artigos ainda não foi usado de verdade.

A ideia: a fonte oficial fica **inteira e local**, em inglês, só para leitura.
Os artigos em português (como os de [`docs/claude-code/`](./README.md))
resumem e adaptam essa fonte. Quando a fonte muda, um comando diz **quais
artigos** precisam ser conferidos de novo.

| Camada | O que é | Onde fica | Vai pro git? |
|---|---|---|---|
| Fonte | Cópia das páginas oficiais, intacta | `mirrors/<nome>/` | Não (só o `mirrors.json`) |
| Artigos | Resumo e adaptação, em português, citando a fonte | `docs/...` | Sim |
| Ligação | O link de cada página usada, no artigo | Seção **Base** de cada artigo | Sim |

## Por que local é melhor que buscar na web

Medido nesta sessão com a documentação do Claude Code (227 páginas, 11 MB,
13 segundos para baixar tudo):

| | Buscar na web (`WebFetch`) | Espelho local (`grep` + leitura) |
|---|---|---|
| Página grande | `en/skills.md` tem 118 mil caracteres. O pesquisador leu só os primeiros ~100 mil | Lê qualquer parte, com número de linha |
| Citação | A ferramenta **resumiu** a página do skill-creator em vez de citá-la; o pesquisador não pôde confirmar uma frase | Texto exato, citável |
| Custo de uma pergunta | Uma página inteira (~30 mil tokens para `skills.md`) passa por um modelo de resumo, mais o agente | Um `grep` por "supporting files" devolveu 2,5 mil caracteres (~700 tokens) |
| Atualização | Sempre a versão do momento | A da última busca; `--check` diz se mudou |

Os tokens são estimativa (cerca de 4 caracteres por token em inglês), não
medição.

## Como funciona

A skill [`mirrors`](./mirrors.md) ganha um tipo novo, **pages**, num script
próprio (`utils/skills/mirrors/fetch_pages.py`). Ele serve para sites de
documentação que não têm repositório git, mas publicam um índice `llms.txt`
com uma página `.md` por assunto.

```bash
# no projeto (host ou container)
python3 ~/.claude/skills/mirrors/fetch_mirrors.py --add claude-code-docs https://code.claude.com/docs/llms.txt --include en --license proprietary
```

| Passo | O que acontece |
|---|---|
| Buscar | Baixa o índice e todas as páginas. O site não informa data de mudança (o `Last-Modified` é a hora do pedido, e não há ETag), então não dá para baixar só o que mudou |
| Comparar | Calcula um hash de cada página e compara com o da busca anterior. Mostra o que é novo, o que mudou e o que saiu |
| Guardar | Grava a cópia somente leitura e um `.mirror-pages.json` com o hash e a data em que cada página mudou (a data da busca que viu a mudança, não a da edição) |
| Conferir artigos | `--stale claude-code-docs docs/` lista os artigos que citam uma página que mudou **depois do último commit do artigo** |

Teste: simulei uma mudança em `en/skills.md`. O `--stale` apontou os três
guias que a citam (`consultor-do-projeto.md`, `montar-consultor.md`,
`mirrors.md`) e nenhum outro.

Descoberta no teste: `en/claude-tag.md` redireciona para uma página HTML em
`claude.com`, que muda a cada pedido. Sem tratamento, ela apareceria como
"mudou" em toda busca. O script pula páginas que saem do site e avisa.

## No dev-sandbox

| Pergunta | Resposta |
|---|---|
| Onde guardar a documentação oficial? | Em `mirrors/claude-code-docs/`, **não** em `docs/claude-code/official/`. O dev-sandbox é público: pôr a documentação da Anthropic no git é redistribuí-la, e a licença não é aberta. E cada atualização somaria até 11 MB ao histórico |
| O pesquisador muda? | Passa a procurar primeiro no espelho (`grep`) e só vai à web se a página não existir ou se o `--check` disser que está velha |
| E o "Conferido em outubro/2026"? | Continua, porque diz a versão do Claude Code. O `--stale` passa a dizer **quando** conferir de novo, em vez de depender de lembrar |
| Quem roda a atualização? | O agente, no começo de uma pesquisa (13 s), ou você, com `/mirrors` |

## Em outros contextos

O mesmo fluxo serve para qualquer série de artigos sobre uma fonte que muda:

1. Espelhe a fonte: repositório git (fixo ou sempre atualizado) ou site com
   `llms.txt` (sempre atualizado).
2. Escreva cada artigo a partir da cópia local, citando as páginas usadas.
3. A cada atualização da fonte, rode `--stale` e revise só os artigos
   apontados.

Muitos sites de documentação já publicam `llms.txt` (há um diretório em
[llmstxt.org](https://llmstxt.org/)). O da Anthropic tem também versões
traduzidas, inclusive `pt-br`, em `https://code.claude.com/docs/_llms/pt-br.txt`;
o esboço ainda não as trata.

## Em aberto

- O `.mirror-pages.json` fica na cópia, fora do git. Num clone novo, as datas
  recomeçam, e o `--stale` só funciona depois da segunda busca. Versionar os
  hashes resolveria, ao custo de 227 linhas no `mirrors.json`.
- Para espelhos git, o `--stale` ainda não existe. Seria o mesmo princípio,
  usando o `git diff` entre dois commits.
- O pesquisador e as rules ainda não foram alterados para usar o espelho.
