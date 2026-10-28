# Capturar artigos da web

Este guia mostra como guardar no projeto artigos da web (posts de blog,
tutoriais), um só, uma lista ou uma cadeia de artigos que citam uns aos
outros, para o Claude ler localmente e escrever a partir deles. O que fazer
com eles depois está em [Base de conhecimento sob demanda](./base-de-conhecimento.md).
Documentação de projetos é outro caso: veja [Espelhar repositórios de
fora](./mirrors.md) e [Espelhar sites de documentação](./mirrors-de-sites.md).

Quem converte cada página é o **Defuddle**, o mesmo motor do [Obsidian Web
Clipper](https://github.com/obsidianmd/obsidian-clipper). Ele guarda só o
artigo, sem menu, propaganda, rodapé ou lista de "relacionados", e o
transforma em Markdown com título, autor e datas no topo.

## O que você terá no fim

| Arquivo | O que é | Vai pro git? |
|---|---|---|
| `mirrors/mirrors.json` | A lista dos endereços capturados | Sim |
| `mirrors/<nome>/<site>/<caminho>.md` | Cada artigo em Markdown, somente leitura | Não |
| `mirrors/<nome>/.mirror-pages.json` | Hash, título, datas e os links do texto de cada artigo | Não |

Artigos quase sempre têm todos os direitos reservados. A cópia fica só na sua
máquina; os seus textos citam a fonte e dizem com as suas palavras.

## 1. Instalar o Defuddle (uma vez só)

Precisa de Node.js: a imagem do dev-sandbox já tem. Rode no lugar onde a
skill está instalada (host ou container):

```bash
npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts
```

O `npm ci` instala as versões exatas do `package-lock.json` que vem com a
skill (Defuddle 0.19.5 e 26 dependências), e o `--ignore-scripts` impede que
qualquer pacote rode código na instalação. Sem o Defuddle, só a captura de
artigos fica fora; o resto da skill funciona.

## 2. Capturar

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Um artigo | "capture este artigo como tokens: <url>" | `--add tokens <url> --web` |
| Mais um no mesmo grupo | "acrescente <url> em tokens" | o mesmo comando com outra URL |
| Ver o que os artigos citam e ainda não foi capturado | "o que os artigos de tokens citam?" | `--links tokens` |
| Seguir a cadeia | "capture os artigos que ele cita, até 10" | `--add tokens <url> --web --depth 1 --max-pages 10` |

"Rode" é `python3 ~/.claude/skills/mirrors/fetch_mirrors.py`, de qualquer
pasta do projeto.

**Comece sem profundidade.** Capture o artigo, veja a lista do `--links` e
escolha, como você faria abrindo abas. Os sites se citam muito: no teste, um
blog deixou 67 links pendentes depois de dois níveis. A profundidade só segue
links do **mesmo site** e para no `--max-pages` (20, se você não disser).

O que a captura faz sozinha:

| Situação | O que acontece |
|---|---|
| A mesma página com outra grafia (`/` no fim, `?utm_...`, `#seção`) ou que redireciona para uma já capturada | Reconhecida como a mesma; não baixa de novo |
| Dois artigos que se citam (laço) | Cada página entra uma vez |
| Imagem, PDF, página inexistente, laço de redirecionamento, página acima de 5 MB | Pulada, com o motivo |
| `robots.txt` do site proíbe | Pulada. O script respeita o que o site pede |
| O site diz que a página é editada num repositório do GitHub | Aparece uma dica: talvez um espelho git sirva melhor |

## 3. Atualizar

Um artigo capturado é uma **foto**: rodar a skill de novo não baixa o que já
está lá, só o que falta (por exemplo, depois de clonar o projeto). Assim a
busca local continua local.

| Você quer | Rode |
|---|---|
| Baixar o que falta | `/mirrors`, ou o script sem argumentos |
| Saber se falta algo (sem rede) | `--check` |
| Baixar tudo de novo e ver o que mudou | `--refresh tokens` |
| Saber quais textos seus citam artigos que mudaram | `--stale tokens docs/` |

A data de modificação que o site informa fica no topo de cada arquivo
(`modified`), mas só se sabe dela baixando a página. Por isso o `--refresh`
compara o **conteúdo** (o hash do Markdown). O HTML não serve para comparar,
porque propaganda e contadores mudam a cada pedido.

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `web mirrors need Defuddle` | Defuddle não instalado | Passo 1 |
| `robots.txt disallows it` | O site pede para robôs não lerem aquela página | Respeite. Leia no navegador |
| `no article content found` | Página sem texto de artigo (índice, login, aplicação) | Capture o artigo, não a página de lista |
| `not HTML (...)` | Link para imagem, PDF ou dados | Normal |
| Muitos artigos pouco úteis | Profundidade alta | Remova com `--remove <nome>` e recomece com `--depth 0` |

## Base

Testado em outubro/2026 com o artigo
[O que são tokens no Claude Code?](https://www.ssdnodes.com/learn/lang/pt/claude-code-token-usage-explained),
da SSD Nodes:

- o HTML tinha 113 mil caracteres e 63 links; o Markdown ficou com 26 mil e
  só as 12 menções do texto (os 4 "relacionados" ficaram de fora);
- dois níveis da cadeia, limitados a 15 páginas novas, levaram 15 segundos,
  sem página repetida;
- um `--refresh` das 16 páginas não mostrou nenhuma mudança falsa.

O leitor de `robots.txt` do Python recebia 403 do servidor e tratava como
"tudo proibido". O script baixa o arquivo com a mesma identificação das
páginas e segue a norma (RFC 9309): erro 4xx quer dizer "sem regras".
