# O Puppeteer não abre o Chromium da imagem: "No usable sandbox"

- **Data:** 2026-11
- **Ambiente:** imagem do dev-sandbox em Debian 13 (trixie), Chromium 156,
  `puppeteer-core` 25.18, `playwright-core` 1.65
- **Base:** evidência (testado dentro do container, 23/11/2026) e
  documentação (lista de arquivos do pacote `chromium-sandbox` no
  [packages.debian.org](https://packages.debian.org/trixie/amd64/chromium-sandbox/filelist),
  lida em 23/11/2026)

## Sintoma

O Playwright abria o navegador; o Puppeteer, com a mesma imagem, falhava:

```text
No usable sandbox! If this is a Debian system, please install the chromium-sandbox package to solve this problem.
```

## Causa

O Chromium isola cada aba numa sandbox própria. Para montá-la ele precisa de
uma de duas coisas, e o container não dá nenhuma:

- **user namespace:** o Docker bloqueia (`unshare -Ur true` dá
  `Operation not permitted`);
- **o helper setuid `chrome-sandbox`:** fica no pacote separado
  `chromium-sandbox` (no bookworm também), e mesmo instalado não serviria,
  porque o `dev-docker` roda com `--security-opt no-new-privileges`, que
  anula o setuid.

O Playwright passa `--no-sandbox` por conta própria; o Puppeteer não. A frase
"Puppeteer already uses it" do `sandbox/AGENTS.md` estava certa sobre o
caminho do navegador, mas o Puppeteer nunca chegava a abrir. Como o pacote e
as flags do container são os mesmos no bookworm, o problema muito
provavelmente já existia antes do trixie (não testado lá).

## Solução

O `/usr/bin/chromium` do Debian é um script que lê os arquivos de
`/etc/chromium.d/` antes de abrir o navegador. A imagem cria um com:

```sh
export CHROMIUM_FLAGS="$CHROMIUM_FLAGS --no-sandbox"
```

Assim qualquer ferramenta que use `/usr/bin/chromium` funciona sem configurar
nada. Desligar a sandbox interna é aceitável aqui: quem isola é o próprio
container.

## O que mudou no dev-sandbox

[`Dockerfile`](../../Dockerfile): arquivo `/etc/chromium.d/no-sandbox`.
