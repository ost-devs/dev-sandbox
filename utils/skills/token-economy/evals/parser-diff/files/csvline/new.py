import re

_FIELD = re.compile(r'\s*(?:"([^"]*)"|([^,]*?))\s*(?:,|$)')


def parse(line):
    """Split one CSV line into fields (rewrite of old.parse, regex based)."""
    fields = []
    pos = 0
    while pos < len(line):
        m = _FIELD.match(line, pos)
        quoted, plain = m.group(1), m.group(2)
        fields.append(quoted if quoted is not None else plain)
        if m.end() == pos:
            break
        pos = m.end()
    return fields or ['']
