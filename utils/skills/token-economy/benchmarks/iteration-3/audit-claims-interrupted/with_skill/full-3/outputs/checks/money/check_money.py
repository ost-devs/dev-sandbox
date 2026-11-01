import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import Checker, ROOT
sys.path.insert(0, os.path.join(ROOT, "kit"))
import money as m
c = Checker("money")

def eq(a, b): return None if a == b else f"got {a!r}, expected {b!r}"
c.fixed("M01", lambda: eq(m.to_cents('12,34'), 1234))
c.fixed("M02", lambda: eq(m.to_cents('1.234,5'), 123450))
c.fixed("M03", lambda: eq(m.to_cents('-1,50'), -150))
c.fixed("M04", lambda: eq(m.to_cents('7'), 700))
c.fixed("M05", lambda: eq(m.format_brl(123456), 'R$ 1.234,56'))
c.fixed("M06", lambda: eq(m.format_brl(5), 'R$ 0,05'))
c.fixed("M07", lambda: eq(m.format_brl(-150), 'R$ -1,50'))
def m08():
    for x in range(0, 1000001):
        if m.to_cents(m.format_brl(x)[3:]) != x: return f"c={x}"
c.fixed("M08", m08)
c.prop("M09", lambda r: (r.randint(0, 10000), r.randint(1, 20)), lambda t, k: sum(m.split_bill(t, k)) == t)
c.fixed("M10", lambda: eq(m.split_bill(900, 3), [300, 300, 300]))
c.prop("M11", lambda r: (r.randint(0, 10000), r.randint(1, 20)), lambda t, k: sum(m.installments(t, k)) == t)
c.prop("M12", lambda r: (r.randint(0, 10000), r.randint(1, 20)),
       lambda t, k: max(m.installments(t, k)) - min(m.installments(t, k)) <= 1)
c.fixed("M13", lambda: eq(m.installments(100, 3), [34, 33, 33]))
c.fixed("M14", lambda: eq(m.apply_discount(1000, 10), 900))
def m15():
    for x in range(0, 1000001):
        if m.apply_discount(x, 0) != x: return f"c={x}"
c.fixed("M15", m15)
def m16():
    for x in range(0, 1000001, 7):
        for p in range(101):
            if m.apply_discount(x, p) > x: return f"c={x} p={p}"
    for x in range(0, 2000):
        for p in range(101):
            if m.apply_discount(x, p) > x: return f"c={x} p={p}"
c.fixed("M16", m16)
c.fixed("M17", lambda: eq(m.add_tax(100, 0.15), 115))
def m18():
    for x in range(0, 1000001):
        if m.add_tax(x, 0) != x: return f"c={x}"
c.fixed("M18", m18)
c.prop("M19", lambda r: (r.randint(0, 1000000), r.random() if r.random() < .9 else r.choice([0, 1, 1e-17])),
       lambda x, rt: m.add_tax(x, rt) >= x)
c.finish()
