#!/usr/bin/env python3
"""Keep read-only copies of outside git repositories in mirrors/ at the repository root.

The manifest mirrors/mirrors.json (versioned) says what is fetched, from where and at which commit;
the copies (mirrors/<name>/, gitignored) have no .git, are read-only and record their commit in
.mirror-commit. Run anywhere inside the repository:

  fetch_mirrors.py [target ...]              fetch targets (default: all)
  fetch_mirrors.py --check [target ...]      report missing, stale or outdated targets (exit 1 if any)
  fetch_mirrors.py --list                    show the manifest, one line per target
  fetch_mirrors.py --add name url [--ref R] [--include PATH ...] [--license ID ...] [--follow]
                                             add a mirror (pinned to the ref's newest commit, or following it), fetch it
  fetch_mirrors.py --pin target [ref|commit] write the ref's newest commit (or the commit) into the manifest, fetch
  fetch_mirrors.py --follow target           always fetch the newest commit of the ref (docs that change often)
  fetch_mirrors.py --remove target           delete the copy and the manifest entry

A target is a mirror (`zed`; a set = all its members) or one member of a set (`cm6/view`). A url with
`{member}` makes a set; pinning a member it does not list yet adds it. A ref is `main`, `v1.2`, a full
`refs/...` name or HEAD. "include" fetches only those paths (sparse checkout, plus the repository's
LICENSE* files); "license_check": "cargo" refuses included crates whose Cargo.toml license is not in
"license". The manifest and the .gitignore lines are created when missing.
"""
import argparse, json, os, pathlib, re, shutil, stat, subprocess, sys, tempfile

GITIGNORE = ['/mirrors/*', '!/mirrors/mirrors.json']
WHAT = ('Read-only copies of outside repositories, fetched into mirrors/<name>/ (gitignored) by the mirrors '
        'skill (fetch_mirrors.py). Entries with "commit" are pinned; entries with "follow": true take the '
        'newest commit of "ref" on every fetch. Cite files as mirrors/<name>/<path> or mirrors/<set>/<member>/<path>.')


def run(*a, cwd=None, check=True):
    return subprocess.run(a, cwd=cwd, check=check, capture_output=True, text=True)


def repo_root():
    r = run('git', 'rev-parse', '--show-toplevel', check=False)
    return pathlib.Path(r.stdout.strip()) if r.returncode == 0 else pathlib.Path.cwd()


ROOT = repo_root()
MIRRORS = ROOT / 'mirrors'
MANIFEST = MIRRORS / 'mirrors.json'


def load():
    if not MANIFEST.exists():
        MIRRORS.mkdir(exist_ok=True)
        save({'_what': WHAT, 'mirrors': {}})
        print(f'created  {MANIFEST.relative_to(ROOT)} (commit it)')
    ensure_gitignore()
    return json.loads(MANIFEST.read_text())


def save(data):
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def ensure_gitignore():
    """Copies ignored, manifest tracked. Appends the two lines only when git does not already agree."""
    if not (ROOT / '.git').exists():
        return
    ignored = lambda p: run('git', 'check-ignore', '-q', p, cwd=ROOT, check=False).returncode == 0
    if ignored('mirrors/x/y') and not ignored('mirrors/mirrors.json'):
        return
    gi = ROOT / '.gitignore'
    text = gi.read_text() if gi.exists() else ''
    if not all(l in text.splitlines() for l in GITIGNORE):
        gi.write_text(text + ('' if text.endswith('\n') or not text else '\n')
                      + '\n# mirrors skill: copies ignored, manifest versioned\n' + '\n'.join(GITIGNORE) + '\n')
        print('updated  .gitignore (commit it)')
    if not ignored('mirrors/x/y') or ignored('mirrors/mirrors.json'):
        print(f'warning  .gitignore: another rule overrides {" and ".join(GITIGNORE)} (e.g. "mirrors/"); fix it by hand')


def resolve(url, ref):
    """Commit at the tip of ref (tags peeled). Short names try tags, then branches."""
    names = [ref] if ref == 'HEAD' or ref.startswith('refs/') else [f'refs/tags/{ref}', f'refs/heads/{ref}']
    for name in names:
        out = run('git', 'ls-remote', url, name, name + '^{}', check=False)
        if out.returncode:
            sys.exit(f'{url}: {out.stderr.strip()}')
        lines = dict(reversed(l.split('\t')) for l in out.stdout.splitlines())
        sha = lines.get(name + '^{}') or lines.get(name)
        if sha:
            return name, sha
    sys.exit(f'{url}: no ref {ref}')


