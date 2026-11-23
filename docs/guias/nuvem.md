# Usar na nuvem do Claude (claude.ai/code)

O Claude Code também roda numa máquina virtual (VM) da Anthropic: você abre a
sessão pelo navegador, pelo app do celular ou pelo app do PC, sem Docker e sem
deixar o computador ligado. Este guia monta lá um ambiente equivalente à imagem
do dev-sandbox.

O projeto precisa estar no GitHub: cada sessão começa com um clone novo dele.

## O que muda em relação ao Docker local

| | Docker local (`dev-docker`) | Nuvem (claude.ai/code) |
|---|---|---|
| Onde roda | no seu PC | numa VM da Anthropic |
| Abre de onde | terminal do PC | navegador, app do celular ou app do PC |
| Agentes | Claude Code, Codex, agy | só Claude Code |
| Arquivos | a pasta do projeto no seu PC | um clone do repositório do GitHub |
| O que sobrevive | projeto, logins, memória do Claude | só o que for commitado e enviado (push) para uma branch |
| Pacote do sistema (`apt-get`) | não dá (sem `sudo`) | dá, mas some no fim da sessão; para ficar, vai no setup script |
| Internet | livre | só os domínios liberados no ambiente |
| Docker dentro da sessão | não | sim, depois de `service docker start` |
| Instruções do ambiente para o Claude | [`sandbox/AGENTS.md`](../../sandbox/AGENTS.md), na imagem | o setup script escreve `~/.claude/CLAUDE.md` |

A memória automática do Claude também não passa de uma sessão para outra
(dedução: toda sessão começa do mesmo disco salvo). O que ele precisa saber do
projeto vai em arquivos do repositório, como o `CLAUDE.md`
([por quê](../claude-code/consultor-do-projeto.md)).

## Configurar o ambiente (uma vez)

Um **ambiente** (*environment*) guarda três coisas: o setup script, a rede e
as variáveis. Para criar ou editar um:

