#!/usr/bin/env python3
"""Share Claude Code auto-memory files between projects.

One copy per shared memory lives in <claude>/memorias-compartilhadas/<group>/.
Each member project's memory/ folder gets a relative symlink to it and a line
in a generated block of its MEMORY.md. Claude's Write and Edit refuse to write
through a symlink and point at the target, so every edit lands on the single
copy and all projects see it.

Groups are in <claude>/memorias-compartilhadas/grupos.json:
    {"grupos": {"todos": ["*"], "dev": ["-dev-sandbox", "/home/me/Dev/*"]}}
An entry is a project folder name under <claude>/projects/ or a project path,
both with optional * globs.
"""

import argparse
import fcntl
import fnmatch
import json
import os
import re
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path

STORE_NAME = "memorias-compartilhadas"
BLOCK_START = "<!-- compartilhar-memorias:inicio (gerado; edite as memórias, não estas linhas) -->"
BLOCK_END = "<!-- compartilhar-memorias:fim -->"
BLOCK_RE = re.compile(
    r"\n*<!-- compartilhar-memorias:inicio[^\n]*-->\n.*?<!-- compartilhar-memorias:fim -->\n?",
    re.S,
)


def claude_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


class Env:
    def __init__(self, root):
        self.root = Path(root)
        self.projects = self.root / "projects"
        self.store = self.root / STORE_NAME
        self.config = self.store / "grupos.json"

    def groups(self):
        if not self.config.exists():
            return {}
        data = json.loads(self.config.read_text(encoding="utf-8"))
        return {g: list(v) for g, v in data.get("grupos", {}).items()}

    def groups_of(self, slug):
        return sorted(g for g, entries in self.groups().items()
                      if any(fnmatch.fnmatchcase(slug, pattern(e)) for e in entries))

    def members(self, group):
        """Project folders that already have a memory/ folder (others join at SessionStart)."""
        if not self.projects.is_dir():
            return []
        return sorted(p.name for p in self.projects.iterdir()
                      if (p / "memory").is_dir() and group in self.groups_of(p.name))

    def desired(self, slug):
        """{file name: group} of the shared memories this project should have."""
        out = {}
        for g in self.groups_of(slug):
            folder = self.store / g
            if folder.is_dir():
                for f in sorted(folder.glob("*.md")):
                    out.setdefault(f.name, g)
        return out

    @contextmanager
    def lock(self):
        self.store.mkdir(parents=True, exist_ok=True)
        with open(self.store / ".lock", "w") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            yield


def pattern(entry):
    """A path like /home/me/Dev/* becomes the folder-name glob -home-me-Dev-*."""
    if "/" in entry:
        return re.sub(r"[^A-Za-z0-9*?]", "-", entry)
    return entry


def front(path):
    """name and description from a memory's frontmatter, without a YAML parser."""
    name, desc = path.stem, ""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        head = text.split("\n---", 1)[0]
        for line in head.splitlines():
            m = re.match(r"(name|description):\s*(.*)", line)
            if m:
                value = m.group(2).strip().strip("\"'")
                if m.group(1) == "name":
                    name = value or name
                else:
                    desc = value
    return name, desc


def index_line(env, fname, group):
    name, desc = front(env.store / group / fname)
    return f"- [{name}]({fname}) — {desc} _(grupo {group})_".replace(" —  _", " — _")


def write_atomic(path, text):
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def link_target(env, mem, group, fname):
    return os.path.relpath(env.store / group / fname, mem)


def points_into_store(env, link):
    target = os.path.normpath(os.path.join(link.parent, os.readlink(link)))
    return Path(target).parent.parent == Path(os.path.normpath(env.store))


def reconcile(env, slug, create=False, dry=False):
    """Make one project match the store. Returns (added lines, removed files, conflicts)."""
    mem = env.projects / slug / "memory"
    want = env.desired(slug)
    if not mem.is_dir():
        if not (create and want) or dry:
            return [], [], []
        mem.mkdir(parents=True)
    added, removed, conflicts, ok = [], [], [], {}

    for fname, group in want.items():
        p = mem / fname
        target = link_target(env, mem, group, fname)
        if p.is_symlink():
            if os.readlink(p) == target:
                ok[fname] = group
                continue
            if not points_into_store(env, p):
                conflicts.append(f"{slug}/{fname}: link para fora da loja ({os.readlink(p)})")
                continue
            if not dry:
                p.unlink()
        elif p.exists():
            if p.read_bytes() != (env.store / group / fname).read_bytes():
                conflicts.append(f"{slug}/{fname}: arquivo local diferente da memória do grupo {group}")
                continue
            if not dry:
                p.unlink()  # same content: a tool rewrote the link as a plain file
        if not dry:
            p.symlink_to(target)
        ok[fname] = group
        added.append(fname)

    for p in sorted(mem.glob("*.md")):
        if p.is_symlink() and p.name not in want and points_into_store(env, p):
            removed.append(p.name)
            if not dry:
                p.unlink()

    lines = [index_line(env, f, g) for f, g in sorted(ok.items())]
    if not dry:
        update_index(mem / "MEMORY.md", lines, ok)
    return [index_line(env, f, want[f]) for f in added], removed, conflicts


