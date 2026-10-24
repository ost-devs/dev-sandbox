# Preservar conversas valiosas do Claude Code

Algumas sessões valem como documento: uma decisão difícil, um diagnóstico, o
raciocínio de uma auditoria. Este guia explica o que o Claude Code guarda,
quando apaga, e como manter as que importam, inclusive referenciadas num PKM
como o Obsidian. Base: documentação oficial
([sessões](https://code.claude.com/docs/en/sessions),
[pasta `.claude`](https://code.claude.com/docs/en/claude-directory),
[hooks](https://code.claude.com/docs/en/hooks)), lida em outubro/2026.

## O que existe e quando some

- Cada conversa é um arquivo **`~/.claude/projects/<projeto>/<id-da-sessão>.jsonl`**:
  todas as mensagens, chamadas de ferramenta e resultados, em texto puro.
  Subagentes ficam em `<id-da-sessão>/subagents/`.
- A **faxina automática apaga** esses arquivos quando ficam mais velhos que
  `cleanupPeriodDays`: **30 dias** por padrão, mínimo 1 (`0` é inválido).
  Vão junto os checkpoints (`/rewind`), saídas grandes de ferramentas e o
  scratchpad da sessão.
- A **memória automática não é apagada** pela faxina.
- O formato do `.jsonl` é **interno** e muda entre versões. Serve para o
  Claude retomar a conversa, não para ler ou processar daqui a anos.
- É tudo **texto puro, sem criptografia**: se o agente leu um `.env` ou um
  comando mostrou um token, isso está na transcrição.

No dev-sandbox vale o mesmo: o `~/.claude` do container é o seu `~/.claude`
do host.

## Três camadas, do mais simples ao mais robusto

### 1. Guardar por mais tempo

Em `~/.claude/settings.json`:

```json
{ "cleanupPeriodDays": 365 }
```

Resolve o "apaga em 30 dias" para tudo. Custos: disco (cada conversa vai de
KB a alguns MB) e mais tempo com eventuais segredos em texto puro no disco.

### 2. Marcar as valiosas e levá-las para o PKM

No fim de uma sessão que vale guardar:

1. **Dê um nome:** `/rename auditoria-view-decisoes`.
2. **Exporte uma cópia legível:** `/export auditoria-view-decisoes.txt` grava
   a conversa como texto, com as saídas das ferramentas. Esse é o arquivo que
   envelhece bem: não depende da versão do Claude Code.
3. **Registre no Obsidian**, numa nota, o que é preciso para voltar:

   ```markdown
   - Sessão: auditoria-view-decisoes
   - ID: 8d26a6eb-caff-4855-a39a-e51ddc077239
   - Projeto: /ferrum (aberto com dev-docker-ferrum)
   - Retomar: claude --resume 8d26a6eb-caff-4855-a39a-e51ddc077239
   - Cópia legível: [[auditoria-view-decisoes.txt]]
   ```

   `claude --resume <id>` funciona **de qualquer pasta**: o Claude procura o
   ID em todos os projetos da máquina. O ID é o nome do arquivo `.jsonl` da
   sessão (`ls -t ~/.claude/projects/<projeto>/ | head -3` logo depois de
   sair). Pelo nome também funciona, de dentro do mesmo repositório:
   `claude --resume auditoria-view-decisoes`.

Antes de colocar o `/export` num cofre sincronizado (Obsidian Sync, git,
nuvem), passe os olhos por tokens e chaves: o export contém as saídas das
ferramentas.

### 3. Arquivo automático, fora do alcance da faxina

Para nunca depender de lembrar: um hook `SessionEnd` que copia cada
transcrição para `~/.claude/arquivo-conversas/`, uma pasta que a faxina não
conhece. Pela lista da documentação, a faxina só apaga os caminhos que ela
nomeia; confira depois do primeiro ciclo de 30 dias que a pasta continua
intacta.

```bash
mkdir -p ~/.claude/hooks
cp ~/dev-sandbox/extras/claude-hooks/arquivar-conversa.py ~/.claude/hooks/
```

E em `~/.claude/settings.json` (vale dentro e fora do container):

```json
{
  "hooks": {
    "SessionEnd": [
      { "hooks": [ { "type": "command",
                     "command": "python3 \"$HOME/.claude/hooks/arquivar-conversa.py\"",
                     "timeout": 15 } ] }
    ]
  }
}
```

- O hook roda quando a sessão termina (também no `/clear` e ao trocar de
  conversa) e substitui a cópia anterior da mesma sessão pela mais nova. Uma
  sessão retomada depois tem a cópia atualizada no próximo fim.
- O `timeout` aumenta o tempo que o Claude espera hooks de saída (o padrão é
  1,5 s, curto para transcrições grandes).
- Uma conversa arquivada pode ser retomada pelo caminho do arquivo:
  `claude --resume ~/.claude/arquivo-conversas/-ferrum/<id>.jsonl`. Isso
  depende de a versão do Claude Code ainda entender o formato antigo; para o
  longo prazo, a camada 2 (`/export`) é a garantia.
- Testado só fora do Claude: o script copia, atualiza e, com entrada inválida,
  avisa no stderr sem impedir a saída. Falta ver o hook rodando numa sessão
  real; confira com `ls ~/.claude/arquivo-conversas/` depois de um `/exit`.

Isso arquiva **tudo**. Se o disco crescer demais, apague as pastas de
projetos que não interessam; as valiosas continuam marcadas no PKM.

## Backup como fonte da verdade

A ordem que não perde nada e não vaza nada:

| O quê | Fonte da verdade | Backup |
|---|---|---|
| Conversas valiosas, para ler | o `/export` no seu PKM | o backup do PKM |
| Conversas para retomar | `~/.claude/arquivo-conversas/` | backup **criptografado** ou só local (disco externo, `restic`, `borg`) |
| Instruções, skills, memórias | `~/.claude` (sem transcrições) | o repositório git privado do [guia de backup](../guias/backup-e-git.md), que de propósito deixa os `.jsonl` de fora |

Transcrições em git hospedado, mesmo privado, não: qualquer segredo que
passou pela conversa vai junto, e o histórico do git guarda para sempre o que
um dia foi commitado.

## Resumo

- Sessão importante: `/rename`, `/export`, nota no PKM com o ID.
- Quer guardar tudo: `cleanupPeriodDays` maior ou o hook de arquivo.
- Retomar: `claude --resume <id>` de qualquer pasta, ou pelo caminho do `.jsonl` arquivado.
- Ler daqui a anos: o `/export`, não o `.jsonl`.
