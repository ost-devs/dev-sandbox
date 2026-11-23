# Extras pessoais da imagem

Ferramentas que só **você** usa (um projeto seu, um gosto seu) entram aqui,
sem branch pessoal e sem mexer no `Dockerfile`.

1. Crie `local/extra.sh` nesta pasta (no host). O git ignora tudo aqui menos
   este README, então o arquivo nunca vai para um commit.
2. Escreva nele os comandos de instalação. São **as mesmas linhas** que você
   põe embaixo do `curl` no setup script da nuvem
   ([guia](../docs/guias/nuvem.md#ferramentas-a-mais-para-o-seu-projeto)).
3. Reconstrua a imagem (no host): `sudo docker build -t dev-sandbox .`

O script roda como `root`, no fim do build, antes dos agentes. Se o último
comando dele falhar, o build para: termine com `|| true` o que puder falhar.
Instale em `/usr/local/bin`: o que vai para a sua home não fica na imagem.

O que servir para qualquer projeto não fica aqui: proponha no
[`Dockerfile`](../Dockerfile) e no [`nuvem/setup.sh`](../nuvem/setup.sh).
