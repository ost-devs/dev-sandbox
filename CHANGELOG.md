# Changelog

Mudanças do dev-sandbox por versão. Detalhes e motivos: [`DOCUMENTACAO.md`](DOCUMENTACAO.md) e
[`docs/aprendizados/`](docs/aprendizados/README.md).

## v0.4 (em desenvolvimento)

- Submódulos: `.git/modules/*/hooks` e `config` também somente leitura.
- Relatório de saída: ao sair, o `dev-docker` lista os arquivos que rodam no host e mudaram na
  sessão ([segurança](docs/guias/seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container)).
- `sandbox/managed-settings.json`: o Claude Code não abre as credenciais dos agentes com as
  ferramentas de leitura e edição.
- `sandbox/AGENTS.md` mais curto; a versão integral fica em `sandbox/AGENTS-completo.md`, fora
  da imagem.
- Removida `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, que o Playwright não lê
  ([aprendizado](docs/aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md)).
- Guia novo: [atualização](docs/guias/atualizacao.md).
- Testado só a seco (`bash -n` e `sudo` falso); falta o teste real no host.

**Ao atualizar da v0.3:** `git pull` e reconstrua a imagem (`sudo docker build -t dev-sandbox .`).

## v0.3

- `.git/hooks` e `.git/config` somente leitura também nos repositórios até dois níveis dentro
  da pasta montada; o início da sessão mostra quantos foram protegidos
  ([segurança](docs/guias/seguranca.md)).
- `dev-docker --nome NOME`: monta o projeto em `/NOME`, com memória do Claude em
  `~/.claude/projects/-NOME/`. `dev-docker --atalho NOME [pasta]`: cria `dev-docker-NOME`, que
  abre o projeto de qualquer lugar; sem caminho, usa a pasta onde o terminal está ("Abrir no
  terminal" no gerenciador de arquivos). Mostra a pasta e pede confirmação, recusa `/` e a home,
  avisa ao trocar o destino de um atalho; `dev-docker --atalhos` lista todos
  ([passo a passo](README.md#atalho),
  [trade-offs](DOCUMENTACAO.md#projeto-com-nome)).
- Guias novos: [trabalhar por projeto](docs/claude-code/projetos.md),
  [migrar memórias](docs/claude-code/migrar-memorias.md),
  [modelo e esforço](docs/claude-code/modelo-e-esforco.md) (esboço com diário de campo),
  [preservar conversas](docs/claude-code/preservar-conversas.md), com o hook opcional
  `extras/claude-hooks/arquivar-conversa.py`.
- Modelo de issue e de discussão para relatos de modelo e esforço (`.github/`).
- Aprendizados ganham o campo **Base** (evidência, documentação ou análise).
- Testado só a seco (`bash -n` e `sudo` falso); falta o teste real no host.

**Ao atualizar da v0.2:** `git pull`; o link `~/.local/bin/dev-docker` já aponta para o script
novo. Reconstrua a imagem (`sudo docker build -t dev-sandbox .`) para os agentes receberem o
`sandbox/AGENTS.md` atualizado. Nada muda se você não usar `--nome`; se passar a usar, a memória
do projeto fica numa pasta nova: [migrar](docs/claude-code/migrar-memorias.md).

## v0.2

- O projeto aparece no container no mesmo caminho do host (memória e conversas do Claude
  separadas por projeto); `/` e a home pedem confirmação.
- Portas opcionais e só em `127.0.0.1` (`DEV_PORTS`); nome único por sessão; vários containers
  ao mesmo tempo.
- `.git/hooks` e `.git/config` somente leitura (`DEV_GIT_RW=1` libera); `--cap-drop ALL`,
  `no-new-privileges`.
- Imagem completa (Go e Java opcionais), instruções do ambiente para os agentes
  (`sandbox/AGENTS.md`), scratchpad do Claude persistente, sem auto-update órfão.
- Documentação em `docs/`: segurança, backup, portas, imagem, Claude Code, aprendizados.

**Ao atualizar da v0.1:** reconstrua a imagem, troque a cópia antiga do script pelo link do
passo 3 da instalação, migre as memórias de `~/.claude/projects/-workspace/`
([como](docs/claude-code/migrar-memorias.md)) e apague o auto-update órfão
(`rm -rf ~/.cache/dev-sandbox/home/.local/share/claude ~/.cache/dev-sandbox/home/.local/bin/claude`).

## v0.1

Primeira versão: tudo montado em `/workspace`, portas fixas.
