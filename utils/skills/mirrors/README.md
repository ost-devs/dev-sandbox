# Mirrors: cópias de fontes de fora

Copia repositórios git, sites de documentação e artigos da web para
`mirrors/<nome>/` no seu projeto, somente leitura e fora do git, para o
Claude ler dali em vez de buscar na web. O `mirrors/mirrors.json` (vai pro
git) guarda de onde vem cada cópia.

Guias completos: [repositórios](../../../docs/claude-code/mirrors.md),
[sites de documentação](../../../docs/claude-code/mirrors-de-sites.md) e
[artigos da web](../../../docs/claude-code/mirrors-de-artigos.md) (este
precisa de `npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts`).

## Como ler as tabelas

Cada linha mostra o mesmo pedido de dois jeitos: em palavras, numa sessão
do Claude, ou como comando. No comando, `...` é o começo:

| Onde | Troque `...` por |
|---|---|
| Numa sessão do Claude | `/mirrors` |
| No terminal, sem o Claude (host ou container, de qualquer pasta do projeto) | `python3 ~/.claude/skills/mirrors/fetch_mirrors.py` |

O que está entre `< >` é seu: `<rust-book>` é um exemplo de nome, `<url>`
e `<site>` são endereços.

## Repositórios git

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Copiar, sempre atualizado | "espelhe o <livro do Rust> e deixe sempre atualizado" | `... --add <rust-book> <url> --follow` |
| Copiar fixo na versão de hoje | "espelhe o <livro do Rust>" | `... --add <rust-book> <url>` |
| Só uma pasta | "espelhe só a pasta <do editor> do <Zed>" | `... --add <zed> <url> --include <crates/editor>` |
| Fixar numa versão publicada | "fixe o <lezer/common> na versão <1.5.2>" | `... --pin <lezer/common> @<1.5.2>` |

## Sites de documentação (`llms.txt`)

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Copiar a documentação | "espelhe a documentação do <Claude Code>" | `... --add <claude-code-docs> <site>/llms.txt` |
| Só uma parte | "... só em <inglês>" | o mesmo com `--include <en>` |
| Atualizar no máximo uma vez por dia | "atualize a <claude-code-docs> se tiver mais de um dia" | `... --max-age 24 <claude-code-docs>` |

## Artigos da web

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Guardar um artigo | "guarde este artigo sobre <testes>: <url>" | `... --add <testes> <url> --web` |
| Ver o que os artigos citam | "o que os artigos de <testes> citam?" | `... --links <testes>` |
| Guardar também os citados | "guarde também os artigos que ele cita, até <10>" | `... --add <testes> <url> --web --depth 1 --max-pages <10>` |
| Ver se mudaram | "veja se os artigos de <testes> mudaram" | `... --refresh <testes>` |

## Para todos

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Baixar tudo (depois de clonar o projeto) | "baixe os mirrors" | `...` |
| Ver o que falta ou está velho | "algum mirror está velho?" | `... --check` |
| Saber quais textos seus citam fontes que mudaram | "quais textos citam páginas que mudaram na <claude-code-docs>?" | `... --stale <claude-code-docs> <docs/>` |
| Tirar uma cópia | "tire o mirror <rust-book>" | `... --remove <rust-book>` |

Depois de adicionar, fixar ou remover, faça commit do `mirrors/mirrors.json`.
