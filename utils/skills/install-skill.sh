#!/bin/bash
set -euo pipefail

# Uso: install-skill.sh NOME [pasta-de-skills]
#   Instala a skill pronta de utils/skills/NOME em pasta-de-skills/NOME
#   (padrão: ~/.claude/skills, vale em todos os projetos; .claude/skills
#   dentro de um repositório vale só nele). Rodar de novo atualiza.
#
# Vai só o que o Claude usa. Fica na bancada (utils/skills/NOME):
# testes, evals, benchmarks e o README para humanos.
# Se a skill tem package.json, instala as dependências dela (npm ci).

SKILLS="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
NOME="${1:-}"
DIR="${2:-$HOME/.claude/skills}"
FICA_NA_BANCADA=(tests evals benchmarks README.md node_modules __pycache__ .pytest_cache)

if [ -z "$NOME" ] || [ ! -f "$SKILLS/$NOME/SKILL.md" ]; then
  echo "Uso: $0 NOME [pasta-de-skills]" >&2
  echo "Skills: $(cd "$SKILLS" && ls -d */ | tr -d / | tr '\n' ' ')" >&2
  exit 1
fi
mkdir -p "$DIR"
DIR="$(cd "$DIR" && pwd)"
SRC="$SKILLS/$NOME"
DEST="$DIR/$NOME"
MARCA=".instalada-por-install-skill"

if [ "$(realpath -m "$DEST")" = "$(realpath "$SRC")" ] || [ -L "$DEST" ]; then
  echo "$DEST é um link (ou a própria bancada); nada foi alterado." >&2; exit 1
fi
if [ -e "$DEST" ] && [ ! -f "$DEST/$MARCA" ]; then
  echo "$DEST já existe e não foi instalada por este script (cópia à mão ou sua)."
  read -r -p "Substituir pela versão de $SRC? Digite 's' para substituir: " resposta || resposta=""
  [ "$resposta" = "s" ] || [ "$resposta" = "S" ] || { echo "Cancelado. Nada foi alterado."; exit 1; }
fi

# Monta ao lado e só troca no fim: se algo falhar, a instalação antiga fica.
NOVA="$(mktemp -d "$DIR/.$NOME.XXXXXX")"
trap 'rm -rf "$NOVA"' EXIT
excluir=(); for x in "${FICA_NA_BANCADA[@]}"; do excluir+=(--exclude="$x"); done
tar -C "$SRC" "${excluir[@]}" -cf - . | tar -C "$NOVA" -xf -

if [ -f "$NOVA/package.json" ]; then
  if command -v npm >/dev/null; then
    echo "Instalando as dependências da skill (npm ci)..."
    npm ci --prefix "$NOVA" --ignore-scripts --no-audit --no-fund --update-notifier=false --loglevel=error
    # Instalada num repositório (.claude/skills), o node_modules não vai pro git.
    echo "node_modules/" > "$NOVA/.gitignore"
  else
    echo "Aviso: sem npm (Node.js), a parte da skill que usa $(sed -n 's/.*"\([a-z@][^"]*\)": *"[0-9].*/\1/p' "$NOVA/package.json" | tr '\n' ' ')não vai funcionar." >&2
    echo "       Instale o Node.js e rode este comando de novo." >&2
  fi
fi

echo "utils/skills/$NOME do dev-sandbox" > "$NOVA/$MARCA"
chmod 755 "$NOVA"
rm -rf "$DEST"
mv "$NOVA" "$DEST"
trap - EXIT
echo "Pronto: $DEST"

case "$NOME" in
  estudar|montar-consultor)
    [ -d "$DIR/mirrors" ] || echo "A $NOME usa a skill mirrors, que não está em $DIR: $0 mirrors${2:+ $2}" ;;
esac
