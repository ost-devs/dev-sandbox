#!/usr/bin/env python3
"""Share Claude Code auto-memory files between projects.

One copy per shared memory lives in <claude>/shared-memories/<group>/.
Each member project's memory/ folder gets a relative symlink to it and a line
in a generated block of its MEMORY.md. Claude's Write and Edit refuse to write
through a symlink and point at the target, so every edit lands on the single
copy and all projects see it.

Groups are in <claude>/shared-memories/groups.json:
    {"groups": {"all": ["*"], "dev": ["-dev-sandbox", "/home/me/Dev/*"]},
     "lines": {"dev/feedback-x.md": {"title": "Short title", "summary": "short summary"}}}
An entry is a project folder name under <claude>/projects/ or a project path,
both with optional * globs. "lines" keeps the title and summary of Claude's own
MEMORY.md line, taken at share time; without one, name and description are used.
The key is <group>/<file> on purpose: the file's folder already says where the
memory lives, so nothing else records it, and unshare drops the entry because
the line goes back to the project's MEMORY.md, where Claude keeps editing it.
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

STORE_NAME = "shared-memories"
BLOCK_START = "<!-- share-memories:start (generated; edit the memories, not these lines) -->"
BLOCK_END = "<!-- share-memories:end -->"
BLOCK_RE = re.compile(r"\n*<!-- share-memories:start[^\n]*-->\n.*?<!-- share-memories:end -->\n?", re.S)
HOOK_EVENTS = {"PostToolUse": "Write|Edit", "SessionStart": None}


def claude_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


class Env:
    def __init__(self, root):
        self.root = Path(root)
        self.projects = self.root / "projects"
        self.store = self.root / STORE_NAME
        self.config = self.store / "groups.json"

    def data(self):
        if not self.config.exists():
            return {}
        return json.loads(self.config.read_text(encoding="utf-8"))

    def groups(self):
        return {g: list(v) for g, v in self.data().get("groups", {}).items()}

    def lines(self):
        """{"<group>/<file>": {"title": ..., "summary": ...}} for the shared memories' index lines."""
        return dict(self.data().get("lines", {}))

    def save(self, groups=None, lines=None):
        data = self.data()
        if groups is not None:
            data["groups"] = groups
        if lines is not None:
            data["lines"] = dict(sorted(lines.items()))
        if not data.get("lines"):
            data.pop("lines", None)
        self.store.mkdir(parents=True, exist_ok=True)
        write_atomic(self.config, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    def save_groups(self, groups):
        self.save(groups=groups)

    def groups_of(self, slug):
        return sorted(g for g, entries in self.groups().items()
                      if any(fnmatch.fnmatchcase(slug, pattern(e)) for e in entries))

    def with_memory(self):
        if not self.projects.is_dir():
            return []
        return sorted(p.name for p in self.projects.iterdir() if (p / "memory").is_dir())

    def members(self, group):
        """Project folders that already have a memory/ folder (others join at SessionStart)."""
        return [s for s in self.with_memory() if group in self.groups_of(s)]

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
        for line in text.split("\n---", 1)[0].splitlines():
            m = re.match(r"(name|description):\s*(.*)", line)
            if m:
                value = m.group(2).strip().strip("\"'")
                if m.group(1) == "name":
                    name = value or name
                else:
                    desc = value
    return name, desc


def own_line(index, fname):
    """Title and summary of Claude's own MEMORY.md line for a memory, or None."""
    if not index.exists():
        return None
    for line in BLOCK_RE.sub("\n", index.read_text(encoding="utf-8")).splitlines():
        m = re.match(rf"\s*-\s*\[(.*)\]\({re.escape(fname)}\)\s*(?:[—–-]+\s*)?(.*)", line)
        if m:
            return {"title": m.group(1), "summary": m.group(2).strip()}
    return None


def index_line(env, fname, group, tag=True):
    saved = env.lines().get(f"{group}/{fname}")
    if saved:
        title, summary = saved.get("title") or Path(fname).stem, saved.get("summary", "")
    else:
        title, summary = front(env.store / group / fname)
    line = f"- [{title}]({fname}) — {summary}" if summary else f"- [{title}]({fname})"
    # The block's HTML comments are stripped when MEMORY.md loads: this tag is what Claude sees.
    return f"{line} _(shared, group {group})_" if tag else line


def write_atomic(path, text):
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


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
        target = os.path.relpath(env.store / group / fname, mem)
        if p.is_symlink():
            if os.readlink(p) == target:
                ok[fname] = group
                continue
            if not points_into_store(env, p):
                conflicts.append(f"{slug}/{fname}: link points outside the store ({os.readlink(p)})")
                continue
            if not dry:
                p.unlink()
        elif p.exists():
            if p.read_bytes() != (env.store / group / fname).read_bytes():
                conflicts.append(f"{slug}/{fname}: local file differs from group {group}'s memory")
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

    if not dry:
        update_index(mem / "MEMORY.md", [index_line(env, f, g) for f, g in sorted(ok.items())], ok)
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


def add_local_line(index, line):
    """Put a line in Claude's own part of MEMORY.md, above the generated block."""
    text = index.read_text(encoding="utf-8") if index.exists() else ""
    m = BLOCK_RE.search(text)
    at = m.start() if m else len(text)
    head, rest = text[:at].rstrip("\n"), text[at:].lstrip("\n")
    write_atomic(index, (f"{head}\n" if head else "") + f"{line}\n" + (f"\n{rest}" if rest else ""))


def reconcile_all(env, slugs=None):
    return [(s, *reconcile(env, s)) for s in (slugs or env.with_memory())]


def memory_file(arg):
    p = Path(arg).absolute()
    if p.parent.name != "memory" or p.parent.parent.parent.name != "projects":
        sys.exit(f"error: {arg} is not a file in <claude>/projects/<project>/memory/")
    return p, p.parent.parent.name


def shared_ref(env, ref):
    group, _, fname = ref.partition("/")
    src = env.store / group / fname
    if not fname or not src.is_file():
        sys.exit(f"error: no shared memory {ref} (use <group>/<file>.md; see status)")
    return group, fname, src


def taken(env, groups, group, fname, ignore=None):
    """Another group whose members overlap this one already uses the name."""
    for g in groups:
        if g != ignore and (env.store / g / fname).exists() and (
                g == group or set(env.members(g)) & set(env.members(group))):
            return g
    return None


# --- commands ---------------------------------------------------------------

def cmd_share(env, args):
    groups = env.groups()
    if args.group not in groups:
        sys.exit(f"error: no group {args.group!r} in {env.config} (create it: group {args.group} --add ...)")
    files = []
    for arg in args.files:
        path, slug = memory_file(arg)
        if path.is_symlink():
            sys.exit(f"error: {path.name} is already shared ({os.readlink(path)})")
        if not path.is_file() or path.name == "MEMORY.md":
            sys.exit(f"error: {path} is not a memory")
        if args.group not in env.groups_of(slug):
            sys.exit(f"error: project {slug} is not in group {args.group} (add it: group {args.group} --add {slug})")
        files.append(path)
    with env.lock():
        for path in files:
            g = taken(env, groups, args.group, path.name)
            if g:
                sys.exit(f"error: {g}/{path.name} already exists; rename the memory first")
        dest = env.store / args.group
        dest.mkdir(parents=True, exist_ok=True)
        lines = env.lines()
        for path in files:
            own = own_line(path.parent / "MEMORY.md", path.name)
            if own:
                lines[f"{args.group}/{path.name}"] = own
            shutil.move(str(path), dest / path.name)
            print(f"shared   {path.name} -> group {args.group}")
        env.save(lines=lines)
        print_report(reconcile_all(env))


def cmd_unshare(env, args):
    refs = [shared_ref(env, r) for r in args.memories]
    keep = None
    if args.keep:
        keep = env.projects / args.keep / "memory"
        if not keep.is_dir():
            sys.exit(f"error: {keep} does not exist")
    with env.lock():
        lines = env.lines()
        for group, fname, src in refs:
            if keep:
                if (keep / fname).is_symlink():
                    (keep / fname).unlink()
                elif (keep / fname).exists():
                    sys.exit(f"error: {keep / fname} exists and is not the link")
                line = index_line(env, fname, group, tag=False)
                shutil.move(str(src), keep / fname)
                add_local_line(keep / "MEMORY.md", line)
            else:
                src.unlink()
            lines.pop(f"{group}/{fname}", None)
            print(f"unshared {group}/{fname}" + (f" (kept in {args.keep})" if keep else ""))
        env.save(lines=lines)
        print_report(reconcile_all(env))


def cmd_move(env, args):
    groups = env.groups()
    if args.group not in groups:
        sys.exit(f"error: no group {args.group!r} in {env.config}")
    refs = [shared_ref(env, r) for r in args.memories]
    with env.lock():
        for group, fname, src in refs:
            g = taken(env, groups, args.group, fname, ignore=group)
            if g:
                sys.exit(f"error: {g}/{fname} already exists")
        (env.store / args.group).mkdir(parents=True, exist_ok=True)
        lines = env.lines()
        for group, fname, src in refs:
            os.replace(src, env.store / args.group / fname)
            if f"{group}/{fname}" in lines:
                lines[f"{args.group}/{fname}"] = lines.pop(f"{group}/{fname}")
            print(f"moved    {group}/{fname} -> {args.group}")
        env.save(lines=lines)
        print_report(reconcile_all(env))


def cmd_line(env, args):
    group, fname, src = shared_ref(env, args.memory)
    if args.title is not None or args.summary is not None:
        with env.lock():
            lines = env.lines()
            key = f"{group}/{fname}"
            cur = dict(lines.get(key) or dict(zip(("title", "summary"), front(src))))
            if args.title is not None:
                cur["title"] = args.title
            if args.summary is not None:
                cur["summary"] = args.summary
            lines[key] = cur
            env.save(lines=lines)
            print_report(reconcile_all(env, env.members(group)))
    print(f"line     {index_line(env, fname, group)}")


def cmd_group(env, args):
    groups = env.groups()
    name = args.name
    if args.delete:
        if name not in groups:
            sys.exit(f"error: no group {name!r}")
        if (env.store / name).is_dir() and any((env.store / name).glob("*.md")):
            sys.exit(f"error: group {name} still has memories; unshare or move them first")
        del groups[name]
        print(f"deleted  group {name}")
    elif args.add or args.remove:
        entries = groups.setdefault(name, [])
        entries += [e for e in args.add if e not in entries]
        missing = [e for e in args.remove if e not in entries]
        if missing:
            sys.exit(f"error: {', '.join(missing)} not in group {name}: {entries}")
        groups[name] = [e for e in entries if e not in args.remove]
        print(f"group    {name}: {', '.join(groups[name]) or '(empty)'}")
    else:
        if name not in groups:
            sys.exit(f"error: no group {name!r}")
        print(f"group    {name}: {', '.join(groups[name])}")
        print(f"projects {', '.join(env.members(name)) or '(none with memory yet)'}")
        return
    with env.lock():
        env.save_groups(groups)
        print_report(reconcile_all(env))


def cmd_sync(env, args):
    with env.lock():
        if args.project:
            print_report([(args.project, *reconcile(env, args.project, create=True))])
        else:
            print_report(reconcile_all(env))


def cmd_status(env, args):
    groups = env.groups()
    if not groups:
        print(f"no groups yet: group <name> --add <project folder or path>")
    lines = env.lines()
    for g, entries in groups.items():
        folder = env.store / g
        files = sorted(f.name for f in folder.glob("*.md")) if folder.is_dir() else []
        print(f"\n[{g}] {', '.join(entries)}")
        print(f"  projects: {', '.join(env.members(g)) or '(none with memory yet)'}")
        print(f"  memories: {', '.join(files) or '(none)'}")
        fallback = [f for f in files if f"{g}/{f}" not in lines]
        if fallback:
            print(f"  index line from name and description (set it with line): {', '.join(fallback)}")
    pending = []
    for slug in env.with_memory():
        added, removed, conflicts = reconcile(env, slug, dry=True)
        pending += [f"{slug}: missing {file_of(a)}" for a in added]
        pending += [f"{slug}: stale link {r}" for r in removed] + conflicts
    print("\npending (run sync):" if pending else "\nnothing pending")
    for line in pending:
        print(f"  {line}")
    if not hooks_installed(load_settings(env)):
        print("\nwarning: hooks not installed, nothing syncs on its own (run install)")


def file_of(line):
    return re.search(r"\]\((.*?)\)", line).group(1)


def print_report(report):
    for slug, added, removed, conflicts in report:
        for a in added:
            print(f"  {slug}: + {file_of(a)}")
        for r in removed:
            print(f"  {slug}: - {r}")
        for c in conflicts:
            print(f"  conflict: {c}")


# --- install ----------------------------------------------------------------

def load_settings(env):
    path = env.root / "settings.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"error: {path} is not valid JSON ({e}); fix it first")


def hooks_installed(settings):
    hooks = settings.get("hooks", {})
    return all(any("share_memories.py" in h.get("command", "")
                   for entry in hooks.get(event, []) for h in entry.get("hooks", []))
               for event in HOOK_EVENTS)


def hook_command(env):
    script = Path(__file__).resolve()
    # $HOME/.claude works on the host and in a container that mounts ~/.claude elsewhere.
    try:
        rel = script.relative_to((Path.home() / ".claude").resolve())
        if env.root.resolve() == (Path.home() / ".claude").resolve():
            return f'python3 "$HOME/.claude/{rel}" hook'
    except ValueError:
        pass
    return f'python3 "{script}" hook'


def cmd_install(env, args):
    settings = load_settings(env)
    command = hook_command(env)
    hooks = settings.setdefault("hooks", {})
    changed = []
    for event, matcher in HOOK_EVENTS.items():
        entries = hooks.setdefault(event, [])
        if any("share_memories.py" in h.get("command", "") for e in entries for h in e.get("hooks", [])):
            continue
        entry = {"matcher": matcher} if matcher else {}
        entry["hooks"] = [{"type": "command", "command": command}]
        entries.append(entry)
        changed.append(event)
    if not env.config.exists():
        print(f"{'would create' if args.dry_run else 'created '} {env.config}")
        if not args.dry_run:
            env.save_groups({})
    path = env.root / "settings.json"
    if not changed:
        print(f"hooks already in {path}")
        return
    if args.dry_run:
        print(f"would add {', '.join(changed)} to {path}:")
        print(json.dumps({"hooks": settings["hooks"]}, indent=2))
        return
    if path.exists():
        shutil.copy2(path, path.with_name("settings.json.bak"))
    write_atomic(path, json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    print(f"added    {', '.join(changed)} hooks to {path}" + (" (backup: settings.json.bak)" if path.with_name("settings.json.bak").exists() else ""))
    print("they apply to sessions started from now on")


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
            notes.append("share-memories conflicts to resolve with the user (skill share-memories):\n"
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
            report = reconcile_all(env, env.members(path.parent.name))
        conflicts = [c for r in report for c in r[3]]
        if conflicts:
            context(event, "share-memories conflicts:\n" + "\n".join(conflicts))
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
                       f"share-memories skill: keep it local (do nothing) or share it with a group.")


def main():
    ap = argparse.ArgumentParser(description="Share Claude Code memories between projects.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="groups, members, shared memories, pending fixes")
    s = sub.add_parser("share", help="move memories into a group")
    s.add_argument("group")
    s.add_argument("files", nargs="+", help="memory paths in <claude>/projects/<project>/memory/")
    s = sub.add_parser("unshare", help="take memories out of their group")
    s.add_argument("memories", nargs="+", help="<group>/<file>.md")
    s.add_argument("--keep", metavar="PROJECT", help="project folder that keeps a plain copy")
    s = sub.add_parser("move", help="move shared memories to another group")
    s.add_argument("group")
    s.add_argument("memories", nargs="+", help="<group>/<file>.md")
    s = sub.add_parser("line", help="show or set a shared memory's MEMORY.md line")
    s.add_argument("memory", help="<group>/<file>.md")
    s.add_argument("--title")
    s.add_argument("--summary")
    s = sub.add_parser("group", help="show, create, change or delete a group")
    s.add_argument("name")
    s.add_argument("--add", action="append", default=[], metavar="ENTRY", help="project folder or path (* allowed); repeatable")
    s.add_argument("--remove", action="append", default=[], metavar="ENTRY")
    s.add_argument("--delete", action="store_true")
    s = sub.add_parser("sync", help="repair links and index blocks")
    s.add_argument("--project", metavar="FOLDER", help="only this project folder (creates memory/ if needed)")
    s = sub.add_parser("install", help="add the two hooks to settings.json and create groups.json")
    s.add_argument("--dry-run", action="store_true")
    sub.add_parser("hook", help="called by the Claude Code hooks (JSON on stdin)")
    args = ap.parse_args(protect(sys.argv[1:]))
    env = Env(claude_dir())
    {"status": cmd_status, "share": cmd_share, "unshare": cmd_unshare, "move": cmd_move,
     "line": cmd_line, "group": cmd_group, "sync": cmd_sync, "install": cmd_install, "hook": cmd_hook}[args.cmd](env, args)


def protect(argv):
    """Project folders start with "-" (-dev-sandbox) and argparse would take them for
    options, so values become --flag=value: one for --keep/--project, each for --add/--remove."""
    out, flag, got = [], None, False
    for a in argv:
        if a in ("--keep", "--project", "--add", "--remove"):
            if flag and not got:
                out.append(flag)
            flag, got = a, False
            continue
        if flag and not a.startswith("--") and (not got or flag in ("--add", "--remove")):
            out.append(f"{flag}={a}")
            got = True
            continue
        if flag and not got:
            out.append(flag)  # flag without a value: let argparse report it
        flag = None
        out.append(a)
    if flag and not got:
        out.append(flag)
    return out

if __name__ == "__main__":
    main()
