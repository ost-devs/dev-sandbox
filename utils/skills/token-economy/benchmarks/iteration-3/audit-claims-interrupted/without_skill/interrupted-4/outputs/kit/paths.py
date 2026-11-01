def join(*parts):
    return '/'.join(p.strip('/') for p in parts if p)


def ext(p):
    return p.rsplit('.', 1)[1] if '.' in p else ''


def stem(name):
    return name.rsplit('.', 1)[0]


def normalize(p):
    absolute = p.startswith('/')
    stack = []
    for part in p.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if stack:
                stack.pop()
            continue
        stack.append(part)
    body = '/'.join(stack)
    if absolute:
        return '/' + body
    return body or '.'


def is_hidden(p):
    return p.rstrip('/').rsplit('/', 1)[-1].startswith('.')


def depth(p):
    return len([x for x in p.split('/') if x])


def parent(p):
    return p.rsplit('/', 1)[0] if '/' in p else ''