def default_ref(url):
    out = run('git', 'ls-remote', '--symref', url, 'HEAD').stdout
    m = re.search(r'^ref: (\S+)\tHEAD', out, re.M)
    return m.group(1) if m else 'HEAD'


def split(data, name):
    mirror, _, member = name.partition('/')
    if mirror not in data['mirrors']:
        sys.exit(f'no mirror {mirror!r} in {MANIFEST.relative_to(ROOT)} (add it: --add {mirror} <url>)')
    return mirror, member, data['mirrors'][mirror]


def targets(data, names):
    """Yield (label, entry, url, dst, mirror) for every target named (or all)."""
    for name in names or list(data['mirrors']):
        mirror, member, e = split(data, name)
        if e['kind'] == 'set':
            if member and member not in e['members']:
                sys.exit(f'{mirror} has no member {member!r} (add it: --pin {name} <ref>)')
            for mem in [member] if member else list(e['members']):
                yield f'{mirror}/{mem}', e['members'][mem], e['url'].format(member=mem), MIRRORS / mirror / mem, e
        else:
            yield mirror, e, e['url'], MIRRORS / mirror, e


def entry_of(data, name, create_ref=None):
    mirror, member, e = split(data, name)
    if e['kind'] != 'set':
        return e, e['url']
    if not member:
        sys.exit(f'name one member of the set: {mirror}/<member>')
    url = e['url'].format(member=member)
    if member not in e['members']:
        if not create_ref:
            sys.exit(f'{mirror} has no member {member!r}')
        e['members'][member] = {'ref': create_ref}
    return e['members'][member], url


def following(entry, mirror):
    return entry.get('follow', False)


def license_problems(tree, entry, mirror):
    if mirror.get('license_check') != 'cargo':
        return []
    bad = []
    for inc in entry.get('include', mirror.get('include', [])):
        toml = tree / inc / 'Cargo.toml'
        m = re.search(r'^license\s*=\s*"([^"]+)"', toml.read_text(), re.M) if toml.exists() else None
        if not m or m.group(1) not in mirror['license']:
            bad.append(f'{inc}: {m.group(1) if m else "no license field"}')
    return bad


def drop_outside_links(tree):
    """A link to ../../.ssh or /etc would let a reader of the mirror read outside it."""
    dropped, top = [], tree.resolve()
    for dirpath, dirs, files in os.walk(tree):
        for n in dirs + files:
            p = pathlib.Path(dirpath, n)
            if p.is_symlink() and not p.resolve().is_relative_to(top):
                dropped.append(str(p.relative_to(tree)))
                p.unlink()
    return dropped


def set_writable(tree, writable):
    """Read-only copies: edits fail instead of being lost on the next fetch."""
    for dirpath, dirs, files in os.walk(tree):
        for f in files:
            p = os.path.join(dirpath, f)
            if not os.path.islink(p):
                mode = os.stat(p).st_mode
                os.chmod(p, mode | stat.S_IWUSR if writable else mode & ~0o222)
        mode = os.stat(dirpath).st_mode
        os.chmod(dirpath, mode | stat.S_IWUSR if writable else mode & ~0o222)


def delete(tree):
    if tree.exists():
        set_writable(tree, True)
        shutil.rmtree(tree)


