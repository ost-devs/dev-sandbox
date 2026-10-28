# Mirrors: cópias de repositórios de fora

Copia outros repositórios para `mirrors/<nome>/` no seu projeto, somente
leitura e fora do git, para o Claude ler dali em vez de buscar na web. O
`mirrors/mirrors.json` (vai pro git) guarda de onde vem cada cópia e em qual
commit.

Guias completos: [repositórios](../../../docs/claude-code/mirrors.md),
[sites de documentação](../../../docs/claude-code/mirrors-de-sites.md) e
[artigos da web](../../../docs/claude-code/mirrors-de-artigos.md) (este
precisa de `npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts`).

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Copiar um repositório | "espelhe https://github.com/rust-lang/book como rust-book" | `--add rust-book https://github.com/rust-lang/book` |
| Sempre na versão mais nova | "... sempre atualizado" | o mesmo com `--follow` |
| Só uma pasta | "espelhe só a pasta `src` de ..." | `--include src` |
| Baixar tudo (depois de clonar o projeto) | `/mirrors` | *(sem argumentos)* |
| Ver o que falta ou está velho | `/mirrors check` | `--check` |
| Fixar na versão mais nova | `/mirrors pin rust-book` | `--pin rust-book` |
| Fixar numa versão publicada | "fixe lezer/common na versão 1.5.2" | `--pin lezer/common @1.5.2` |
| Guardar um artigo da web em Markdown | "capture este artigo: <url>" | `--add <nome> <url> --web` |
| Ver o que os artigos citam | "o que esses artigos citam?" | `--links <nome>` |
| Tirar um espelho | `/mirrors remove rust-book` | `--remove rust-book` |

"Rode" é `python3 ~/.claude/skills/mirrors/fetch_mirrors.py`, de qualquer
pasta do projeto. Depois de adicionar, fixar ou remover, faça commit do
`mirrors/mirrors.json`.
