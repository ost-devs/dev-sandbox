import re


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def truncate(s, n):
    return s if len(s) <= n else s[:n - 1] + '…'


def count_words(s):
    return len(s.split())


def capitalize_words(s):
    return ' '.join(w[:1].upper() + w[1:] for w in s.split(' '))


def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
