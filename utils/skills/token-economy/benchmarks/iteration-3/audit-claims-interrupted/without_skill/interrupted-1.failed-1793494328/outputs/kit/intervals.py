def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def length(a):
    return a[1] - a[0]


def contains(a, x):
    return a[0] <= x <= a[1]


def merge(intervals):
    s = sorted(intervals)
    out = [s[0]]
    for start, end in s[1:]:
        last_start, last_end = out[-1]
        if start <= last_end:
            out[-1] = (last_start, max(last_end, end))
        else:
            out.append((start, end))
    return out


def intersect(a, b):
    if not overlaps(a, b):
        return None
    return (max(a[0], b[0]), min(a[1], b[1]))


def total_covered(intervals):
    return sum(length(i) for i in merge(intervals))
