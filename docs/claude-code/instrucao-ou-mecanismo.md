# Instrução ou mecanismo: o que vai no CLAUDE.md e o que vai na configuração

Toda linha de `CLAUDE.md`, `AGENTS.md` ou rule é um **pedido** ao modelo. Uma
montagem somente leitura, uma regra `deny` ou um script é uma **trava**. Este
guia ajuda a decidir qual dos dois usar em cada caso, usando como exemplo a
v0.4 do dev-sandbox, que trocou instruções de segurança por travas.

Base oficial: as páginas de [memória](https://code.claude.com/docs/en/memory)
e de [permissões](https://code.claude.com/docs/en/permissions). Conferido em
outubro/2026 (Claude Code 2.1.310). No fim do guia há uma
[tabela](#de-onde-vem-cada-afirmação) que diz o que é documentação, o que é
evidência e o que é só análise.

## A ideia de partida e o que ajustar nela

A ideia que motivou este guia foi:

> *"Rules e CLAUDE.md deveriam cobrir só o que não dá para configurar. Isso
> economiza tokens."*

A direção está certa, mas precisa de três ajustes:

1. **O critério está incompleto.** "Não dá para configurar" é condição
   necessária, mas não suficiente. A linha também precisa mudar o que o agente
   faz, e tratar de algo que ele **não descobriria sozinho**. Muita coisa que
   não dá para configurar também não precisa ser dita.
2. **O ganho principal não é token, é garantia.** Uma trava vale mesmo quando o
   modelo esquece, se confunde ou é enganado por um texto malicioso. A
   economia de tokens existe, mas é pequena (números
   [abaixo](#quanto-de-token-isso-economiza)).
3. **Uma trava também tem limite.** Ela troca "talvez o modelo obedeça" por
   "vale até tal ponto". Escrever onde fica esse ponto faz parte do trabalho.

## O que a documentação diz

A página oficial de memória é direta:

> "O Claude trata [os arquivos CLAUDE.md e a memória] como contexto, não como
> configuração imposta. Para bloquear uma ação, independentemente do que o
> Claude decidir, use um hook PreToolUse."

> "As regras de settings são impostas pelo cliente, independentemente do que
> o Claude decidir fazer. As instruções do CLAUDE.md moldam o comportamento,
> mas não são uma camada de imposição."

A mesma página divide os assuntos assim (resumo):

| Assunto | Onde configurar |
|---|---|
| Bloquear ferramentas, comandos ou caminhos | Settings: `permissions.deny` |
| Isolamento por sandbox | Settings: `sandbox.enabled` |
| Variáveis de ambiente | Settings: `env` |
| Estilo de código, lembretes de conformidade, comportamento | CLAUDE.md |

Então a tese de "trava para o que precisa valer, texto para orientar" é a
própria recomendação oficial. O que este guia acrescenta é como aplicar isso
linha por linha.

### Placa e lombada

A placa "Devagar, escola" depende de o motorista ler, entender e querer
obedecer. A lombada funciona com qualquer motorista, até o distraído. Mas a
lombada só vale no ponto onde foi instalada, e há coisas que nenhuma lombada
diz, como "cuidado: crianças atravessando". Uma placa "não dirija na
contramão" também não ajuda, porque todo motorista já sabe: é só ruído.

Instruções são placas e mecanismos são lombadas. Os dois têm seu lugar.

## O teste da linha

Para cada linha de instrução, existente ou nova:

```text
1. Precisa valer mesmo que o modelo esqueça, se confunda
   ou seja enganado?
     sim → MECANISMO (deny, hook, montagem, script, CI).
           Escreva até onde ele vale.
     não → siga

2. O agente descobre isso sozinho, na hora em que precisa?
   (mensagem de erro clara, --help, arquivo do projeto)
     sim → NADA. Apague a linha.
     não → siga

3. Saber disso muda o que ele faz?
     não → NADA.
     sim → INSTRUÇÃO, curta e concreta. Depois decida onde ela mora ↓

4. Quando ela vale?
     sempre, em todo o projeto      → CLAUDE.md / AGENTS.md
     só numa parte (docs/, Rust...) → rule com `paths`
     só às vezes, e você sabe quando → diga no próprio pedido
     só num ambiente (o container)  → o arquivo que só carrega lá
```

A pergunta 4 parece detalhe, mas evitou um erro neste repositório (ver
[instrução no lugar certo](#instrução-no-lugar-certo)).

## O caso do dev-sandbox

Até a v0.3, o `sandbox/AGENTS.md` tinha seções inteiras de Git e segurança. Na
v0.4, elas foram trocadas por mecanismos:

| Instrução antiga | O que a substituiu | Quem garante | Até onde vale |
|---|---|---|---|
| "`.git/hooks` e `.git/config` são somente leitura" | Montagem `readonly` no [`dev-docker`](../../dev-docker) | O Docker, para **qualquer** processo e **qualquer** agente | Não cobre repositórios criados na sessão nem mais fundos que dois níveis. `DEV_GIT_RW=1` desliga |
| "Nunca leia as credenciais dos agentes" | `deny` em [`sandbox/managed-settings.json`](../../sandbox/managed-settings.json) | O cliente do Claude Code | Só o Claude Code (Codex e agy, não). Segundo a documentação, cobre as ferramentas de arquivo e `cat`/`head`/`sed` no terminal, mas não um script Python ou Node que abra o arquivo sozinho |
| "Liste no fim os arquivos que rodam no host" | Relatório de saída no `dev-docker` | O script, pelo ctime (o agente não disfarça com `touch`) | Só aparece **ao sair**. Não roda se a pasta montada for a raiz ou a home. A lista de padrões é fixa |
| "Identidade git só com `--global`", "sem chaves SSH" | Nada | O próprio agente: o erro é claro, e ele não faria push sem pedir | Análise, não medida |

**O que mudou de verdade:** antes, a proteção dependia de quatro coisas. O
agente tinha que ler o arquivo, lembrar dele, obedecer e não ser convencido do
contrário por um README malicioso. O Codex e o agy só leem o arquivo se você
acrescentar uma linha no host. Uma montagem somente leitura não depende de
nenhuma dessas coisas.

**O que ficou como instrução, e por quê:**

| Linha que ficou | Por que passa no teste |
|---|---|
| `/tmp` fora do `$HOME` se perde ao sair | O agente não tem como saber que é um container descartável |
| `apt-get` falha, não contorne com gambiarras grandes | O erro do `apt-get` ele descobre sozinho. A linha existe pela segunda metade: muda o que ele faz depois do erro |
| Ferramenta faltando: avise e anote | Não dá para virar mecanismo, porque exige julgamento ("teria ajudado?"). E há evidência de que, sem a linha, o agente contorna calado ([aprendizado](../aprendizados/2026-10-agente-contorna-ferramenta-faltando.md)) |
| Playwright: passe `executablePath` | Não dá para configurar: o Playwright não lê variável de ambiente para isso ([aprendizado](../aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md)) |
| Traduzir `/tmp/dev-home/...` para o caminho do host | O agente não sabe como as pastas foram montadas. Linha nova, ainda não testada |

## Uma trava também tem limite

Cada mecanismo da tabela tem um limite diferente:

- **Alcance:** o `deny` só vale para o Claude Code. A montagem vale para todos.
- **Momento:** o relatório só aparece no fim. Se você der `git commit` noutro
  terminal do host com a sessão aberta, um hook versionado alterado já roda
  ([segurança](../guias/seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container)).
- **Cobertura:** o `deny` pega `cat`, mas não `python -c "open(...)"`. O
  relatório só pega os padrões da lista.

Por isso o limite fica escrito **ao lado** do mecanismo, como o guia de
segurança faz. *Análise:* uma trava cujo limite não está escrito dá uma
sensação de segurança que ela não entrega. Isso pode ser pior do que uma
instrução honesta, porque ninguém fica atento ao que ela não cobre.

Um caso real deste repositório: a documentação dizia que o `deny` não cobria
`cat`. A página oficial diz que cobre. O limite estava escrito, mas no lugar
errado. Isso foi corrigido junto com este guia, ainda sem teste no container.

**O erro precisa ser claro.** Quando uma trava bloqueia, o agente recebe um
erro. "Read-only file system" ou uma recusa por regra `deny` dizem o que
aconteceu. *Hipótese:* um erro obscuro vira um enigma, e o agente tende a
contornar, como fez com o `rsync` que faltava. Aquele caso é evidência de que
agentes contornam obstáculos calados, mas não envolvia uma trava.

## Nem instrução fixa nem trava

### Você, no pedido

A versão pessoal do `sandbox/AGENTS.md` não tem a linha de portas. Ela não
passa no teste como "nada": não dá para configurar, o agente não deduz qual
porta do host está publicada, e isso muda o que ele faz (`vite --host`, porta
certa). Mesmo assim saiu, porque o mantenedor **sabe quando** precisa e diz no
pedido. A informação chega só na hora em que importa, sem custo fixo.

Isso funciona para quem conhece o ambiente. Para um iniciante, a linha volta:
por isso a versão completa (`sandbox/AGENTS-completo.md`) a mantém.

### Instrução no lugar certo

A tradução de caminhos (`/tmp/dev-home/.claude/` → `~/.claude/`) quase foi
parar numa rule em `~/.claude/` do host. Só que o `~/.claude` do host é o mesmo
que entra no container, então a regra carregaria também nas sessões **fora**
do Docker. Lá ela estaria errada e custaria tokens em toda sessão. O lugar
certo é o `/etc/claude-code/CLAUDE.md`, que só carrega dentro do container.

Regra prática: **onde o arquivo carrega deve coincidir com onde o fato é
verdade.**

### Rules com `paths`

Uma instrução que só importa quando alguém mexe em `docs/` não precisa
ocupar contexto o resto do tempo. Com `paths`, ela não custa nada até ser
relevante ([como funciona](./memoria-e-instrucoes.md#rules-instruções-que-só-aparecem-quando-importam)).

## Conflitos entre instruções: planejamento ou instrução?

A documentação diz que, se duas instruções se contradizem, **"o Claude pode
escolher uma arbitrariamente"**. Também diz que, entre uma rule pessoal e uma
do projeto, nenhuma prevalece sobre a outra.

Evitar o conflito é trabalho de planejamento e revisão, sim. A documentação
recomenda revisar os arquivos de tempos em tempos e oferece o
`/doctor prompt-audit`, que procura instruções contraditórias ou
desatualizadas e propõe correções. *(Documentado; ainda não testado aqui.)*

Mas, num projeto com vários documentos de autoridade que mudam com o tempo
(decisões, especificações, briefs de fase), conflitos vão aparecer mesmo com
boa revisão. Uma linha como "se dois documentos se contradizem, pare e
mostre os dois trechos; não escolha" não entrega a decisão ao agente: ela
**proíbe** o agente de decidir. E passa no teste: não dá para configurar, ele
não deduz a ordem de autoridade, e muda o que ele faz.

Um cuidado: diga que um documento mais específico **detalhando** um geral não
é conflito. Sem isso, o agente para à toa.

## Sinais de que uma instrução deveria virar trava

- Você já corrigiu a mesma coisa mais de uma vez.
- Desobedecer custa caro ou não tem volta (segurança, dados, produção).
- Um programa consegue verificar com sim ou não (formato, lint, caminho
  proibido, comando proibido).
- Um texto de fora (README, issue, página web) poderia convencer o agente do
  contrário.

E o caminho inverso: quando a regra exige julgamento ("avise se teria
ajudado"), uma trava não serve, e a instrução é a ferramenta certa.

## Travas disponíveis

| Quer garantir | Mecanismo | Onde |
|---|---|---|
| O Claude não abre certos arquivos nem usa certas ferramentas | `permissions.deny` | Settings. Em managed settings, ninguém sobrescreve |
| Bloquear comandos com uma lógica sua | Hook `PreToolUse` | Settings ([hooks](https://code.claude.com/docs/en/hooks-guide)) |
| Restringir arquivos e rede de **qualquer** processo do terminal | Sandbox do Claude Code | Settings. Dentro do Docker, [teste antes](../guias/seguranca.md#sandbox-interno-dos-agentes) |
| Uma variável sempre definida | `env` nos settings, `ENV` no `Dockerfile` | — |
| Algo que o agente não pode tocar | Não montar, ou montar somente leitura | `dev-docker` |
| Formato, testes, lint | CI ou hook | Projeto |

## Quanto de token isso economiza

Medido: o `/context` mostrou **518 tokens** para o `sandbox/AGENTS.md` da v0.4,
num arquivo de 1.280 bytes. A versão anterior às reduções tinha 2.977 bytes.
Na mesma proporção, isso daria uns 1.200 tokens, mas é uma **estimativa**, não
uma medida. A economia fica na casa de 700 tokens por sessão, numa janela de
1 milhão.

É pouco. Ainda assim, essas linhas entram em **toda** sessão de **todo**
projeto, e a documentação diz que arquivos mais longos são seguidos com menos
consistência. Quanto isso pesa, não medimos.

## De onde vem cada afirmação

| Afirmação | Base |
|---|---|
| CLAUDE.md é contexto, não trava; settings são impostos pelo cliente | Documentação ([memória](https://code.claude.com/docs/en/memory), outubro/2026) |
| Instruções contraditórias: o Claude pode escolher uma arbitrariamente | Documentação (memória) |
| `/doctor prompt-audit` acha conflitos | Documentação (memória); não testado |
| `deny` de leitura cobre `cat`/`head`/`sed`, não scripts | Documentação ([permissões](https://code.claude.com/docs/en/permissions)); não testado no container |
| Arquivos mais longos reduzem a obediência | Documentação (memória); a intensidade não foi medida |
| O agente contorna ferramenta faltando sem avisar | Evidência ([aprendizado](../aprendizados/2026-10-agente-contorna-ferramenta-faltando.md)) |
| O Playwright não lê variável para o navegador | Evidência ([aprendizado](../aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md)) |
| 518 tokens no AGENTS.md da v0.4 | Medido (`/context`) |
| ~1.200 tokens na versão antiga | Estimativa por proporção de bytes |
| Relatório de saída, submódulos protegidos, `deny` funcionando | Testados só a seco (ver `CHANGELOG.md`, v0.4); falta o teste no host |
| Trava sem limite escrito pode ser pior que instrução honesta | Análise |
| Erro obscuro leva o agente a contornar | Hipótese |