def update_index(index, lines, shared):
    text = index.read_text(encoding="utf-8") if index.exists() else ""
    body = BLOCK_RE.sub("\n", text)
    # A shared memory is listed only in the block: drop Claude's own line for it.
    kept = [l for l in body.splitlines()
            if not any(re.match(rf"\s*-\s*\[.*\]\({re.escape(f)}\)", l) for f in shared)]
    body = "\n".join(kept).rstrip("\n")
    if lines:
        block = "\n".join([BLOCK_START, *lines, BLOCK_END])
        body = f"{body}\n\n{block}" if body else block
    new = body + "\n" if body else ""
    if new != text:
        write_atomic(index, new)


def reconcile_group(env, group):
    report = []
    for slug in env.members(group):
        report.append((slug, *reconcile(env, slug)))
    return report


def memory_file(arg):
    p = Path(arg).absolute()
    if p.parent.name != "memory" or p.parent.parent.parent.name != "projects":
        sys.exit(f"erro: {arg} não é um arquivo em <claude>/projects/<projeto>/memory/")
    return p, p.parent.parent.name


# --- commands ---------------------------------------------------------------

def cmd_share(env, args):
    path, slug = memory_file(args.arquivo)
    if path.is_symlink():
        sys.exit(f"erro: {path.name} já é compartilhada ({os.readlink(path)})")
    if not path.is_file() or path.name == "MEMORY.md":
        sys.exit(f"erro: {path} não é uma memória")
    groups = env.groups()
    if args.grupo not in groups:
        sys.exit(f"erro: grupo {args.grupo!r} não existe em {env.config}")
    if args.grupo not in env.groups_of(slug):
        sys.exit(f"erro: o projeto {slug} não está no grupo {args.grupo}; inclua-o em {env.config}")
    with env.lock():
        # The same name in another group would give some project two memories for one link.
        for g in groups:
            other = env.store / g / path.name
            if other.exists() and (g == args.grupo or set(env.members(g)) & set(env.members(args.grupo))):
                sys.exit(f"erro: já existe {g}/{path.name}; renomeie a memória antes")
        dest = env.store / args.grupo
        dest.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), dest / path.name)
        report = reconcile_group(env, args.grupo)
    print(f"{path.name} → grupo {args.grupo}")
    print_report(report)


def cmd_unshare(env, args):
    group, _, fname = args.memoria.partition("/")
    src = env.store / group / fname
    if not fname or not src.is_file():
        sys.exit(f"erro: {src} não existe (use <grupo>/<arquivo>.md)")
    with env.lock():
        keep = None
        if args.manter:
            keep = env.projects / args.manter / "memory"
            if not keep.is_dir():
                sys.exit(f"erro: {keep} não existe")
            if (keep / fname).is_symlink():
                (keep / fname).unlink()
            elif (keep / fname).exists():
                sys.exit(f"erro: {keep / fname} já existe e não é o link")
            line = index_line(env, fname, group).rsplit(" _(grupo", 1)[0]
            shutil.move(str(src), keep / fname)
        else:
            src.unlink()
        report = reconcile_group(env, group)
        if keep:
            index = keep / "MEMORY.md"
            text = index.read_text(encoding="utf-8") if index.exists() else ""
            m = BLOCK_RE.search(text)
            at = m.start() if m else len(text.rstrip("\n"))
            head, rest = text[:at].rstrip("\n"), text[at:].lstrip("\n")
            write_atomic(index, (f"{head}\n" if head else "") + f"{line}\n" + (f"\n{rest}" if rest else ""))
    print(f"{group}/{fname} deixou de ser compartilhada" + (f"; ficou em {args.manter}" if keep else ""))
    print_report(report)


def cmd_sync(env, args):
    slugs = [args.projeto] if args.projeto else sorted(
        p.name for p in env.projects.iterdir() if (p / "memory").is_dir()) if env.projects.is_dir() else []
    with env.lock():
        report = [(s, *reconcile(env, s, create=bool(args.projeto))) for s in slugs]
    print_report(report)


