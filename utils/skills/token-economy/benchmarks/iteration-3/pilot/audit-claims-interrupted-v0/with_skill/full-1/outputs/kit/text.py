import re
import unicodedata


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def truncate(s, n, suffix='...'):
    return s if len(s) <= n else s[:n - len(suffix)] + suffix


def count_words(s):
    return len(s.split())


def title_case(s):
    return ' '.join(w[:1].upper() + w[1:] for w in s.split(' '))


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def pad_left(s, n, ch=' '):
    return s.rjust(n, ch)


def is_palindrome(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
