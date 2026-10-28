# O leitor de `robots.txt` do Python proibia um site que libera tudo

- **Data:** 2026-10
- **Ambiente:** container do dev-sandbox, Python 3.11, skill `mirrors` (captura de artigos)
- **Base:** evidência: captura de `https://www.ssdnodes.com/learn/...`, cujo
  `robots.txt` tem `Allow: /` e só bloqueia áreas administrativas

## Sintoma
A captura de um artigo era pulada com `robots.txt disallows it`, mas o
`robots.txt` do site liberava a página.

## Causa
`urllib.robotparser.RobotFileParser.read()` baixa o `robots.txt` com a
identificação padrão do Python (`Python-urllib`). O servidor (atrás do
Cloudflare) responde 403 para ela, e o `RobotFileParser` trata 401 e 403
como "tudo proibido". A norma atual ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309))
diz o contrário: um erro 4xx no `robots.txt` quer dizer "sem regras".

## Solução
Baixar o `robots.txt` com a mesma identificação usada nas páginas e passar o
texto para `RobotFileParser.parse()`. Erro 4xx: tudo liberado. Erro 5xx ou
falta de rede: não buscar.

## O que mudou no dev-sandbox
`Fetcher.allowed()` em
[`utils/skills/mirrors/fetch_web.py`](../../utils/skills/mirrors/fetch_web.py).
