# Mirrors: cópias de fontes de fora

Copia repositórios git, sites de documentação e artigos da web para
`mirrors/<nome>/` no seu projeto, somente leitura e fora do git, para o
Claude ler dali em vez de buscar na web. O `mirrors/mirrors.json` (vai pro
git) guarda de onde vem cada cópia.

Guias completos: [repositórios](../../../docs/claude-code/mirrors.md),
[sites de documentação](../../../docs/claude-code/mirrors-de-sites.md) e
[artigos da web](../../../docs/claude-code/mirrors-de-artigos.md) (este
precisa de `npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts`).

### Repositórios git

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Copiar um repositório | "espelhe https://github.com/rust-lang/book como rust-book" | `--add rust-book https://github.com/rust-lang/book` |
| Sempre na versão mais nova | "... sempre atualizado" | o mesmo com `--follow` |
| Só uma pasta | "espelhe só a pasta `src` de ..." | `--include src` |
| Fixar na versão mais nova | `/mirrors pin rust-book` | `--pin rust-book` |
| Fixar numa versão publicada | "fixe lezer/common na versão 1.5.2" | `--pin lezer/common @1.5.2` |

### Sites de documentação (`llms.txt`)

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Copiar a documentação de um site | "espelhe a documentação da Stripe, só pagamentos e API" | `--add stripe-docs https://docs.stripe.com/llms.txt --include payments api` |
| Atualizar no máximo uma vez por dia | "atualize a stripe-docs se tiver mais de um dia" | `--max-age 24 stripe-docs` |
| Saber quais textos seus citam páginas que mudaram | "quais docs citam páginas que mudaram na stripe-docs?" | `--stale stripe-docs docs/` |

### Artigos da web

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Guardar um artigo em Markdown | "capture este artigo como testes: <url>" | `--add testes <url> --web` |
| Ver o que os artigos citam | "o que os artigos de testes citam?" | `--links testes` |
| Seguir a cadeia (mesmo site) | "capture os artigos que ele cita, até 10" | `--add testes <url> --web --depth 1 --max-pages 10` |
| Baixar de novo e ver o que mudou | "atualize os artigos de testes" | `--refresh testes` |

### Para todos

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Baixar tudo (depois de clonar o projeto) | `/mirrors` | *(sem argumentos)* |
| Ver o que falta ou está velho | `/mirrors check` | `--check` |
| Tirar um espelho | `/mirrors remove rust-book` | `--remove rust-book` |

"Rode" é `python3 ~/.claude/skills/mirrors/fetch_mirrors.py`, de qualquer
pasta do projeto. Depois de adicionar, fixar ou remover, faça commit do
`mirrors/mirrors.json`.
