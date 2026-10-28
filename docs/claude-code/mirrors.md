# Espelhar repositórios de fora

Este guia mostra **como** deixar outros repositórios (a documentação de uma
linguagem, a biblioteca que você estuda, os exemplos de outro projeto) dentro
do seu projeto, para o Claude ler sem buscar página por página na web. O
**porquê** está em [Trabalhar por projeto](./projetos.md#3-um-projeto-que-consulta-outros-repositórios).

Documentação de site, sem repositório git (como a do Claude Code): veja
[Espelhar sites de documentação](./mirrors-de-sites.md).

Quem faz o trabalho é a skill `/mirrors`, que vem no dev-sandbox
([`utils/skills/mirrors/`](../../utils/skills/mirrors/SKILL.md)). Ela baixa
cada repositório para `mirrors/<nome>/` e anota de onde veio e em qual commit.

## O que você terá no fim

| Arquivo no seu projeto | O que é | Vai pro git? |
|---|---|---|
| `mirrors/mirrors.json` | A lista: de onde vem cada cópia, em qual commit e com qual licença | Sim |
| `mirrors/<nome>/` | A cópia. Sem `.git` e somente leitura | Não |
| `mirrors/<nome>/.mirror-commit` | O commit que está na cópia | Não |
| `.gitignore` | Ganha duas linhas: `/mirrors/*` e `!/mirrors/mirrors.json` | Sim |

A skill cria o `mirrors.json` e as linhas do `.gitignore` na primeira vez,
mesmo numa pasta que ainda não é repositório git: assim, depois do
`git init`, as cópias já ficam fora do primeiro commit.

Por que somente leitura e sem `.git`: o Claude não edita a cópia por engano
(a edição seria perdida na próxima atualização), e nenhum hook do git do
repositório de fora roda na sua máquina. Links simbólicos que apontam para
fora da cópia são apagados.

## 1. Instalar a skill (uma vez só)

A skill fica na sua pasta pessoal do Claude, então serve para todos os seus
projetos. Rode **no host**, trocando `~/dev-sandbox` pelo lugar onde você
clonou o dev-sandbox:

```bash
mkdir -p ~/.claude/skills
cp -r ~/dev-sandbox/utils/skills/mirrors ~/.claude/skills/
```

A pasta leva o `SKILL.md` e o script, que a IA usa, e um `README.md` curto
para você consultar sem abrir o dev-sandbox. O Claude não carrega o README:
ele só entra no contexto se o Claude decidir abrir o arquivo.

Para capturar artigos da web, instale também o Defuddle (precisa de Node.js;
detalhes em [Capturar artigos da web](./mirrors-de-artigos.md#1-instalar-o-defuddle-uma-vez-só)):

```bash
npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts
```

Para atualizar depois de um `git pull` no dev-sandbox, rode no host. A
última linha só se você usa a captura de artigos: o `rm -rf` apaga o
Defuddle junto.

```bash
rm -rf ~/.claude/skills/mirrors
cp -r ~/dev-sandbox/utils/skills/mirrors ~/.claude/skills/
npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts
```

Conferir: abra uma sessão nova do Claude em qualquer projeto e digite
`/mirr`. A skill deve aparecer na lista.

## 2. Escolher o modo

| Modo | Quando usar | Exemplo |
|---|---|---|
| **Fixo** (*pin*): guarda um commit | Código ou especificação que seus documentos citam. A versão só muda quando você pede | Uma biblioteca que você está portando |
| **Versão publicada** (*pin* com `@versão`): o commit da tag da versão | Você quer exatamente o que foi publicado (no npm, por exemplo), não o que veio depois | `lezer/common` na versão que outro pacote exige |
| **Sempre atualizado** (*follow*): o commit mais novo a cada atualização | Documentação que muda e que você quer sempre em dia | A documentação do Rust, o `.claude/` do dev-sandbox |

Na dúvida, fixe. Com cópia fixa, o `mirrors.json` diz exatamente o que o
Claude leu quando escreveu cada documento.

## Como ler as tabelas

Cada linha mostra o mesmo pedido de dois jeitos: em palavras, numa sessão
do Claude, ou como comando. No comando, `...` é o começo:

| Onde | Troque `...` por |
|---|---|
| Numa sessão do Claude | `/mirrors` |
| No terminal, sem o Claude (host ou container, de qualquer pasta do projeto) | `python3 ~/.claude/skills/mirrors/fetch_mirrors.py` |

O que está entre `< >` é seu: `<rust-book>` é um exemplo de nome,
`<url>` é o endereço do repositório.

## 3. Adicionar

Pedindo ao Claude, ele confere a licença antes de baixar e a anota no
`mirrors.json`. No terminal, informe você: `--license <MIT>`.

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Copiar um repositório, sempre atualizado | "espelhe o <livro do Rust> e deixe sempre atualizado" | `... --add <rust-book> <url> --follow` |
| Só uma pasta de um repositório grande | "espelhe só a pasta <do editor> do <Zed>" | `... --add <zed> <url> --include <crates/editor>` |
| Vários repositórios da mesma organização | "espelhe o <common>, o <lr> e o <highlight> do <lezer>" | `... --add <lezer> '<url>/{member}'`, depois `... --follow <lezer/common> <lezer/lr>` |
| Um pacote na versão publicada | "fixe o <lezer/common> na versão <1.5.2>" | `... --pin <lezer/common> @<1.5.2>` |

O terceiro caso é um **conjunto** (*set*): uma entrada no `mirrors.json`
com o endereço `https://github.com/lezer-parser/{member}` e uma lista de
membros. Cada membro vira `mirrors/lezer/<membro>/`. Pedidos para o
conjunto inteiro ("deixe todo o lezer sempre atualizado") valem para todos
os membros de uma vez.

Na versão publicada, a skill procura a tag `1.5.2` ou `v1.5.2`. Se o
repositório não tiver a tag, ela para e avisa, em vez de pegar outro commit.

Workspace Rust com crates de licenças diferentes (o Zed, por exemplo): peça
para conferir a licença de cada crate. A skill põe `"license_check": "cargo"`
na entrada, e a cópia recusa toda pasta incluída cujo `Cargo.toml` tenha
licença fora da lista.

## 4. Revisar e fazer o commit

Confira no terminal do projeto:

```bash
git status
git diff mirrors/mirrors.json .gitignore
```

| Confira | Por quê |
|---|---|
| Só `mirrors/mirrors.json` e `.gitignore` aparecem no `git status` | As cópias não podem ir para o commit. Se aparecer `mirrors/<nome>/`, veja [problemas comuns](#problemas-comuns) |
| Cada entrada tem `license` | Copiar é permitido pela maioria das licenças; **usar** o código no seu projeto depende dela |
| O commit ou a tag é o que você queria | É a versão que seus documentos vão citar |

Faça o commit do `mirrors.json` junto com os documentos que citam a nova
versão. Assim cada commit do projeto diz qual versão das fontes ele cita.

## 5. No dia a dia

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Baixar tudo que está no `mirrors.json` (clonou o projeto em outra máquina) | "baixe os mirrors" | `...` |
| Saber o que está faltando ou velho | "algum mirror está velho?" | `... --check` |
| Subir uma cópia fixa para a versão mais nova | "atualize o <rust-book> para a versão mais nova" | `... --pin <rust-book>` |
| Tirar uma cópia | "tire o mirror <rust-book>" | `... --remove <rust-book>` |

Depois de fixar ou remover, faça commit do `mirrors.json`.

O `check` também avisa quando uma cópia fixa não é o commit da versão que o
seu `package.json` declara (o commit veio depois da publicação). Se você
queria a versão publicada, ele mostra o comando para fixá-la.

## Mais comandos

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Ver todas as opções | "o que a mirrors sabe fazer?" | `... --help` |
| Listar os espelhos | "quais mirrors eu tenho?" | `... --list` |
| Ter as skills e agentes do dev-sandbox para consultar, sempre atualizados | "espelhe a pasta `.claude` do dev-sandbox, sempre atualizada" | `... --add dev-sandbox <url do dev-sandbox> --include .claude --follow` |
| Fixar na versão que o `package.json` do repositório declara | "fixe o <lezer/common> na versão do package.json" | `... --pin <lezer/common> @package` |
| Fixar todos os membros de um conjunto no commit mais novo | "fixe todo o <lezer>" | `... --pin <lezer>` |

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `/mirrors` não aparece | Skill não instalada em `~/.claude/skills/`, ou sessão aberta antes da instalação | Confira com `ls ~/.claude/skills/mirrors/SKILL.md` e abra uma sessão nova |
| `warning .gitignore: another rule overrides...` | Outra linha do `.gitignore` (por exemplo `mirrors/`) ignora também o `mirrors.json` | Apague essa linha e deixe só as duas da skill |
| `mirrors/<nome>/` aparece no `git status` | O `.gitignore` foi apagado ou editado | Rode `/mirrors` de novo: ele devolve as duas linhas |
| `Permission denied` ao apagar a cópia | A cópia é somente leitura de propósito | Use `/mirrors --remove <nome>`. À mão: `chmod -R u+w mirrors/<nome> && rm -rf mirrors/<nome>` |
| `version 1.2.3 has no tag 1.2.3 or v1.2.3` | O repositório não criou tag para essa versão (comum quando o `package.json` já tem a próxima versão, ainda não publicada) | Escolha uma versão que tenha tag, ou fixe num commit |
| `unpinned <nome>` | O membro foi criado sem modo | `/mirrors --pin <nome>` ou `/mirrors --follow <nome>` |
| `refused ... license not in` | Num workspace Rust com `"license_check": "cargo"`, uma pasta incluída tem licença fora da lista | Tire a pasta do `include` ou, se a licença serve, acrescente-a em `license` |

## Base

Fatos do Claude Code conferidos na página oficial de
[skills](https://code.claude.com/docs/en/skills):

- skill pessoal em `~/.claude/skills/<nome>/` vale em todos os projetos;
- `${CLAUDE_SKILL_DIR}` aponta para a pasta da skill, e é assim que ela acha
  o script.

Comportamento do script testado num diretório sem `.git`, com um conjunto de
três repositórios do `lezer-parser` e tags com e sem `v` (git 2.39).

Conferido em outubro/2026 (Claude Code 2.1.310).
