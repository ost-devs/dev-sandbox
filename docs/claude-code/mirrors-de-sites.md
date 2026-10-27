# Espelhar sites de documentação

Este guia mostra **quando e como** copiar para o seu projeto a documentação
de um site que não está num repositório git. O exemplo é a documentação
oficial do Claude Code, que o dev-sandbox já usa. O mesmo vale para outras.
O uso geral da skill está em [Espelhar repositórios de fora](./mirrors.md);
o que fazer com a cópia está em
[Base de conhecimento sob demanda](./base-de-conhecimento.md).

## Quando serve

Muitos sites de documentação publicam um índice para IAs, o `llms.txt`, com
um link por página. Quando cada link aponta para uma página em Markdown
(`.md`) do mesmo site, a skill `/mirrors` copia todas as páginas para
`mirrors/<nome>/`.

Escolha o caminho nesta ordem:

| A documentação... | Use | Por quê |
|---|---|---|
| Está num repositório git (a pasta `docs/` de um projeto, por exemplo) | Espelho git, do [guia geral](./mirrors.md), com `--include` na pasta | Tem commit: dá para fixar uma versão, e o download é só do que mudou |
| Não está, mas o site tem `llms.txt` com páginas `.md` | Espelho de site (este guia) | É a única forma de ter a documentação inteira e local |
| Tem só um arquivo único (`llms-full.txt`) ou links para páginas HTML | Ainda não é suportado. Procure o repositório git da documentação | |
| Não tem `llms.txt` | Ainda não é suportado. Peça ao Claude para ler as páginas que você precisa | |

Na prática, o espelho de site é para documentação **fechada**: a de
produtos cujo código não é aberto. Projetos de código aberto quase sempre
guardam a documentação no próprio repositório, e aí o espelho git é melhor.

Uma diferença a favor do site, deduzida e não testada: a página `.md` do
site já vem pronta para ler, enquanto o repositório pode ter componentes
(MDX) e trechos que vêm de outros arquivos.

## Sites testados

Testado em outubro/2026. Os sites mudam: confira antes (veja abaixo como).

| Site | Índice (`llms.txt`) | Páginas `.md` | Documentação no git? | Use |
|---|---|---|---|---|
| Claude Code | `https://code.claude.com/docs/llms.txt` | 227 (em inglês: `--include en`) | Não | **Site**. Uma página redireciona para outro site e é pulada |
| API do Claude | `https://platform.claude.com/llms.txt` | 821 | Não | **Site** |
| Stripe | `https://docs.stripe.com/llms.txt` | 472 | Não | **Site**, com uma parte: `--include payments api` |
| MCP | `https://modelcontextprotocol.io/llms.txt` | 358 | `modelcontextprotocol/modelcontextprotocol`, pasta `docs` | Git |
| uv (Python) | `https://docs.astral.sh/uv/llms.txt` | 55 | `astral-sh/uv`, pasta `docs` | Git |
| React | `https://react.dev/llms.txt` | 180 | `reactjs/react.dev`, pasta `src/content` | Git |
| Expo | `https://docs.expo.dev/llms.txt` | 568 | `expo/expo`, pasta `docs` | Git |
| Supabase | `https://supabase.com/llms.txt` | 31 | `supabase/supabase`, pasta `apps/docs` | Git |
| Bun | `https://bun.com/docs/llms.txt` (o `bun.sh` antigo não serve) | 319 | `oven-sh/bun`, pasta `docs` | Git |
| Cloudflare | `https://developers.cloudflare.com/workers/llms.txt` (um por produto) | 422 | `cloudflare/cloudflare-docs` | Git |
| Next.js | `https://nextjs.org/docs/llms.txt` | 0 (links HTML) | `vercel/next.js`, pasta `docs` | Git |
| Svelte, Hono, Tauri | `.../llms.txt` | 0 (só arquivos únicos) | Sim | Git |
| Rust | Não tem | | `rust-lang/book`, `rust-lang/reference` | Git |