def fetch(label, entry, url, dst, mirror, commit):
    include = entry.get('include', mirror.get('include'))
    with tempfile.TemporaryDirectory() as tmp:
        t = pathlib.Path(tmp)
        run('git', 'init', '-q', cwd=t)
        run('git', 'remote', 'add', 'origin', url, cwd=t)
        filt = ['--filter=blob:none'] if include else []
        if include:
            run('git', 'sparse-checkout', 'set', '--no-cone', '/LICENSE*', *[f'/{p.strip("/")}/' for p in include], cwd=t)
        if run('git', 'fetch', '-q', '--depth', '1', *filt, 'origin', commit, cwd=t, check=False).returncode:
            # servers that refuse fetching a commit by id
            run('git', 'fetch', '-q', *filt, 'origin', f'{entry["ref"]}:refs/mirror', cwd=t)
        run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', commit, cwd=t)
        bad = license_problems(t, entry, mirror)
        if bad:
            sys.exit(f'refused  {label}: license not in {mirror["license"]}: ' + '; '.join(bad))
        shutil.rmtree(t / '.git')
        dropped = drop_outside_links(t)
        delete(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(t, dst, symlinks=True)
        os.chmod(dst, 0o755)   # the temp dir was 0700
    (dst / '.mirror-commit').write_text(commit + '\n')
    set_writable(dst, False)
    print(f'fetched  {label} {commit[:7]}{" (following " + entry["ref"] + ")" if following(entry, mirror) else ""}')
    for d in dropped:
        print(f'  dropped link pointing outside the mirror: {d}')


def sync(data, names, check):
    problems = 0
    for label, entry, url, dst, mirror in targets(data, names):
        stamp = dst / '.mirror-commit'
        have = stamp.read_text().strip() if stamp.exists() else None
        if following(entry, mirror):
            want = resolve(url, entry['ref'])[1]
        elif entry.get('commit'):
            want = entry['commit']
        else:
            print(f'unpinned {label} (pin it: --pin {label}, or --follow {label})')
            continue
        if have == want:
            print(f'ok       {label} {have[:7]}')
        elif check:
            state = 'missing' if have is None else 'outdated' if following(entry, mirror) else 'stale'
            print(f'{state:8} {label} (want {want[:7]})')
            problems += 1
        else:
            fetch(label, entry, url, dst, mirror, want)
    return problems


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    act = p.add_mutually_exclusive_group()
    act.add_argument('--check', action='store_true')
    act.add_argument('--list', action='store_true')
    act.add_argument('--add', nargs=2, metavar=('NAME', 'URL'))
    act.add_argument('--pin', action='store_true', help='targets: TARGET [REF|COMMIT]')
    act.add_argument('--remove', action='store_true')
    p.add_argument('--follow', action='store_true', help='TARGET: follow its ref from now on; with --add: add it following')
    p.add_argument('--ref', help='with --add: branch, tag or refs/... (default: the remote HEAD branch)')
    p.add_argument('--include', nargs='+', default=[], metavar='PATH', help='with --add: fetch only these paths')
    p.add_argument('--license', nargs='+', default=[], metavar='ID', help='with --add: SPDX ids, e.g. MIT')
    p.add_argument('targets', nargs='*')
    a = p.parse_args()
    data = load()

    if a.list:
        for label, entry, url, dst, mirror in targets(data, a.targets):
            how = f'follow {entry["ref"]}' if following(entry, mirror) else f'pin {(entry.get("commit") or "none")[:7]} ({entry["ref"]})'
            print(f'{label:24} {how:32} {url}')
        return 0

    if a.add:
        name, url = a.add
        if name in data['mirrors']:
            sys.exit(f'{name} already exists')
        if '{member}' in url:
            data['mirrors'][name] = {'kind': 'set', 'url': url, 'license': a.license, 'members': {}}
            save(data)
            print(f'added    set {name}; add members with --pin {name}/<member> <ref>')
            return 0
        ref, commit = resolve(url, a.ref or default_ref(url))
        e = {'kind': 'repo', 'url': url, 'ref': ref}
        e.update({'follow': True} if a.follow else {'commit': commit})
        if a.include:
            e['include'] = a.include
        e['license'] = a.license
        data['mirrors'][name] = e
        save(data)
        print(f'added    {name} {ref} {"(following)" if a.follow else "-> " + commit[:7]} (commit mirrors/mirrors.json)')
        if not a.license:
            print('  no license recorded: check it and add "license" to the entry')
        return sync(data, [name], False)

    if a.follow and (a.check or a.list or a.pin or a.remove):
        sys.exit('--follow goes alone with a target, or with --add')

    if a.pin or a.follow or a.remove:
        if not a.targets:
            sys.exit('name a target')
        name = a.targets[0]

    if a.remove:
        mirror, member, e = split(data, name)
        if e['kind'] == 'set' and member:
            e['members'].pop(member, None)
            delete(MIRRORS / mirror / member)
        else:
            del data['mirrors'][mirror]
            delete(MIRRORS / mirror)
        save(data)
        print(f'removed  {name} (commit mirrors/mirrors.json)')
        return 0

    if a.follow:
        entry, url = entry_of(data, name)
        entry['follow'] = True
        entry.pop('commit', None)
        save(data)
        print(f'follow   {name} {entry["ref"]} (commit mirrors/mirrors.json)')
        return sync(data, [name], False)

    if a.pin:
        arg = a.targets[1] if len(a.targets) > 1 else None
        sha = bool(arg and re.fullmatch(r'[0-9a-f]{40}', arg))
        entry, url = entry_of(data, name, create_ref='HEAD' if sha or not arg else arg)
        if sha:
            entry['commit'] = arg
        else:
            entry['ref'], entry['commit'] = resolve(url, arg or entry['ref'])
        entry.pop('follow', None)
        save(data)
        print(f'pinned   {name} {entry["ref"]} -> {entry["commit"][:7]} (commit mirrors/mirrors.json)')
        return sync(data, [name], False)

    return 1 if sync(data, a.targets, a.check) else 0


if __name__ == '__main__':
    sys.exit(main())
