# DOCUMENTAÇÃO — dev-sandbox

Este documento explica **por que** cada parte do [`README.md`](./README.md)
é como é. Não é preciso ler tudo de uma vez — use os links do README para
pular direto na dúvida específica.

---

## Índice

1. [Instalar o Docker](#instalar-o-docker)
2. [Por que não usar o grupo docker](#por-que-nao-usar-o-grupo-docker)
3. [O problema de fundo: bind mount e UID](#o-problema-de-fundo-bind-mount-e-uid)
   - [Por que o projeto é montado no mesmo caminho do host](#por-que-o-projeto-e-montado-no-mesmo-caminho-do-host)
   - [Projeto com nome e atalhos](#projeto-com-nome)
4. [Por que /root precisa de permissões especiais](#por-que-root-precisa-de-permissoes-especiais)
5. [Por que $HOME não pode continuar sendo /root](#por-que-home-nao-pode-continuar-sendo-root)
6. [Por que a home inteira é montada, não pasta por pasta](#por-que-a-home-inteira-e-montada)
7. [Por que a ordem dos mounts importa](#por-que-a-ordem-dos-mounts-importa)
8. [Por que o cache do cargo fica separado](#por-que-o-cache-do-cargo-fica-separado)
9. [O que morre a cada sessão e o que persiste](#o-que-morre-a-cada-sessao-e-o-que-persiste)
10. [Arquivo de instruções por agente (GEMINI.md, CLAUDE.md, AGENTS.md)](#arquivo-de-instrucoes-por-agente)
11. [Configuração de cada agente](#configuracao-de-cada-agente)
12. [Testando o sandbox interno do agy](#testando-o-sandbox-interno-do-agy)
13. [Corrigindo arquivos antigos criados como root](#corrigindo-arquivos-antigos)
14. [Limpando o cache (sessão suspeita)](#limpando-o-cache)
15. [Modelo de segurança — resumo](#modelo-de-seguranca-resumo)
16. [Troubleshooting](#troubleshooting)

---

## Instalar o Docker

Primeiro, descubra se sua distro é uma derivada do Ubuntu/Debian (Linux
Mint, Pop!_OS, elementary OS, Zorin etc.) ou uma instalação "pura":

```bash
[ -f /etc/upstream-release/lsb-release ] && echo "DERIVADA — use a Opção B" || echo "PURA — use a Opção A"
```

### Opção A — Debian/Ubuntu puro

```bash
curl -fsSL https://get.docker.com | sh
```

### Opção B — Distro derivada (Mint, Pop!_OS etc.)

O script da Opção A pode detectar incorretamente a distribuição base em
algumas distros derivadas e montar o repositório com o codinome errado,
quebrando a instalação com erros do tipo `E: Impossível corrigir
problemas, você manteve (hold) pacotes quebrados.`

Nesse caso, instale manualmente apontando para o repositório Ubuntu
correto:

```bash
# remove instalações antigas conflitantes, se houver
sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null

# dependências
sudo apt update && sudo apt install -y ca-certificates curl gnupg

# chave GPG oficial do Docker
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# repositório usando o codinome Ubuntu BASE da distro (não o da derivada)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/upstream-release/lsb-release && echo "$DISTRIB_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

<a id="por-que-nao-usar-o-grupo-docker"></a>
## Por que não usar o grupo docker
Colocar seu usuário no grupo `docker` (`sudo usermod -aG docker $USER`)
equivale, na prática, a dar acesso root ao sistema para qualquer processo
rodando com seu usuário — o daemon do Docker roda como root, e qualquer
membro do grupo `docker` consegue montar `/` do host dentro de um
container e escrever nele, sem senha nenhuma.

Isso é especialmente relevante aqui porque o propósito inteiro deste setup
é rodar um agente de IA autônomo. Se esse agente (ou uma dependência que
ele instalar) for comprometido, o dano possível é proporcional ao que o
seu usuário consegue fazer — e "seu usuário consegue dar root a qualquer
processo sem senha" é um raio de dano muito maior do que "seu usuário
consegue rodar `docker` com `sudo`, que pede senha toda vez".

Mantendo fora do grupo, cada comando `docker` exige `sudo` — uma fricção
proposital: um processo comprometido não consegue digitar sua senha
sozinho.

---

## O problema de fundo: bind mount e UID

A pasta do projeto dentro do container é um **bind mount**: o container não tem uma cópia da sua
pasta, ele enxerga *a mesma pasta real* do host através de outro caminho.
Não existe tradução de identidade nesse tipo de mount — o UID que cria um
arquivo dentro do container é literalmente o UID gravado no arquivo no
disco do host.

Um `Dockerfile` sem `USER` definido roda como `root` (UID 0) por padrão.
Se o processo dentro do container criar:

```
~/Dev/meu-projeto/nota.md
```

o arquivo aparece no host como:

```
root root nota.md
```

— inacessível para edição por programas do seu usuário normal (Obsidian,
VS Code, `git`, etc.), porque seu usuário não é dono do arquivo e não está
no grupo dele.

**A correção:** fazer o processo dentro do container rodar com o mesmo
UID/GID do seu usuário no host, usando a flag nativa do Docker:

```bash
--user "$HOST_UID:$HOST_GID"
```

Com `HOST_UID="$(id -u)"` e `HOST_GID="$(id -g)"` obtidos *antes* de
iniciar o container, qualquer arquivo criado na pasta do projeto já nasce com
o dono certo — sem precisar rodar `chown` depois de cada sessão.

Essa é a única mudança realmente indispensável de todo o setup — o resto
deste documento existe para explicar as consequências dela e como lidar
com elas.

<a id="por-que-o-projeto-e-montado-no-mesmo-caminho-do-host"></a>
### Por que o projeto é montado no mesmo caminho do host

O Claude Code separa memória, histórico de conversas e `--continue` **pelo
caminho do projeto**. Se todo projeto aparecesse no mesmo caminho dentro do
container (como na v0.1, com tudo em `/workspace`), todos virariam um só
([detalhes](docs/claude-code/memoria-e-instrucoes.md#3-memória-dentro-do-dev-sandbox)).

Por isso `~/Dev/meu-projeto` aparece dentro do container como
`/home/voce/Dev/meu-projeto`, igualzinho. Além da memória, isso faz caminhos em
mensagens de erro e worktrees do git baterem dentro e fora. Duas exceções vão
para `/workspace` (ou para `/NOME`, com `--nome`): pastas de sistema (`/usr`,
`/tmp`...) e montagens amplas (`/` ou a home inteira), que ainda pedem
confirmação antes, porque entregam ao agente justamente o que o sandbox
deveria esconder.

<a id="projeto-com-nome"></a>
### Projeto com nome e atalhos

`dev-docker --nome meu-site` monta o projeto em `/meu-site` em vez do caminho
do host. O jeito prático de usar isso é o **atalho**:
`dev-docker --atalho meu-site` cria o comando `dev-docker-meu-site`, um script
de três linhas em `~/.local/bin/` que chama `dev-docker --nome meu-site <a pasta>`.

**Criar.** Rode uma vez, num terminal aberto na pasta do projeto. Sem caminho,
ele usa a pasta onde o terminal está; também dá para passar o caminho:
`dev-docker --atalho meu-site ~/Projetos/meu-site`.

```text
$ dev-docker --atalho meu-site
O comando dev-docker-meu-site vai abrir sempre esta pasta:
    /home/ana/Projetos/meu-site
Confirma? Digite 's' para criar: s
Pronto. De qualquer terminal, em qualquer pasta, digite:  dev-docker-meu-site
```

**Cuidado com a pasta.** O atalho guarda a pasta para sempre: confira se é a
que você quer abrir. Qualquer pasta serve, com ou sem git. O engano comum é
num projeto com git: rodar dentro de uma subpasta (`src`) em vez da raiz. Por
isso o script:

- mostra a pasta e só cria com `s`;
- avisa quando a pasta fica dentro de um repositório git sem ser a raiz dele,
  e mostra qual é a raiz;
- recusa `/` e pastas que contêm a sua home;
- ao recriar um atalho com o mesmo nome, mostra para onde ele aponta hoje
  antes de trocar;
- não sobrescreve um arquivo de `~/.local/bin/` que ele não criou.

**Corrigir, listar, apagar.** Errou a pasta: rode de novo o mesmo
`dev-docker --atalho meu-site` na pasta certa. Ver todos:
`dev-docker --atalhos`. Apagar: `rm ~/.local/bin/dev-docker-meu-site`. Moveu ou
renomeou a pasta do projeto (ou a do dev-sandbox): crie o atalho de novo.

**Nome ou caminho do host?**

| | Caminho do host (padrão) | `--nome` |
|---|---|---|
| Pasta da memória do Claude | `~/.claude/projects/-home-ana-Projetos-meu-site/` | `~/.claude/projects/-meu-site/` |
| Mesma memória em outro PC (via [backup](docs/guias/backup-e-git.md)) | só se o caminho for igual lá | sim, se o nome for o mesmo |
| Mesma memória que o Claude fora do container | sim | não |
| Caminhos nas mensagens de erro batem com o host (clicar no VS Code) | sim | não (`/meu-site/...`) |
| Precisa de `cd` antes | sim | não, com o atalho |

Dois projetos com o mesmo nome dividem a memória: escolha nomes únicos. Ao
trocar um projeto de um modo para o outro, a memória fica na pasta antiga;
mova uma vez ([como](docs/claude-code/migrar-memorias.md)).

---

<a id="por-que-root-precisa-de-permissoes-especiais"></a>
## Por que /root precisa de permissões especiais

Consequência direta da mudança acima: os instaladores de `agy` (e, se
ativado, do Claude Code via método npm) rodam durante o **build** da
imagem, que é sempre feito como `root`. Eles gravam o binário em
`/root/.local/bin` — a home do usuário que executou o instalador.

Só que em **runtime** o processo não é mais root — é o seu UID. E por
padrão, em imagens Debian, `/root` tem permissão `700`
(`drwx------`), dono `root:root`. Um UID diferente de 0 cai na categoria
"outros" e não tem nenhuma permissão sobre `/root` — nem de leitura, nem
de travessia (entrar no diretório). O binário existe, o `PATH` aponta
certo pra ele, mas o processo não consegue nem entrar em `/root` pra
chegar até `/root/.local/bin`. Resultado: `agy: command not found` ou
`Permission denied`, mesmo com tudo instalado corretamente.

A correção no `Dockerfile`:

```dockerfile
RUN chmod 755 /root \
    && chmod -R a+rX /root/.local
```

- `chmod 755 /root` — libera travessia (`+x`) e leitura (`+r`) do
  diretório para qualquer usuário, mas não escrita. Ninguém além de root
  consegue criar ou apagar arquivos direto em `/root`.
- `chmod -R a+rX /root/.local` — o `X` maiúsculo (diferente de `x`
  minúsculo) só adiciona permissão de execução a diretórios e a arquivos
  que **já eram executáveis**. Isso dá exatamente o necessário — ler o
  binário e executá-lo — sem tornar executável, por engano, um arquivo de
  dados (um `.json` de config, por exemplo) que não deveria ser.

Node.js **não precisa** desse tratamento: pacotes globais (`npm install
-g`) vão para `/usr/local/lib/node_modules` e `/usr/local/bin`, que já são
`755` por padrão (diretórios de sistema, não uma home de usuário
específico). Rust também não precisa de ajuste extra além do que já está
no bloco original (próxima seção).

---

<a id="por-que-home-nao-pode-continuar-sendo-root"></a>
## Por que $HOME não pode continuar sendo /root

Mesmo com `/root` legível, ferramentas que escrevem configuração ou cache
(o `npm`, o `agy`, o `claude`, o `codex`) fazem isso em `$HOME` — que
precisa ser **gravável**, não só legível. Seu UID no runtime não tem
permissão de escrita em `/root` (só `755`, de propósito — ver seção
anterior).

A solução é redirecionar `$HOME` para um lugar que qualquer UID consiga
escrever:

```dockerfile
RUN mkdir -p /tmp/dev-home && chmod 1777 /tmp/dev-home
ENV HOME=/tmp/dev-home
```

`1777` é o mesmo esquema de permissão do `/tmp` padrão do sistema: todo
mundo pode criar arquivos ali, mas o *sticky bit* (o `1` inicial) impede
que um usuário apague ou renomeie um arquivo criado por outro usuário —
relevante se você algum dia rodar este setup numa máquina compartilhada
por múltiplas contas.

Esse `ENV HOME` no `Dockerfile` já cobre o build; ele é reforçado de novo
em runtime, no script, via `--env "HOME=/tmp/dev-home"` — redundante mas
inofensivo, e garante que o valor não dependa de nenhuma outra
configuração da imagem.

---

<a id="por-que-a-home-inteira-e-montada"></a>
## Por que a home inteira é montada

Antes de chegar nesse ponto, uma versão anterior deste setup montava
pasta por pasta: `.npm` num `--mount`, `.gemini` em outro. Funciona, mas
tem uma lacuna: qualquer ferramenta *nova* que você instalar no futuro
(um linter que cria `~/.eslintrc-cache`, outro CLI qualquer) grava em
`/tmp/dev-home/algum-lugar-novo` — que não tem mount nenhum — e esse
estado simplesmente desaparece quando o `--rm` destrói o container.

Em vez de tentar prever cada ferramenta futura, monta-se `$HOME` inteiro:

```bash
DEV_HOME_PATH="$HOME/.cache/dev-sandbox/home"
--mount "type=bind,src=$DEV_HOME_PATH,dst=/tmp/dev-home"
```

Qualquer coisa que qualquer processo gravar em `$HOME` dentro do
container — sem exceção, sem precisar listar — já nasce persistente no
host, em `~/.cache/dev-sandbox/home`.

> **⚠️ Contrapartida de segurança:** com `$HOME` inteiro persistente,
> qualquer coisa que um agente comprometido (por prompt injection, por
> exemplo) escrever ali também sobrevive entre sessões — um cache de
> `npm` envenenado, uma dotfile maliciosa nova. Antes, com mounts
> individuais, o dano de uma sessão comprometida ficava restrito às
> pastas especificamente montadas. Na prática o conteúdo de `$HOME` é
> cache/config de ferramentas, não binários executados automaticamente,
> então o risco adicional é baixo — mas é o preço real dessa
> conveniência. Ver [Limpando o cache](#limpando-o-cache) se algum dia
> desconfiar de uma sessão.

---

## Por que a ordem dos mounts importa

Você provavelmente quer que `.gemini` (ou `.claude`, `.codex`) dentro do
container aponte para a pasta **real** do seu host — a mesma que uma
instalação nativa do agente usaria — em vez de uma cópia nova dentro do
cache genérico. Isso é possível porque o Linux permite montar uma pasta
*dentro* de outra que já é um ponto de montagem:

```bash
--mount "type=bind,src=$DEV_HOME_PATH,dst=/tmp/dev-home"        # 1º: preenche $HOME inteiro
--mount "type=bind,src=$GEMINI_PATH,dst=/tmp/dev-home/.gemini"  # 2º: sobrepõe só essa subpasta
```

O resultado: `/tmp/dev-home` inteiro vem do cache genérico, **exceto**
`/tmp/dev-home/.gemini`, que é substituída pela segunda mount — apontando
pra `~/.gemini` real do host. Mesma lógica se você ativar `.claude` e
`.codex`: cada overlay decide qual subpasta usa a pasta real do host em
vez do cache genérico.

A ordem em que os mounts são declarados no comando importa: o mount "de
fora" (a pasta inteira) precisa ser processado antes dos mounts "de
dentro" (as subpastas específicas). Se a ordem fosse invertida, o mount
da pasta inteira, vindo depois, cobriria tudo — inclusive o caminho que o
overlay específico já tinha ocupado — escondendo-o.

Isso explica por que `.gemini`/`.claude`/`.codex` vêm da pasta real do
host (login compartilhado com o uso nativo do agente, se você usa fora do
Docker também), enquanto qualquer outra coisa nova em `$HOME` cai
automaticamente no cache genérico, sem esforço extra.

A mesma regra vale para a proteção do `.git` (v0.2): o repositório é montado
primeiro, com escrita, e depois `.git/hooks` e `.git/config` são montados por
cima **somente leitura**. Motivo em [segurança](docs/guias/seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container).

> Exceção conhecida: `~/.claude.json` (estado do Claude Code, fora da pasta
> `.claude`) cai no cache genérico, separado do arquivo do host. Ver
> [sessões e persistência](docs/claude-code/sessoes-e-persistencia.md#por-que-o-claudejson-fica-separado).

---

## Por que o cache do cargo fica separado

`.gemini`/`.claude`/`.codex` são **identidade** — o mesmo login, a mesma
conta, faz sentido compartilhar entre onde quer que você rode o agente.

O cache do `cargo` é diferente: é cache de **pacotes compilados para um
toolchain específico**. O Rust instalado dentro da imagem Docker
(`/usr/local/cargo`) é uma instalação separada de qualquer Rust que você
tenha nativamente no seu Linux (`~/.cargo`, se instalado via `rustup` fora
do Docker) — possivelmente versões diferentes do compilador. Misturar os
caches seria o problema, não a solução: um crate compilado/cacheado numa
versão do `rustc` pode não ser compatível com outra.

Por isso o cargo tem mount próprio, fora do esquema de overlay de
`$HOME`, apontando para uma pasta dedicada só ao Docker:

```bash
CARGO_CACHE_PATH="$HOME/.cache/dev-sandbox/cargo"
--mount "type=bind,src=$CARGO_CACHE_PATH,dst=/usr/local/cargo/registry"
```

Isso também explica por que ele **não** é filho de `$HOME`: `CARGO_HOME`
é um `ENV` fixo em `/usr/local/cargo`, independente de onde `$HOME`
aponta — por isso o mount de `$DEV_HOME_PATH` não afeta o cargo em nada.

Se você quiser mesmo assim compartilhar cache com um Rust nativo do host
(aceitando o risco de incompatibilidade caso as versões divirjam), o
mesmo truque de overlay de `.gemini` funciona aqui: monte seu
`~/.cargo/registry` real por cima de `/usr/local/cargo/registry`. Não é a
recomendação padrão deste guia.

---

<a id="o-que-morre-a-cada-sessao-e-o-que-persiste"></a>
## O que morre a cada sessão e o que persiste

A regra não é "instalação grande morre, coisa pequena sobrevive" — é
estritamente sobre **onde** o arquivo é escrito no filesystem. Cai dentro
da pasta do projeto, `$HOME` (`/tmp/dev-home`) ou `/usr/local/cargo/registry`
→ sobrevive. Cai em qualquer outro lugar do sistema (`/usr`, `/lib`,
`/var`, etc.) → morre com o `--rm`, não importa o tamanho ou a
importância da ferramenta.

| Como instala | Onde grava | Sobrevive à sessão? |
|---|---|---|
| `apt-get install <pacote>` | `/usr`, `/var/lib/dpkg` (sistema) | ❌ Não |
| `npm install -g <pacote>` | `/usr/local/lib/node_modules` (padrão) | ❌ Não |
| `npm install <pacote>` (dentro do projeto) | `<projeto>/node_modules` | ✅ Sim |
| `cargo install <binário>` | `$CARGO_HOME/bin` = `/usr/local/cargo/bin` | ❌ Não — só `.../registry` está montado |
| `cargo build` (dependências) | `$CARGO_HOME/registry` | ✅ Sim |
| `pip install --user <pacote>` | `$HOME/.local/...` | ✅ Sim (com `$HOME` inteiro montado) |
| `uv venv` / `python -m venv .venv` (dentro do projeto) | `<projeto>/.venv` | ✅ Sim |
| Config/cache de qualquer CLI novo | `$HOME/...` | ✅ Sim, automaticamente |
| Temporários e scratchpad do Claude Code | `$CLAUDE_CODE_TMPDIR` = `$HOME/.cache/claude-tmp` | ✅ Sim (v0.2) |
| Arquivo solto em `/tmp` | `/tmp` do container | ❌ Não |

`apt-get install` e `npm install -g` nem chegam a gravar: sem `root`, dão
`Permission denied`. Isso é proposital.

O caso do `cargo install` é o mais contraintuitivo: o **cache de
compilação** (`registry`) persiste, mas o **binário final** instalado via
`cargo install` some — porque só a subpasta `registry` está montada, não
`$CARGO_HOME` inteiro. Se isso incomodar no dia a dia, a correção é
trocar o mount de `.../registry` por `$CARGO_HOME` inteiro — mesmo
princípio já usado para `$HOME`.

**Como confirmar isso na prática** (sem depender só da teoria):

```bash
dev-docker
```

Dentro da sessão, sem passar pelo agente (pra isolar a variável):

```bash
touch /tmp/efemero.txt ~/persistente.txt
exit
```

Entre de novo (`dev-docker`) e rode `ls /tmp/efemero.txt ~/persistente.txt`:
o primeiro sumiu, o segundo continua.

### Por que isso é uma boa prática, não uma limitação

Forçar qualquer dependência de sistema a ser promovida deliberadamente
pro `Dockerfile` evita acumular estado não versionado dentro do container
ao longo do tempo — o clássico "funciona na minha máquina" que ninguém
mais consegue reproduzir depois. Se um pacote de sistema é realmente
necessário, ele deveria estar documentado no `Dockerfile`, não instalado
silenciosamente numa sessão e esquecido.

---

<a id="arquivo-de-instrucoes-por-agente"></a>
## Arquivo de instruções por agente

Existem dois tipos de instrução, e misturar os dois era o problema do
antigo `GEMINI.md` deste repositório:

| Tipo | Fala sobre | Onde fica |
|---|---|---|
| **Do ambiente** | O container: o que persiste, sem `sudo`, portas, ferramentas que faltam | [`sandbox/AGENTS.md`](sandbox/AGENTS.md), dentro da imagem. Igual para todo projeto |
| **Do projeto** | O código: stack, comandos de teste, convenções | `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` na raiz de cada repositório |

O antigo `GEMINI.md` misturava os dois, citava caminhos que não existem neste
setup (`/root/.gemini`, `/root/.npm`) e mandava o agente rodar `apt-get
install`, que falha sem `root`. Ele foi substituído pelo `sandbox/AGENTS.md`.

### Instruções do ambiente

- **Claude Code** carrega sozinho: a imagem copia o arquivo para
  `/etc/claude-code/CLAUDE.md`, o local "managed" do Claude Code no Linux
  ([comprovado aqui](docs/aprendizados/2026-10-etc-claude-md-carrega-sozinho.md)).
- **Codex e agy** não têm um local equivalente garantido. Acrescente uma linha
  condicional ao arquivo global de cada um no host (`~/.codex/AGENTS.md`,
  `~/.gemini/GEMINI.md`), como no [README](README.md#instruções-do-ambiente-para-os-agentes).

### Instruções do projeto

| Agente | Arquivo lido na raiz do repositório |
|---|---|
| Antigravity CLI (agy) | `GEMINI.md` |
| Claude Code | `CLAUDE.md`; ou `AGENTS.md`, se não houver `CLAUDE.md` |
| Codex CLI | `AGENTS.md` |

Usa mais de um agente? Mantenha um `AGENTS.md` canônico. O Claude Code já lê
ele. Para o agy, um link: `ln -s AGENTS.md GEMINI.md`. Se precisar de algo só
para o Claude, crie um `CLAUDE.md` com `@AGENTS.md` na primeira linha e o
extra embaixo. Detalhes em [memória e instruções](docs/claude-code/memoria-e-instrucoes.md).

---

<a id="configuracao-de-cada-agente"></a>
## Configuração de cada agente

| Agente | Config principal | Credenciais |
|---|---|---|
| Antigravity CLI | `~/.gemini/antigravity-cli/settings.json` | dentro de `~/.gemini/` |
| Claude Code | `~/.claude/settings.json` | `~/.claude/.credentials.json` |
| Codex CLI | `~/.codex/config.toml` | `~/.codex/auth.json` |

Como `$HOME` dentro do container é redirecionado para `/tmp/dev-home` (e
`.gemini`/`.claude`/`.codex` têm overlay para a pasta real do host — ver
[seção anterior](#por-que-a-ordem-dos-mounts-importa)), cada agente
encontra sua config e credenciais automaticamente, sem nenhuma variável
de ambiente adicional — eles já respeitam `$HOME` por padrão.

### settings.json do agy

```json
{
  "toolPermission": "proceed-in-sandbox",
  "enableTerminalSandbox": true,
  "allowNonWorkspaceAccess": false
}
```

- **`toolPermission`** controla quanto o `agy` pede confirmação:
  `strict` (pede pra quase tudo) → `request-review` (revisão antes de
  editar/rodar) → `proceed-in-sandbox` (roda sozinho dentro do sandbox,
  confirma o resto) → `always-proceed` (nunca confirma).
- **`enableTerminalSandbox`** ativa um isolamento interno adicional (no
  Linux, via `nsjail`) para os comandos de terminal do `agy` — uma camada
  extra além do isolamento do Docker.
- **`allowNonWorkspaceAccess: false`** impede que as ferramentas do
  agente acessem qualquer coisa fora da pasta do projeto — inclusive suas
  próprias credenciais montadas em `.gemini`.

> **⚠️ Cuidado:** `toolPermission: always-proceed` combinado com o
> sandbox pode tornar a proteção inefetiva — há relatos do próprio agente
> conseguindo sugerir e aplicar um "bypass" nesse modo. Prefira
> `proceed-in-sandbox` ou `request-review` se a proteção importa.

### O que o Docker já cobre sozinho

`enableTerminalSandbox` e `allowNonWorkspaceAccess` não existem pra
proteger seu computador — isso o isolamento do container já faz de
graça, sempre, independente de configuração. Eles existem pra proteger as
duas pontes reais e vivas durante a sessão: a pasta do projeto e
suas credenciais montadas. Isso vale igualmente para Claude Code e Codex,
que têm seus próprios mecanismos de permissão equivalentes.

---

## Testando o sandbox interno do agy

Dentro de uma sessão `dev-docker`, peça ao agente (ou rode manualmente)
para criar um arquivo fora da pasta do projeto, em:

```
/tmp/teste-sandbox.txt
```

> **⚠️ Não teste em `/root`:** desde a correção do `Dockerfile`, `/root`
> está com permissão `755` (sem escrita para o seu UID). Testar ali
> sempre vai dar "Operation not permitted", **mesmo que o
> `enableTerminalSandbox` esteja quebrado** — porque a permissão Unix
> comum já bloqueia a escrita antes do `nsjail` entrar em ação, tornando
> o teste inválido. `/tmp` dentro do container é `1777` por padrão
> (gravável por qualquer UID, e é uma pasta **diferente** de
> `/tmp/dev-home`, que é a única persistente) — só um bloqueio ativo do
> `nsjail` impede a escrita ali.

- Se aparecer `Operation not permitted` ou erro equivalente → o `nsjail`
  está restringindo de verdade.
- Se o arquivo for criado sem erro → o sandbox não está restringindo
  nada nesse ambiente (pode ser isolamento aninhado, já que `nsjail`
  roda dentro de um container Docker).

Não confunda esse teste com o isolamento do Docker: mesmo que o arquivo
seja criado, isso não afeta seu PC real — o `/tmp` do container é
isolado do `/tmp` do host.

---

## Corrigindo arquivos antigos

Se você já rodou este setup (ou uma versão anterior sem `--user`) e tem
arquivos `root:root` em algum repositório:

```bash
cd ~/meu-projeto-afetado
sudo chown -R "$(id -u):$(id -g)" .
```

> **⚠️ Cuidado:** rode isso **só** dentro do repositório afetado. Nunca
> `sudo chown -R "$(id -u):$(id -g)" /` nem em uma pasta ampla que
> contenha outros dados do sistema — isso alteraria o dono de arquivos
> do sistema operacional que precisam continuar sendo de `root`.

---

## Limpando o cache

Com `$HOME` inteiro persistente (ver [seção 6](#por-que-a-home-inteira-e-montada)),
se você desconfiar do conteúdo de uma sessão (por exemplo, depois de rodar
o agente sobre um repositório de origem duvidosa), zere o cache genérico:

```bash
rm -rf ~/.cache/dev-sandbox/home
mkdir -p ~/.cache/dev-sandbox/home
```

Isso não afeta `.gemini`/`.claude`/`.codex` (pastas reais do seu host,
fora do cache genérico) nem o cache do cargo — se desconfiar deles
especificamente, limpe cada um à parte.

---

<a id="modelo-de-seguranca-resumo"></a>
## Modelo de segurança — resumo

| Camada | Função | Sempre ativa? |
|---|---|---|
| Docker (namespaces de mount) | Isola o filesystem do container do restante do sistema | Sim, sempre — não depende de nenhuma configuração |
| Bind mount do projeto | Expõe somente o repositório em uso | Sim |
| `.git/hooks` e `.git/config` somente leitura | Impede que o agente plante código que roda no host no próximo `git`, também nos repositórios até dois níveis dentro da pasta montada ([o que fica de fora](docs/guias/seguranca.md)) | Sim, a menos que `DEV_GIT_RW=1` (v0.2; repositórios internos desde a v0.3) |
| `--cap-drop ALL` + `no-new-privileges` | Tira do container privilégios de kernel de que ninguém precisa e bloqueia binários setuid | Sim (v0.2) |
| Portas só em `127.0.0.1` e só com `DEV_PORTS` | Nada do container fica visível na rede local | Sim (v0.2) |
| `--user UID:GID` | Impede que arquivos do workspace nasçam como `root` | Sim, enquanto o script tiver essa flag |
| `--rm` | Destrói o container ao terminar, sem deixar resíduo de sistema | Sim, enquanto o script tiver essa flag |
| Overlays específicos (`.gemini`/`.claude`/`.codex`) | Compartilham credenciais reais sem expor o resto do host | Sim |
| `allowNonWorkspaceAccess: false` (agy) e equivalentes | Impede acesso arbitrário fora do workspace pelas ferramentas do agente | Só se configurado assim |
| Sandbox interno de cada agente (`nsjail` etc.) | Restringe comandos durante a sessão, além do Docker | Depende de funcionar corretamente aninhado — testar (seção 12) |

**A correção essencial de todo o setup:** `--user "$HOST_UID:$HOST_GID"`,
com os valores obtidos antes de iniciar o container. Todo o resto deste
documento existe para lidar com as consequências dessa única mudança.

Esta tabela lista só o que **protege**. O que continua exposto (credenciais
montadas, internet de saída, arquivos do projeto que rodam no host) está em
[segurança](docs/guias/seguranca.md). Leia antes de usar o sandbox com
código de terceiros.

---

## Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `agy: command not found` dentro do container | Esqueceu de reconstruir a imagem após editar o `Dockerfile` | `sudo docker build -t dev-sandbox .` |
| Arquivo criado pelo agente continua `root:root` no host | Script antigo sem `--user`, ou você editou o script e removeu a flag | Confira a flag `--user "$HOST_UID:$HOST_GID"` no `dev-docker` |
| Login do agente pede autenticação toda sessão | Pasta de credenciais não montada, ou montada na ordem errada | Confira se o mount específico (`.gemini`/`.claude`/`.codex`) vem DEPOIS do mount de `$DEV_HOME_PATH` no comando |
| `Permission denied` ao rodar um binário instalado via `curl \| bash` | Faltou o `chmod 755 /root` + `chmod -R a+rX /root/.local` no `Dockerfile` para esse instalador específico | Adicione o mesmo tratamento já usado pro `agy` |
| Pacote instalado via `apt-get` some a cada sessão | Comportamento esperado — `/usr` não é persistente | Promova a instalação pro `Dockerfile` e reconstrua a imagem |
| Obsidian não abre/edita uma nota criada pelo agente | Arquivo antigo, criado antes da correção com `--user` | Rode o `chown` da [seção 13](#corrigindo-arquivos-antigos) |
| `failed to bind host port ... address already in use` | Outro programa do host (ou outro container) usa a porta pedida em `DEV_PORTS` | `ss -ltnp \| grep :<porta>` no host e escolha outra, ex.: `DEV_PORTS="8090:8080"` |
| `could not lock config file .git/config` ou `Read-only file system` em `.git/hooks` | Proteção do `.git` (v0.2), proposital | Faça a mudança no host, ou abra a sessão com `DEV_GIT_RW=1` |
| `claude --version` não muda depois de dias | Auto-update desligado na imagem (v0.2) | `sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .` |
| `/resume` mostra conversas de outros projetos | O projeto foi aberto em `/workspace` (pasta de sistema, `/` ou a home inteira), ou dois projetos usam o mesmo `--nome` | Abra pelo caminho do host ou com um `--nome` só dele |
| A memória ou as conversas de um projeto sumiram | O projeto foi aberto de outro jeito (outro caminho, ou com/sem `--nome`): o Claude procura em outra pasta | Reabra do jeito de antes, ou [migre as memórias](docs/claude-code/migrar-memorias.md); conversas: `claude --resume <id>` funciona de qualquer pasta |
| `dev-docker-<nome>: command not found` | `~/.local/bin` fora do `PATH`, ou o atalho foi criado noutra máquina | Passo 3 da instalação no README; recrie com `dev-docker --atalho <nome> <pasta>` |
