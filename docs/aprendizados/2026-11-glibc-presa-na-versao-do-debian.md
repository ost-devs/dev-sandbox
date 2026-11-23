# Binário pronto não roda na imagem: a glibc é a do Debian

- **Data:** 2026-11
- **Ambiente:** imagem do dev-sandbox em Debian 12 (bookworm, glibc 2.36); `cargo-mutants` 27.1.0
- **Base:** evidência (o binário falhou dentro do container, 23/11/2026) e
  documentação ([calendário do Debian](https://wiki.debian.org/DebianReleases))

## Sintoma

```text
cargo-mutants: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found
```

O mesmo binário rodava na nuvem do Claude (Ubuntu 24.04).

## Causa

A glibc é a biblioteca base do sistema, e cada versão do Debian fica presa a
uma. O bookworm traz a 2.36 até o fim e nunca vai receber a 2.39: não é um
pacote desatualizado que um `apt upgrade` resolve. Binários prontos são
compilados em sistemas novos e pedem a glibc deles; quanto mais velha a base,
mais ferramentas falham assim. O bookworm também já era *oldstable*: o Debian
13 (trixie, glibc 2.41) é o estável desde agosto de 2025.

O primeiro contorno foi compilar o `cargo-mutants` no build (`cargo install`,
1 minuto a mais). Funcionava, mas escondia o problema de fundo.

## Solução

Trocar a base da imagem para `debian:trixie-slim`. Três pacotes mudaram de
nome no trixie: `dnsutils` → `bind9-dnsutils`, `libatk-bridge2.0-0` →
`libatk-bridge2.0-0t64`, `libasound2` → `libasound2t64`.

**Lição:** quando um binário pede uma glibc mais nova, olhe a idade da base
antes de compilar por fora.

## O que mudou no dev-sandbox

[`Dockerfile`](../../Dockerfile): base trixie, pacotes renomeados e o
`cargo-mutants` volta a ser binário pronto.