def cmd_status(env, args):
    groups = env.groups()
    if not groups:
        print(f"nenhum grupo: crie {env.config}")
    for g, entries in groups.items():
        files = sorted(f.name for f in (env.store / g).glob("*.md")) if (env.store / g).is_dir() else []
        print(f"\n[{g}] {', '.join(entries)}")
        print(f"  projetos: {', '.join(env.members(g)) or '(nenhum com memória ainda)'}")
        print(f"  memórias: {', '.join(files) or '(nenhuma)'}")
    pending = []
    if env.projects.is_dir():
        for p in sorted(env.projects.iterdir()):
            if (p / "memory").is_dir():
                added, removed, conflicts = reconcile(env, p.name, dry=True)
                pending += [f"{p.name}: falta {a.split('](')[1].split(')')[0]}" for a in added]
                pending += [f"{p.name}: sobra {r}" for r in removed] + conflicts
    print("\npendências (rode sincronizar):" if pending else "\nsem pendências")
    for line in pending:
        print(f"  {line}")
    settings = env.root / "settings.json"
    if "compartilhar.py" not in (settings.read_text(encoding="utf-8") if settings.exists() else ""):
        print(f"\naviso: os hooks não estão em {settings}; nada sincroniza sozinho")


def print_report(report):
    for slug, added, removed, conflicts in report:
        for a in added:
            print(f"  {slug}: + {a}")
        for r in removed:
            print(f"  {slug}: - {r}")
        for c in conflicts:
            print(f"  conflito: {c}")


# --- hook -------------------------------------------------------------------

def context(event, text):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


def cmd_hook(env, args):
    data = json.load(sys.stdin)
    event = data.get("hook_event_name")
    if event == "SessionStart":
        transcript = Path(data.get("transcript_path") or "")
        if transcript.parent.parent.name != "projects":
            return
        env = Env(transcript.parent.parent.parent)
        slug = transcript.parent.name
        if not env.groups_of(slug):
            return
        with env.lock():
            added, _, conflicts = reconcile(env, slug, create=True)
        notes = []
        if added:
            notes.append("Shared memories just linked into this project's memory (their index lines may "
                         "not be in the MEMORY.md you loaded):\n" + "\n".join(added))
        if conflicts:
            notes.append("compartilhar-memorias conflicts to resolve with the user (skill compartilhar-memorias):\n"
                         + "\n".join(conflicts))
        if notes:
            context(event, "\n\n".join(notes))
        return

    if event != "PostToolUse":
        return
    path = Path((data.get("tool_input") or {}).get("file_path") or "")
    if path.suffix != ".md":
        return
    if path.parent.parent.name == STORE_NAME:
        # A shared memory was edited: refresh its index line everywhere.
        env = Env(path.parent.parent.parent)
        with env.lock():
            report = reconcile_group(env, path.parent.name)
        conflicts = [c for r in report for c in r[3]]
        if conflicts:
            context(event, "compartilhar-memorias conflicts:\n" + "\n".join(conflicts))
        return
    if path.parent.name != "memory" or path.parent.parent.parent.name != "projects":
        return
    env = Env(path.parent.parent.parent.parent)
    slug = path.parent.parent.name
    groups = env.groups_of(slug)
    if not groups:
        return
    if path.name == "MEMORY.md":
        with env.lock():
            reconcile(env, slug)  # puts the block back if a rewrite dropped it
        return
    if data.get("tool_name") == "Write" and (data.get("tool_response") or {}).get("type") == "create":
        context(event, f"New memory `{path.name}`. This project is in the shared-memory groups "
                       f"{', '.join(groups)}. Once the memory and its index line are written, apply the "
                       f"compartilhar-memorias skill: keep it local (do nothing) or share it with a group.")


def main():
    ap = argparse.ArgumentParser(description="Compartilha memórias do Claude Code entre projetos.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("compartilhar", help="move uma memória para um grupo")
    s.add_argument("arquivo", help="caminho da memória em <claude>/projects/<projeto>/memory/")
    s.add_argument("grupo")
    s = sub.add_parser("descompartilhar", help="tira uma memória do grupo")
    s.add_argument("memoria", help="<grupo>/<arquivo>.md")
    s.add_argument("--manter", metavar="PROJETO", help="pasta do projeto que fica com uma cópia local")
    s = sub.add_parser("sincronizar", help="corrige links e índices")
    s.add_argument("--projeto", metavar="PASTA", help="só esta pasta de projeto (cria memory/ se preciso)")
    sub.add_parser("status", help="grupos, memórias e pendências")
    sub.add_parser("hook", help="chamado pelos hooks do Claude Code (JSON na entrada)")
    # Project folders start with "-" (-dev-sandbox); argparse would take them for options.
    argv, i = [], 0
    raw = sys.argv[1:]
    while i < len(raw):
        if raw[i] in ("--manter", "--projeto") and i + 1 < len(raw):
            argv.append(f"{raw[i]}={raw[i + 1]}")
            i += 2
        else:
            argv.append(raw[i])
            i += 1
    args = ap.parse_args(argv)
    env = Env(claude_dir())
    {"compartilhar": cmd_share, "descompartilhar": cmd_unshare, "sincronizar": cmd_sync,
     "status": cmd_status, "hook": cmd_hook}[args.cmd](env, args)


if __name__ == "__main__":
    main()
