# Atualizar o dev-sandbox

Dentro do container nada se atualiza sozinho: tudo vem da imagem, e o container
é destruído no `exit`. Um `claude update`, um `rustup update` ou um `npm install -g`
feito lá dentro some na próxima sessão. Quem atualiza é o **build da imagem**.
Já o host (Docker, kernel, o git do seu PC) segue as atualizações do seu sistema.

## Resumo

| O quê | Como | Quando |
|---|---|---|
| Script `dev-docker` e documentação | `git -C ~/dev-sandbox pull` | Quando sair versão nova ([`CHANGELOG.md`](../../CHANGELOG.md)) |
| Agentes (Claude Code, Codex, agy) | [Rebuild só dos agentes](#2-só-os-agentes) | Toda semana, ou quando quiser um recurso novo |
| Resto da imagem (Debian, Chromium, git, Node, Rust, uv) | [Rebuild completo](#3-a-imagem-inteira) | Todo mês, e logo após uma falha de segurança grave no Chromium |
| Instruções dos agentes ([`sandbox/AGENTS.md`](../../sandbox/AGENTS.md)) | Rebuild normal (`sudo docker build -t dev-sandbox .`) | Depois de editar o arquivo |
| Dependências do projeto | O gerenciador do projeto, dentro do container, como sempre | Quando o projeto pedir |
| Docker, kernel e git do host | Atualizações do sistema | Sempre que o sistema oferecer |

## 1. O repositório

```bash
git -C ~/dev-sandbox pull
```

O comando `dev-docker` é um link para o script do repositório, então já está
atualizado. Leia a seção **"Ao atualizar"** da versão nova no `CHANGELOG.md`:
ela diz se é preciso reconstruir a imagem.

## 2. Só os agentes

```bash
cd ~/dev-sandbox
sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .
```

Os agentes ficam na última camada do `Dockerfile`, então só ela é refeita: leva
minutos. O auto-update do Claude Code fica desligado de propósito
(`DISABLE_AUTOUPDATER=1`), porque baixava versões que nunca eram usadas
([aprendizado](../aprendizados/2026-10-claude-autoupdate-orfao.md)).

Para conferir, abra uma sessão e rode `claude --version` (ou `codex --version`).

## 3. A imagem inteira

```bash
cd ~/dev-sandbox
sudo docker build --pull --no-cache -t dev-sandbox .
```

- `--pull` baixa a versão mais nova do Debian base.
- `--no-cache` refaz todas as camadas. Sem ele, o Docker reaproveita o
  `apt-get install` antigo e nenhuma correção chega.

Isso traz as correções de segurança do Debian, o Chromium, o git de dentro do
container, o Rust stable, o Node 22 mais recente e o `uv`. O Chromium é o que
mais pesa: o agente abre páginas da internet com ele.

Leva bem mais tempo (dezenas de minutos) e baixa alguns GB.

**Cuidados:**
- Se você usa Go ou Java, repita os `--build-arg WITH_GO=1` e `WITH_JAVA=1`.
  Sem eles, a imagem nova vem sem essas linguagens.
- A versão **maior** do Node é fixa (`setup_22.x` no `Dockerfile`). Para
  trocar de versão maior, edite essa linha.

### Guardar a versão anterior antes

Se o build novo quebrar algo, dá para voltar:

```bash
sudo docker tag dev-sandbox dev-sandbox:anterior   # antes do rebuild
DEV_IMAGE=dev-sandbox:anterior dev-docker          # usar a antiga, se precisar
sudo docker rmi dev-sandbox:anterior               # quando a nova estiver ok
```

## 4. Limpar depois

Cada rebuild deixa a imagem antiga sem nome (`<none>`), ocupando GB. Sessões já
abertas continuam na imagem antiga até o `exit`; a próxima `dev-docker` usa a
nova. Para liberar espaço, ver [onde a imagem ocupa espaço](./filosofia-da-imagem.md#onde-a-imagem-ocupa-espaço-no-seu-disco).

## 5. O host

- **Docker e kernel:** atualize pelo sistema (`sudo apt update && sudo apt upgrade`,
  ou o atualizador gráfico). São eles que seguram uma fuga do container
  ([segurança](./seguranca.md)).
- **O git do seu PC e o git do container são independentes.** O do host atualiza
  com o sistema; o do container, só no rebuild. Versões diferentes convivem bem
  no mesmo repositório. Mas é o git do **host** que roda os hooks e lê o
  `.git/config` quando você faz `commit` e `push` fora do container, e falhas de
  segurança do git já envolveram exatamente isso. Mantenha o do host em dia.
