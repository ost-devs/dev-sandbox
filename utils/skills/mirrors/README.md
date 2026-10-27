# Mirrors: cópias de repositórios de fora

Às vezes o Claude precisa ler muitos arquivos de outro repositório: a
documentação do Rust, o código de uma biblioteca, os exemplos de outro
projeto. Buscar página por página na web enche o contexto. Com a skill
`mirrors`, o repositório fica copiado em `mirrors/<nome>/` dentro do seu
projeto, e o Claude lê dali.

Instalação: [`utils/README.md`](../../README.md#instalar).

## Como fica no seu projeto

| Arquivo | O que é | Vai pro git? |
|---|---|---|
| `mirrors/mirrors.json` | A lista: de onde vem cada cópia e em qual commit | Sim |
| `mirrors/<nome>/` | A cópia. Sem `.git` e somente leitura | Não |
| `mirrors/<nome>/.mirror-commit` | O commit que está na cópia | Não |
| `.gitignore` | Ganha duas linhas: `/mirrors/*` e `!/mirrors/mirrors.json` | Sim |

A skill cria o `mirrors.json` e as linhas do `.gitignore` na primeira vez,
mesmo numa pasta que ainda não é repositório git: assim, depois do `git init`,
as cópias já ficam fora do commit.

Por que somente leitura e sem `.git`: assim o Claude não edita a cópia por
engano (a edição seria perdida na próxima atualização), e nenhum hook do git
do repositório de fora roda na sua máquina. Links simbólicos que apontam para
fora da cópia são apagados.

## Fixo ou sempre atualizado

| Modo | Quando usar | Exemplo |
|---|---|---|
| **Fixo** (*pin*): guarda um commit | Código ou especificação que seus documentos citam. A versão só muda quando você pede | Uma biblioteca que você estuda |
| **Sempre atualizado** (*follow*): pega o commit mais novo a cada atualização | Documentação que muda e que você quer sempre em dia | A documentação do Rust, o próprio dev-sandbox |

## Pedir ao Claude

Fale normalmente, ou use `/mirrors`:

| Você quer | Peça |
|---|---|
| Copiar um repositório | "espelhe https://github.com/rust-lang/book como rust-book, sempre atualizado" |
| Só uma parte de um repositório grande | "espelhe só a pasta `src` de ..." |
| Atualizar tudo (ou baixar depois de clonar o projeto) | `/mirrors` |
| Ver o que está faltando ou velho | `/mirrors check` |
| Fixar na versão atual | `/mirrors pin rust-book` |
| Fixar na versão publicada (a tag `1.2.3` ou `v1.2.3`) | "fixe lezer/common na versão 1.5.2" |
| Seguir vários de uma vez | "deixe todos os membros de lezer sempre atualizados" |
| Tirar um espelho | `/mirrors remove rust-book` |

Depois de adicionar, fixar ou remover, faça commit do `mirrors/mirrors.json`.

## Rodar sem o Claude

O script funciona sozinho, de qualquer pasta dentro do projeto:

```bash
python3 ~/.claude/skills/mirrors/fetch_mirrors.py --help
```

Exemplos:

```bash
# o .claude/ do dev-sandbox, sempre atualizado
python3 ~/.claude/skills/mirrors/fetch_mirrors.py --add dev-sandbox https://github.com/ost-devs/dev-sandbox --include .claude --follow

# baixar tudo que está no mirrors.json (por exemplo, depois de clonar o projeto)
python3 ~/.claude/skills/mirrors/fetch_mirrors.py

# o que está faltando ou desatualizado
python3 ~/.claude/skills/mirrors/fetch_mirrors.py --check
```

Apagar uma cópia na mão exige devolver a permissão de escrita antes:
`chmod -R u+w mirrors/<nome> && rm -rf mirrors/<nome>`. O `--remove` faz isso
sozinho.

## Licença

Copiar código de outra pessoa para o seu disco é permitido pela maioria das
licenças, mas **usar** o código no seu projeto depende da licença. A skill
pede para registrar a licença de cada espelho no `mirrors.json`. Para
workspaces Rust com crates de licenças diferentes, o campo
`"license_check": "cargo"` faz a cópia recusar crates com licença fora da
lista.
