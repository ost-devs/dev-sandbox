# Portas, apps gráficos e várias sessões ao mesmo tempo

## Portas: desligadas por padrão

Na v0.1 o script publicava portas fixas (3000, 5173, 8000, 8080). Isso trouxe
dois problemas:

- **Conflito com serviços do host.** O container não subia porque o
  Syncthing já ocupava a 8080 (`address already in use`). Trocar para
  `8090:8080` resolve o sintoma, mas é remendo.
- **Só um container por vez.** Duas sessões não podem publicar a mesma porta,
  então a segunda sessão falhava, mesmo em outro projeto.

Na v0.2 nenhuma porta é publicada, a não ser que você peça:

```bash
DEV_PORTS="5173" dev-docker                 # 127.0.0.1:5173 → 5173 do container
DEV_PORTS="5173 3000" dev-docker            # várias
DEV_PORTS="8090:8080" dev-docker            # porta 8090 no host → 8080 no container
```

As portas são sempre publicadas em `127.0.0.1`: só o seu computador enxerga,
não a rede Wi-Fi. Porta ocupada? Descubra quem está usando com
`ss -ltnp | grep :8080` (no host) e escolha outra.

**Você não precisa de porta para o agente testar.** Dentro do container,
`curl localhost:3000` e o Chromium headless funcionam sem nada publicado.
A porta serve só para **você** abrir no navegador do host.

### O servidor precisa escutar em `0.0.0.0`

Por padrão, servidores de desenvolvimento escutam só em `localhost` *de dentro*
do container, e a porta publicada não chega neles:

| Ferramenta | Comando |
|---|---|
| Vite | `npm run dev -- --host` |
| Next.js | `next dev -H 0.0.0.0` |
| FastAPI/uvicorn | `uvicorn app:app --host 0.0.0.0` |
| Python simples | `python -m http.server 8000 --bind 0.0.0.0` |

Depois, no navegador do host: `http://localhost:5173`.

## Ver o app rodando

| O que você quer ver | Como |
|---|---|
| Site/front-end | `DEV_PORTS` + servidor em `0.0.0.0`, abrir no navegador do host |
| O agente "ver" a tela | Ele mesmo usa Chromium headless/Playwright e tira screenshots, sem porta nenhuma |
| Janela do Tauri (ou outro app desktop) | O container não tem tela. Veja as opções abaixo |

### App desktop (Tauri): as opções reais

1. **Rodar `tauri dev` no host, depois de revisar o diff.** É o mais prático:
   o agente programa e valida no container (`cargo check`, `cargo test`,
   `npm run build`), e você roda a janela no host. Mas é **código do agente
   rodando fora do sandbox**: `build.rs`, scripts do `package.json` e a config do
   Tauri executam com o seu usuário. Num projeto seu, revisando o que mudou, é
   aceitável. Num repositório de terceiros, não. Ver [segurança](./seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container).
2. **Só o front-end no navegador**, com `DEV_PORTS`. Funciona para o visual;
   botões que chamam o Rust (`invoke`) não respondem fora da janela do Tauri.
3. **Repassar a tela do host para o container (X11/Wayland).** Não recomendado:
   com acesso ao servidor gráfico, um processo consegue capturar o que você
   digita e o que aparece em qualquer janela. Desfaz o isolamento que o projeto
   existe para dar.

## Várias sessões ao mesmo tempo

### Projetos diferentes

Abra um terminal por projeto e rode `dev-docker` (ou `dev-docker-<nome>`) em cada. Cada container ganha
um nome próprio (`dev-<repo-ou-nome>-<número>`), mostrado ao iniciar. Se mais de um
precisar de porta, use portas diferentes.

Montado no caminho real ou com um `--nome` próprio, cada projeto tem memória e
histórico próprios no Claude Code ([por quê](../claude-code/memoria-e-instrucoes.md#3-memória-dentro-do-dev-sandbox)).

### Outro terminal no mesmo container

Para rodar um servidor numa aba e o agente em outra, por exemplo:

```bash
sudo docker exec -it dev-meu-projeto-12345 bash     # o nome aparece ao iniciar
sudo docker ps --filter name=dev-                   # ou liste os que estão rodando
```

O `exec` entra com o mesmo usuário e as mesmas pastas da sessão original.
Quando a sessão original faz `exit`, o container fecha para todo mundo.

### Dois agentes no mesmo projeto

Dois agentes editando a mesma pasta ao mesmo tempo vão pisar um no outro
(um roda os testes no meio da edição do outro, os dois mexem no mesmo
arquivo). Dê a cada um a sua cópia de trabalho com **git worktree**:

```bash
claude --worktree nova-tela        # cria .claude/worktrees/nova-tela num branch próprio
```

- O worktree fica **dentro** do repositório, então já está montado no container.
  Coloque `.claude/worktrees/` no `.gitignore`.
- Evite `git worktree add ../outra-pasta`: um container aberto nessa outra pasta
  não enxerga o `.git` do repositório principal, e o git quebra lá dentro.
- Se o git reclamar de não conseguir gravar a config ao criar o worktree, rode
  essa sessão com `DEV_GIT_RW=1` (ver [segurança](./seguranca.md)).

Cada agente pode estar no mesmo container (via `exec`) ou num container
separado: o `~/.claude` compartilhado suporta várias sessões simultâneas.
