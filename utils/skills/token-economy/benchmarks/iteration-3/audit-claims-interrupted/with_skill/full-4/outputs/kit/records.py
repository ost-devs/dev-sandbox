def parse_kv(s):
    return dict(pair.split('=', 1) for pair in s.split(';') if pair)


def to_kv(d):
    return ';'.join(f'{k}={v}' for k, v in d.items())


def pick(d, keys):
    return {k: d[k] for k in keys if k in d}


def rename(d, mapping):
    return {mapping.get(k, k): v for k, v in d.items()}


def group_by(rows, key):
    out = {}
    for r in rows:
        out.setdefault(r[key], []).append(r)
    return out


def sort_by(rows, key):
    return sorted(rows, key=lambda r: r[key])


def deep_get(d, path, default=None):
    for part in path.split('.'):
        if not isinstance(d, dict) or part not in d:
            return default
        d = d[part]
    return d
