# Changelog

Mudanças do dev-sandbox por versão. Detalhes e motivos: [`DOCUMENTACAO.md`](DOCUMENTACAO.md) e
[`docs/aprendizados/`](docs/aprendizados/README.md).

## v0.3 (branch `feat/workspace-multi-repo`, ainda não na `main`)

- `.git/hooks` e `.git/config` somente leitura também nos repositórios até dois níveis dentro
  da pasta montada; o início da sessão mostra quantos foram protegidos
  ([segurança](docs/guias/seguranca.md)).
- `dev-docker --nome NOME`: monta o projeto em `/NOME`, com memória do Claude em
  `~/.claude/projects/-NOME/`. `dev-docker --atalho NOME [pasta]`: cria `dev-docker-NOME`, que
  abre o projeto de qualquer lugar ([trade-offs](DOCUMENTACAO.md#projeto-com-nome)).
- Guias novos: [trabalhar por projeto](docs/claude-code/projetos.md),
  [migrar memórias](docs/claude-code/migrar-memorias.md),
  [modelo e esforço](docs/claude-code/modelo-e-esforco.md) (esboço com diário de campo).
- Modelo de issue e de discussão para relatos de modelo e esforço (`.github/`).
- Aprendizados ganham o campo **Base** (evidência, documentação ou análise).
- Testado só a seco (`bash -n` e `sudo` falso); falta o teste real no host.

**Ao atualizar da v0.2:** `git pull`; o link `~/.local/bin/dev-docker` já aponta para o script
novo. Nada muda se você não usar `--nome`. Se passar a usar, a memória do projeto fica numa
pasta nova: [migrar](docs/claude-code/migrar-memorias.md).

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

**Ao atualizar da v0.1:** [README, "Vindo da v0.1?"](README.md#vindo-da-v01).

## v0.1

Primeira versão: tudo montado em `/workspace`, portas fixas.
