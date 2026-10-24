#!/usr/bin/env python3
"""Hook SessionEnd do Claude Code: copia a transcrição da sessão para um arquivo fora da faxina.

Instalação e motivo: docs/claude-code/preservar-conversas.md. Lê o JSON do hook no stdin
(session_id, transcript_path, cwd) e copia <sessão>.jsonl e a pasta <sessão>/subagents/ para
~/.claude/arquivo-conversas/<pasta-do-projeto>/. Cada execução substitui a cópia anterior da
mesma sessão pela versão mais nova. Nunca falha a saída do Claude: erros vão para o stderr.
"""
import json, pathlib, shutil, sys

try:
    data = json.load(sys.stdin)
    src = pathlib.Path(data['transcript_path']).expanduser()
    if not src.is_file():
        sys.exit(0)
    dest_dir = pathlib.Path.home() / '.claude' / 'arquivo-conversas' / src.parent.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_dir / src.name)
    sub = src.with_suffix('') / 'subagents'
    if sub.is_dir():
        target = dest_dir / src.stem / 'subagents'
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(sub, target)
except Exception as e:  # o hook não pode impedir a saída da sessão
    print(f'arquivar-conversa: {e}', file=sys.stderr)
