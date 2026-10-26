# O Playwright ignora o Chromium da imagem e pede para baixar navegadores

- **Data:** 2026-10
- **Ambiente:** imagem dev-sandbox (Debian 12), Chromium 156, Node 22, Playwright 1.64.1
- **Base:** evidência: teste dentro do container, com e sem `executablePath`, e
  busca da variável no código do `playwright-core` 1.64.1

## Sintoma
O `Dockerfile` define `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium`,
e o `sandbox/AGENTS.md` dizia que o Playwright "já aponta" para o Chromium da
imagem. Mesmo assim, `chromium.launch()` falha:

```
browserType.launch: Executable doesn't exist at /tmp/dev-home/.cache/ms-playwright/chromium_headless_shell-1248/...
Looks like Playwright was just installed or updated.
Please run the following command to download new browsers:
```

O agente segue a mensagem, roda `npx playwright install` e baixa centenas de
MB para o `$HOME`: exatamente o que a instrução queria evitar.

## Causa
O Playwright não lê `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. A variável não
aparece no código do `playwright-core`; ele só procura os navegadores que ele
mesmo baixa, em pastas com versão no nome (`chromium_headless_shell-1248`).
O Puppeteer, ao contrário, lê `PUPPETEER_EXECUTABLE_PATH`, e essa funciona.

Não há como configurar isso só na imagem de forma estável:
- não existe variável de ambiente para o caminho do executável;
- `PLAYWRIGHT_BROWSERS_PATH` exige a pasta com o número de versão exato, que
  muda a cada versão do Playwright.

O lugar certo é o projeto: a opção `executablePath` no `launch()` ou no
`playwright.config`.

## Solução
```js
chromium.launch({ executablePath: '/usr/bin/chromium' })
// ou, no playwright.config:
// use: { launchOptions: { executablePath: '/usr/bin/chromium' } }
```

Com isso o teste roda com o Chromium da imagem, sem baixar nada. O Chromium do
sistema não é a versão exata que o Playwright espera; funcionou no teste, mas
um recurso muito novo do Playwright pode falhar.

## O que mudou no dev-sandbox
- `sandbox/AGENTS.md`: a instrução manda usar `executablePath` em vez de baixar
  navegadores.
- `Dockerfile`: removida a `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, que não tinha
  efeito e fazia parecer que o Playwright já estava configurado.