1. Em [claude.ai/code](https://claude.ai/code), na tela de nova sessão, toque
   no primeiro botão da linha embaixo da caixa de mensagem (o seletor de
   ambiente).
2. **New environment** cria um ambiente. Para editar um que já existe, toque
   no ícone de engrenagem ao lado do nome dele, em **Cloud**. Com uma sessão
   aberta, toque na seta ao lado do título dela e depois em **Edit cloud environment**.
3. Preencha os três itens abaixo e salve com **Add environment** ou **Save changes**.

**No celular:** funciona igual no navegador do celular, em claude.ai/code.
Se o app não mostrar a edição do ambiente, use o navegador.

### 1. Setup script

É um script que roda como `root` antes de cada sessão nova. O resultado fica
guardado (cache), então só a primeira sessão espera, cerca de 1 minuto.

**Opção curta (recomendada, fácil de digitar no celular).** Ela baixa o
[`nuvem/setup.sh`](../../nuvem/setup.sh) deste repositório e o roda:

```bash
#!/bin/bash
# dev-sandbox (docs/guias/nuvem.md). Versão: 2026-11-23
curl -fsSL https://raw.githubusercontent.com/ost-devs/dev-sandbox/main/nuvem/setup.sh | bash
```

O cache só é refeito quando você edita este campo, muda a rede, ou depois de
cerca de 7 dias. Quando o `nuvem/setup.sh` mudar no repositório e você quiser a
versão nova já, troque a data na linha `Versão:` e salve.

Esse script roda como `root` na sua VM. Se você usa um fork, troque
`ost-devs/dev-sandbox` pelo seu repositório.

**Opção completa.** Cole o conteúdo inteiro do [`nuvem/setup.sh`](../../nuvem/setup.sh)
no campo. No PC, você também pode baixar o arquivo e usar **Choose file**.
Use esta opção se não quiser depender do GitHub na hora da sessão, ou se quiser
fixar uma versão. Para atualizar, você cola de novo.

O que o script faz:

- instala os pacotes do [`Dockerfile`](../../Dockerfile) que faltam na imagem
  da nuvem (`fd`, `tree`, `rsync`, `sqlite3`, `dig`, bibliotecas do Tauri...);
- instala `typescript` e `tsx` globais;
- instala as ferramentas de teste do Rust da imagem: `llvm-tools-preview`,
  `cargo llvm-cov` (cobertura) e `cargo mutants` (testes de mutação);
- cria `/usr/bin/chromium`, o mesmo caminho do Docker, apontando para o Chrome
  que já vem na nuvem;
- escreve `~/.claude/CLAUDE.md`, que faz para o Claude o papel do
  `sandbox/AGENTS.md`: onde ele está, o que sobrevive, como iniciar Docker e
  bancos e o que fazer quando faltar uma ferramenta.

Ele **não** baixa navegador: a imagem da nuvem já traz o Playwright com o
Chrome dele ([por quê](../aprendizados/2026-11-nuvem-ja-traz-o-navegador.md)).

### 2. Rede (*Network access*)

Escolha **Limited** e deixe **Allow package managers** marcado. Para o
dev-sandbox não precisa liberar nenhum domínio: o GitHub e os registros de
pacotes (npm, PyPI, crates.io...) já estão na lista padrão.

Em **Allowed domains**, coloque só o que o **seu projeto** chama (uma API, um
site que os testes acessam), um por linha. Em apps antigos, essa opção se chama
**Custom**, com uma caixa para incluir a lista padrão: marque essa caixa.

### 3. Variáveis de ambiente (opcional)

Sem variáveis, os commits saem com autor `Claude`. Para saírem no seu nome:

```text
GIT_AUTHOR_NAME=Seu Nome
GIT_AUTHOR_EMAIL=voce@exemplo.com
```

- **Só essas duas.** Não defina `GIT_COMMITTER_NAME`/`GIT_COMMITTER_EMAIL`:
  quem assina o commit é a nuvem, com a chave do Claude, fora da sua VM. Com
  o *committer* trocado para você, o GitHub não confere a assinatura e o commit
  aparece sem o selo **Verified**. Assim fica: autor = você, *committer* =
  Claude, assinatura válida (testado numa sessão da nuvem, 11/2026).
- Uma por linha, **sem espaço antes do nome**. Colar texto recuado (comum no
  celular) gera `   NOME=...`, e a variável é ignorada sem nenhum aviso.
- Não precisa de variável do Playwright ou do Puppeteer: a imagem já define as
  dela, e as suas não ajudam.
- Nada de senha ou chave de API aqui: quem usa o ambiente lê as variáveis.
  Chaves vão em *network secrets* ([documentação](https://code.claude.com/docs/en/cloud-environments#add-network-secrets)).
- O setup script não enxerga essas variáveis: ele roda antes delas existirem.

### 4. Conferir

Abra uma sessão nova nesse ambiente e peça:

```text
Confira o ambiente: mostre o fim de /var/log/dev-sandbox-nuvem.log e rode `which fd tree tsc chromium`.
```

E digite `/context`: `/root/.claude/CLAUDE.md` deve aparecer em **Memory files**.

## Ferramentas a mais para o seu projeto

Se o seu projeto precisa de algo que o dev-sandbox não traz, acrescente as
linhas **embaixo** do `curl`, no campo do setup script. Termine cada uma em
`|| true` (se o script falhar, a sessão não abre) e prefira binários prontos a
compilar: o script precisa terminar em menos de ~5 minutos para entrar no cache.

Exemplo: Rust nightly, para recursos instáveis como `cargo +nightly llvm-cov
--doctests` (o `cargo llvm-cov` e o `cargo mutants` já vêm no `nuvem/setup.sh`):

```bash
rustup toolchain install nightly --profile minimal --component llvm-tools-preview || echo "AVISO: nightly não foi instalado"
```

As mesmas linhas servem no seu PC: ponha em [`local/extra.sh`](../../local/README.md)
e o build da imagem roda elas. Um texto só para os dois lugares.

Quando o Claude terminar uma resposta com `Missing in sandbox: <ferramenta>`,
é o sinal: ele precisou de algo que não estava lá. Se for coisa do seu
projeto, ponha aqui. Se for útil para qualquer projeto, proponha no
[`nuvem/setup.sh`](../../nuvem/setup.sh) (e no `Dockerfile`).

## Problemas comuns

| Sintoma | Causa e solução |
|---|---|
| A sessão não abre e fala do setup script | Algum comando saiu com erro. Ponha `\|\| true` no fim dele |
| Instalou, mas a sessão seguinte não tem | O script passou de ~5 min e não entrou no cache. Troque `cargo install` por binários prontos |
| Mudei o `nuvem/setup.sh` e nada mudou | O cache é da versão antiga. Troque a data da linha `Versão:` |
| `request blocked` / host bloqueado | O domínio não está liberado. Acrescente em **Allowed domains** |
| Um teste do Playwright pede `npx playwright install` | O projeto fixa outra versão do Playwright. Use `executablePath: '/usr/bin/chromium'` ([detalhes](../aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md)) |

---
Fonte: [Cloud environments](https://code.claude.com/docs/en/cloud-environments)
(setup script, cache, rede, variáveis, ferramentas instaladas).
Conferido em 11/2026 (Claude Code 2.1.325), com testes numa sessão da nuvem.