## 1. Conferir se um site serve

Peça ao Claude: "o site X tem llms.txt com páginas .md?". Ou confira no
terminal (host ou container):

```bash
curl -s https://docs.stripe.com/llms.txt | grep -c '\.md)'
```

Um número alto quer dizer que serve. Zero quer dizer que não serve.

## 2. Adicionar

Fale normalmente ("espelhe a documentação da API do Claude"), ou rode no
projeto:

```bash
python3 ~/.claude/skills/mirrors/fetch_mirrors.py --add claude-api-docs https://platform.claude.com/llms.txt --license LicenseRef-Anthropic-docs
```

| Opção | Para quê |
|---|---|
| `--include en` | Só as páginas cujo caminho começa com `en/` (um idioma, um produto, uma seção) |
| `--license` | A licença da documentação. Muitas não são abertas: aí escreva, por exemplo, `LicenseRef-Anthropic-docs`, e não ponha a cópia no git (a skill já a deixa fora) |

A cópia fica em `mirrors/<nome>/`. Dentro dela:

| Arquivo | O que é |
|---|---|
| `llms.txt` | O índice: cada página com uma linha dizendo o que cobre. O Claude escolhe a página por aqui |
| `<caminho>.md` | Uma página, com o mesmo caminho que tem no site |
| `.mirror-pages.json` | O hash de cada página e quando ela mudou |

## 3. Atualizar

Um espelho de site é sempre "atualizado": não dá para fixar uma versão,
porque o site não tem commits. Cada atualização baixa **todas** as páginas,
porque o site não diz quais mudaram, e compara cada uma com a anterior.

| Você quer | Peça ou rode |
|---|---|
| Atualizar e ver o que mudou | `/mirrors`, ou o script sem argumentos |
| Só saber se mudou, sem gravar | `/mirrors check` |
| Saber quais artigos seus citam páginas que mudaram | `--stale <nome> docs/` ([como funciona](./base-de-conhecimento.md#como-funciona)) |

A data de mudança é a da atualização que viu a mudança, não a da edição no
site. Quem atualiza toda semana sabe a data com folga de uma semana.

## No dev-sandbox

A documentação do Claude Code fica em `mirrors/claude-code-docs/`, fora do
git, porque a licença não é aberta. O agente `claude-code-pesquisador`
atualiza a cópia uma vez por tarefa, procura nela com `grep` e só vai à web
se a página não existir. Quando há mudança, ele roda o `--stale` e diz quais
guias de `docs/claude-code/` conferir.

Depois de clonar o dev-sandbox, baixe a cópia uma vez (no container ou no
host):

```bash
python3 utils/skills/mirrors/fetch_mirrors.py
```

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `no .md pages under ... in the index` | O site lista páginas HTML ou outros índices | Veja [quando serve](#quando-serve). No Cloudflare, use o índice de cada produto |
| `skipped ...: redirects off the site` | A página foi movida para outro site | Normal: ela fica de fora. Se precisar dela, espelhe o outro site |
| Toda atualização mostra a mesma página como mudada | A página tem conteúdo que muda a cada pedido (data, contador) | Avise: o script precisa ignorá-la |
| A atualização demora | Ela baixa tudo: cerca de 15 páginas por segundo | Use `--include` para ficar só com o que usa |
| `--pin` recusa | Site não tem commit | Normal. Para fixar versão, use o repositório git da documentação, se houver |

## Base

Testado num projeto descartável e no dev-sandbox, em outubro/2026: a
documentação do Claude Code tem 227 páginas e 11 MB, e baixa em 13 segundos.
O site não manda ETag, e o `Last-Modified` é a hora do pedido, por isso não
dá para baixar só o que mudou. Os outros índices foram verificados contando
os links `.md` sob o endereço de cada site, e as pastas de documentação pela
API do GitHub.
