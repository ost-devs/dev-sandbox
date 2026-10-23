# Imagem completa ou enxuta? E onde ela ocupa espaço

## A escolha: completa por padrão

A v0.1 começava pequena e ia crescendo conforme faltava algo. Na prática isso
custava caro de um jeito que não aparece:

- O agente **não avisa** quando falta uma ferramenta. Sem `rsync`, ele escreve
  um script Python para copiar arquivos. Sem `sqlite3`, improvisa outro. Funciona,
  mas gasta tokens, tempo e às vezes erra.
- Cada descoberta exige editar o `Dockerfile`, reconstruir e reabrir a sessão.

Para um ambiente de **agentes de IA**, alguns GB a mais de imagem custam menos
do que essa fricção. A v0.2 já vem com: Python + `uv`, Node 22 + pnpm/yarn/TS,
Rust + clippy/rustfmt, C/C++ (`clang`, `cmake`), Chromium headless, as
bibliotecas do Tauri v2, e os utilitários que agentes usam sem pedir (`rsync`,
`sqlite3`, `lsof`, `ip`, `dig`, `nc`, `tmux`, `bc`...). Fica na casa de 6 a 8 GB.

### Linguagens que nem todo mundo usa

Go e Java ficam desligados e ligam no build, sem editar o arquivo:

```bash
sudo docker build --build-arg WITH_GO=1 --build-arg WITH_JAVA=1 -t dev-sandbox .
```

Para outra linguagem (PHP, Ruby, .NET...), siga o mesmo padrão: um `ARG WITH_X=0`
e um `RUN if [ "$WITH_X" = "1" ]; then ...; fi`. Se for útil para mais gente,
mande um PR.

### Quando faz sentido enxugar

- Disco realmente apertado (ver abaixo antes: o problema pode ser outro).
- Você não usa Tauri nem testes de navegador: o bloco do Chromium/Tauri é o maior.
- Vai rodar em CI ou num servidor, onde tempo de download importa.

### Como o agente ajuda a completar a imagem

O [`sandbox/AGENTS.md`](../../sandbox/AGENTS.md) pede que, quando faltar uma
ferramenta de sistema que teria ajudado, o agente diga isso no fim da resposta e
anote uma linha em `~/.dev-sandbox/feedback.md` (no host:
`~/.cache/dev-sandbox/home/.dev-sandbox/feedback.md`). De tempos em tempos, leia
esse arquivo, decida o que entra no `Dockerfile` e registre em
[`docs/aprendizados/`](../aprendizados/) o que for interessante.

## Onde a imagem ocupa espaço no seu disco

As imagens **não** ficam na sua home. Com o Docker atual (snapshotter do
containerd), ficam em `/var/lib/containerd`, na partição do sistema. Quem
instalou o Linux com `/` pequeno e `/home` separado (ex.: 100 GB + o resto)
sente isso primeiro.

Ver quanto o Docker está usando:

```bash
sudo docker system df          # imagens, containers, cache de build
sudo du -sh /var/lib/containerd /var/lib/docker
```

O que mais cresce costuma ser o **cache de build**, não a imagem. Limpe o
cache antigo sem perder o atual:

```bash
sudo docker builder prune --filter until=96h
sudo docker image prune        # imagens sem nome (<none>) de builds anteriores
```

### Se o Timeshift estiver ligado: exclua o Docker dele

O Timeshift copia a raiz do sistema, **incluindo `/var/lib/containerd`**, a
cada snapshot. Cada rebuild da imagem vira GB a mais nos snapshots. Num caso
real, 29 GB de 49 GB de snapshots eram cópias do Docker
([o aprendizado completo](../aprendizados/2026-10-disco-cheio-timeshift-docker.md)).
Em Configurações → Filtros, adicione:

```text
/var/lib/containerd/**
/var/lib/docker/**
```

Digite sem espaço no começo: com espaço, o filtro não pega.

### Mover os dados do Docker para a partição da home (opcional)

Se a raiz é pequena e a home tem espaço, dá para mudar onde o Docker guarda
tudo. É mexer no sistema: faça com calma e com backup.

```bash
sudo systemctl stop docker docker.socket containerd
sudo mkdir -p /home/docker-data
sudo rsync -aHAX /var/lib/containerd/ /home/docker-data/containerd/
sudo rsync -aHAX /var/lib/docker/ /home/docker-data/docker/
```

Depois:

- em `/etc/containerd/config.toml`, a linha `root = "/home/docker-data/containerd"`
  (se o arquivo não existir: `containerd config default | sudo tee /etc/containerd/config.toml`);
- em `/etc/docker/daemon.json`: `{ "data-root": "/home/docker-data/docker" }`.

```bash
sudo systemctl start containerd docker
sudo docker images             # a imagem continua lá?
```

Só apague as pastas antigas em `/var/lib` depois de testar uma sessão
`dev-docker` completa.
