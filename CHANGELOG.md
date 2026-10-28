# Changelog

Mudanças do dev-sandbox por versão. Detalhes e motivos: [`DOCUMENTACAO.md`](DOCUMENTACAO.md) e
[`docs/aprendizados/`](docs/aprendizados/README.md).

## v0.5 (em desenvolvimento)

O dev-sandbox passa a ser também um **kit para trabalhar com o Claude Code em qualquer projeto**:
fontes externas copiadas para o projeto, guias escritos a partir delas e conferidos na documentação
oficial. Nada muda na imagem nem no `dev-docker`.

- [`/mirrors`](utils/skills/mirrors/SKILL.md) copia três tipos de fonte para `mirrors/`, só
  leitura e fora do git: repositórios git ([guia](docs/claude-code/mirrors.md)), sites de
  documentação com `llms.txt` ([guia](docs/claude-code/mirrors-de-sites.md)) e artigos da web em
  Markdown, um, uma lista ou uma cadeia, com o Defuddle do Obsidian Web Clipper
  ([guia](docs/claude-code/mirrors-de-artigos.md)).
  - Fixa na versão publicada (`--pin <alvo> @1.2.3` ou `@package`) e opera conjuntos em lote.
  - Cria as linhas do `.gitignore` mesmo antes do `git init`.
  - `--stale` aponta os guias que citam páginas que mudaram; `--max-age` evita baixar de novo a
    cada busca; ao espelhar um site, avisa se a documentação está num repositório git.
  - 15 testes sem internet, e uma rule que manda rodá-los a cada mudança.
- [`/estudar`](utils/skills/estudar/SKILL.md): transforma artigos em guias do projeto. Captura,
  deixa você escolher o que seguir, confere números e versões na fonte oficial, mostra o plano e
  só então escreve. Aprende com cada estudo e com as suas correções
  ([calibração](docs/claude-code/estudar-calibracao.md)).
- [`/montar-consultor`](docs/claude-code/montar-consultor.md): o pesquisador ganha um espelho da
  documentação (cita o texto exato em vez de buscar na web); a auditoria lista guias com fontes
  alteradas; as rules pedem teste para cada bug corrigido.
- [`/share-memories`](utils/skills/share-memories/SKILL.md): leva uma memória para todos os
  projetos, uma lista ou uma categoria, com uma cópia só e um link em cada projeto; o Claude
  decide o que é geral e só reescreve uma memória com a sua permissão. Instala os próprios hooks,
  cria e muda grupos, opera em lote ([guia](docs/claude-code/compartilhar-memorias.md)). 25
  testes sem internet.
- [Inglês para devs](docs/ingles-para-devs/README.md): nomes e comandos para a IA ficam em
  inglês; o [glossário](docs/ingles-para-devs/glossario.md) explica cada um, com pronúncia.
- Neste repositório: a documentação oficial do Claude Code e da API do Claude fica em
  `mirrors/`, e o agente `claude-code-pesquisador` consulta a cópia local primeiro.
- Guias novos: [base de conhecimento sob demanda](docs/claude-code/base-de-conhecimento.md),
  [quanto custa uma sessão](docs/claude-code/por-baixo-dos-panos/quanto-custa.md) e
  [limite de uso](docs/claude-code/limite-de-uso.md).
- Corrigido: [modelo e esforço](docs/claude-code/modelo-e-esforco.md) dizia que não existe modelo
  Mythos (existe, só para organizações verificadas).
- [Aprendizado](docs/aprendizados/2026-10-robots-txt-403-proibe-tudo.md): o leitor de
  `robots.txt` do Python tratava um 403 como "tudo proibido".

**Ao atualizar da v0.4:** `git pull` e copie as skills de novo para `~/.claude/skills/`
([como](utils/README.md#instalar)). Para capturar artigos da web, rode também
`npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts` (precisa de Node.js). Não precisa
reconstruir a imagem.

## v0.4 (fechada; falta o teste no host)


- Submódulos: `.git/modules/*/hooks` e `config` também somente leitura.
- Relatório de saída: ao sair, o `dev-docker` lista os arquivos que rodam no host e mudaram na
  sessão ([segurança](docs/guias/seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container)).
- `sandbox/managed-settings.json`: o Claude Code não abre as credenciais dos agentes com as
  ferramentas de leitura e edição.
- `sandbox/AGENTS.md` mais curto; a versão integral fica em `sandbox/AGENTS-completo.md`, fora
  da imagem.
- `sandbox/AGENTS.md`: ao passar um caminho para o usuário abrir, o agente traduz
  `/tmp/dev-home/...` para o caminho do host.
- Removida `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, que o Playwright não lê
  ([aprendizado](docs/aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md)).
- Guias novos: [atualização](docs/guias/atualizacao.md) e
  [instrução ou mecanismo](docs/claude-code/instrucao-ou-mecanismo.md) e [branches](docs/guias/branches.md).
- Pasta [`utils/`](utils/README.md): skills para usar em qualquer projeto. `/montar-consultor` monta o
  consultor do projeto ([guia](docs/claude-code/montar-consultor.md)); `/mirrors` guarda cópias
  somente leitura de repositórios de fora.
- Corrigido: o `deny` de credenciais cobre `cat`/`head`/`sed` no terminal (documentação oficial);
  o que passa é um script que abra o arquivo sozinho.
- Testado só a seco (`bash -n` e `sudo` falso); falta o teste real no host. Novidades vão para a v0.5.

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
