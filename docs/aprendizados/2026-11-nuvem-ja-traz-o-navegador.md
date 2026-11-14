# Na nuvem do Claude, copiar a configuração de navegador do Docker atrapalha

- **Data:** 2026-11
- **Ambiente:** claude.ai/code, ambiente da Anthropic (Ubuntu 24.04, imagem de
  27/10/2026), Playwright 1.63 global, Chrome for Testing 153, Puppeteer 24,
  Claude Code 2.1.325
- **Base:** evidência: sessão aberta com um setup script copiado do `Dockerfile`;
  testes com o Playwright da imagem, com o Playwright 1.55 fixado num projeto e
  com o Puppeteer; leitura do ambiente salvo

## Sintoma
Um setup script feito a partir do `Dockerfile`, mais as variáveis
`PLAYWRIGHT_BROWSERS_PATH`, `PUPPETEER_EXECUTABLE_PATH` e
`PUPPETEER_SKIP_DOWNLOAD` no ambiente:

- baixou 700 MB de Chromium para `/opt/ms-playwright`, que nada usava;
- as variáveis não valiam: na sessão, `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`
  e `PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome`;
- criou `/usr/bin/chromium` como link para o binário do Chrome, e o Puppeteer
  falhava com ele: `Failed to launch the browser process`. O binário explica:
  `Running as root without --no-sandbox is not supported`.

## Causa
- A imagem da nuvem já traz o Playwright global com os navegadores dele em
  `/opt/pw-browsers` e já define `PLAYWRIGHT_BROWSERS_PATH`,
  `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` e `PUPPETEER_EXECUTABLE_PATH`.
  `chromium.launch()` e `puppeteer.launch()` funcionam sem opção nenhuma.
- `/usr/bin/google-chrome` é um script que acrescenta `--no-sandbox` quando
  roda como `root`. Na nuvem tudo roda como `root`, então só ele serve de
  caminho fixo para o Puppeteer.
- O setup script definia o próprio `PLAYWRIGHT_BROWSERS_PATH`, por isso o
  `playwright install` não viu os navegadores que já existiam.
- Os nomes das variáveis foram salvos com espaços na frente
  (`   PLAYWRIGHT_BROWSERS_PATH`), provavelmente por colar texto recuado. O
  formulário aceita sem avisar, e a sessão ignora a variável. Aqui foi sorte:
  se valesse, o Puppeteer apontaria para o link quebrado.

## Solução
- Não baixar navegador nem definir variáveis de navegador na nuvem.
- Para manter o caminho do Docker: `ln -sf /usr/bin/google-chrome /usr/bin/chromium`.
  Com isso, Playwright e Puppeteer funcionam também por `/usr/bin/chromium`.
- Projeto que fixa outra versão do Playwright: igual ao Docker,
  `executablePath: '/usr/bin/chromium'`. Testado com 1.55: sem a opção, falha
  com `Executable doesn't exist at /opt/pw-browsers/chromium_headless_shell-1187/...`;
  com ela, funciona.

Ao levar uma configuração para um ambiente novo, liste primeiro o que ele já
tem. Aqui, metade dos pacotes apt do script já vinha na imagem.

## O que mudou no dev-sandbox
- [`nuvem/setup.sh`](../../nuvem/setup.sh) e o guia [Usar na nuvem](../guias/nuvem.md).
- Triagem de ferramenta reportada: `cargo llvm-cov` e `cargo mutants` faltaram
  num projeto do usuário. Ficam como exemplo de extra por projeto no guia, fora
  do `nuvem/setup.sh` e do `Dockerfile`: servem a projetos Rust com essas
  práticas de teste, e o binário pronto instala em segundos quando precisar.
