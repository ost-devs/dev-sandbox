import sys, os, json, random, calendar
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from datetime import date, timedelta
from kit.dates import *

SEED = 12345
D0, D1 = date(2000, 1, 1).toordinal(), date(2030, 12, 31).toordinal()
def days():
    return (date.fromordinal(o) for o in range(D0, D1 + 1))
NDAYS = D1 - D0 + 1

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

def eq(f, code):
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", "execucao unica"
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), "execucao unica"

def first(it, pred, show, note):
    """it: iterable of cases; returns first failing case."""
    for c in it:
        try:
            if not pred(c):
                return show(c), note
        except Exception as e:
            return show(c) + f" -> excecao {type(e).__name__}: {e}", note
    return None, note + "; nenhum contraexemplo achado"

def rand_dates(n, seed_off=0):
    rng = random.Random(SEED + seed_off)
    return [date.fromordinal(rng.randint(1, date.max.toordinal())) for _ in range(n)]

claim('D01')(lambda: eq(lambda: (add_months(date(2024, 1, 31), 1), date(2024, 2, 29)), "add_months(date(2024,1,31),1)"))
claim('D02')(lambda: first(days(), lambda x: (lambda r: (r.day, r.month, r.year) == (x.day, x.month, x.year + 1))(add_months(x, 12)),
    lambda x: f"add_months({x!r}, 12) = {add_months(x, 12)!r}", f"exaustivo: {NDAYS} datas 2000-2030"))
claim('D03')(lambda: first(days(), lambda x: add_months(add_months(x, 1), -1) == x,
    lambda x: f"add_months(add_months({x!r},1),-1) = {add_months(add_months(x, 1), -1)!r}", f"exaustivo: {NDAYS} datas 2000-2030"))

def pairs():
    edge = [date(2024, 1, 1), date(2024, 1, 2), date(1, 1, 1), date(9999, 12, 31), date(2000, 2, 29)]
    for a in edge:
        for b in edge: yield (a, b)
    rd = rand_dates(2000)
    for i in range(0, 2000, 2): yield (rd[i], rd[i + 1])
PN = f"bordas + 1000 pares aleatorios (semente {SEED}) em todo o dominio de date"
claim('D04')(lambda: first(pairs(), lambda p: days_between(*p) >= 0,
    lambda p: f"days_between({p[0]!r}, {p[1]!r}) = {days_between(*p)}", PN))
claim('D05')(lambda: first(pairs(), lambda p: days_between(p[0], p[1]) == -days_between(p[1], p[0]),
    lambda p: f"days_between({p[0]!r},{p[1]!r}) = {days_between(*p)}, inverso = {days_between(p[1], p[0])}", PN))
claim('D06')(lambda: eq(lambda: (is_leap(1900), False), "is_leap(1900)"))
claim('D07')(lambda: eq(lambda: (is_leap(2000), True), "is_leap(2000)"))
claim('D08')(lambda: first(range(1, 10000), lambda y: is_leap(y) == calendar.isleap(y),
    lambda y: f"is_leap({y}) = {is_leap(y)}", "exaustivo: anos 1..9999"))
claim('D09')(lambda: eq(lambda: (weekday_name(date(2024, 1, 1)), 'Monday'), "weekday_name(date(2024,1,1))"))
claim('D10')(lambda: eq(lambda: (quarter(date(2024, 4, 1)), 2), "quarter(date(2024,4,1))"))
claim('D11')(lambda: first((date(y, m, 1) for y in range(1, 10000) for m in range(1, 13)), lambda x: quarter(x) in (1, 2, 3, 4),
    lambda x: f"quarter({x!r}) = {quarter(x)}", "exaustivo: todos os meses dos anos 1..9999 (quarter depende so do mes)"))
claim('D12')(lambda: eq(lambda: (end_of_month(date(2023, 2, 10)), date(2023, 2, 28)), "end_of_month(date(2023,2,10))"))
claim('D13')(lambda: first(days(), lambda x: end_of_month(x) >= x,
    lambda x: f"end_of_month({x!r}) = {end_of_month(x)!r}", f"exaustivo: {NDAYS} datas 2000-2030"))
claim('D14')(lambda: eq(lambda: (iso_week(date(2021, 1, 1)), 1), "iso_week(date(2021,1,1))"))
claim('D15')(lambda: eq(lambda: (parse_br('31/12/2024'), date(2024, 12, 31)), "parse_br('31/12/2024')"))

def d16():
    try:
        got = parse_br('1/2/2024')
    except ValueError:
        return None, "execucao unica; ValueError levantado"
    except Exception as e:
        return f"parse_br('1/2/2024') levantou {type(e).__name__}, nao ValueError", "execucao unica"
    return f"parse_br('1/2/2024') = {got!r} (nao levantou excecao)", "execucao unica"
claim('D16')(d16)

def d17():
    for x in days():
        xo = x.toordinal()
        for k in range(-1000, 1001):
            if add_days(x, k) - x != timedelta(days=k):
                return f"add_days({x!r}, {k}) - x = {add_days(x, k) - x!r}", "exaustivo"
    return None, f"exaustivo: {NDAYS} datas x 2001 valores de k; nenhum contraexemplo achado"
claim('D17')(d17)
claim('D18')(lambda: first(((x, k) for x in days() for k in range(-30, 31)), lambda c: add_months(*c).day <= c[0].day,
    lambda c: f"add_months({c[0]!r}, {c[1]}) = {add_months(*c)!r}", f"exaustivo: {NDAYS} datas x 61 valores de k"))
claim('D19')(lambda: first(days(), lambda x: weekday_name(add_days(x, 7)) == weekday_name(x),
    lambda x: f"weekday_name(add_days({x!r},7)) = {weekday_name(add_days(x, 7))}, weekday_name(x) = {weekday_name(x)}", f"exaustivo: {NDAYS} datas 2000-2030"))

def main():
    ids = sys.argv[1:] or sorted(R)
    res = []
    for i in ids:
        try:
            ce, note = R[i]()
        except Exception as e:
            ce, note = f"excecao {type(e).__name__}: {e}", "erro na checagem"
        if ce: note = note.replace("; nenhum contraexemplo achado", "; contraexemplo encontrado")
        line = {"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce, "note": note}
        res.append(line)
        print(json.dumps(line, ensure_ascii=False))
    if not sys.argv[1:]:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_dates.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
