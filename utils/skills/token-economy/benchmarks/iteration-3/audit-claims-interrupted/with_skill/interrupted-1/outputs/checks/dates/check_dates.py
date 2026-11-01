import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import dates as M
import calendar
from datetime import date, timedelta
START=date(2000,1,1); NDAYS=(date(2030,12,31)-START).days+1
def alld(): return (START+timedelta(days=i) for i in range(NDAYS))
def each(pred):
    for x in alld():
        try:
            if not pred(x): return f'x={x!r}'
        except Exception as e: return f'x={x!r} raised {type(e).__name__}: {e}'
def gd(r): return date(r.randint(1,9999),r.randint(1,12),r.randint(1,28))
def D02(): return each(lambda x: (lambda y:(y.day,y.month,y.year)==(x.day,x.month,x.year+1))(M.add_months(x,12)))
def D03(): return each(lambda x: M.add_months(M.add_months(x,1),-1)==x)
def D04(): return forall('D04',lambda r:(gd(r),gd(r)),lambda a,b:M.days_between(a,b)>=0) or ('args=(date(2024,1,2), date(2024,1,1))' if M.days_between(date(2024,1,2),date(2024,1,1))<0 else None)
def D05(): return forall('D05',lambda r:(gd(r),gd(r)),lambda a,b:M.days_between(a,b)==-M.days_between(b,a))
def D08():
    for y in range(1,10000):
        if M.is_leap(y)!=calendar.isleap(y): return f'y={y}'
def D11(): return forall('D11',lambda r:gd(r),lambda d:M.quarter(d) in (1,2,3,4))
def D13(): return each(lambda x: M.end_of_month(x)>=x)
def D16():
    try: v=M.parse_br('1/2/2024')
    except ValueError: return None
    return f"parse_br('1/2/2024') returned {v!r}, no ValueError"
def D17():
    r=rng('D17')
    for x in alld():
        for k in [-1000,-1,0,1,1000]+[r.randint(-1000,1000) for _ in range(3)]:
            if M.add_days(x,k)-x!=timedelta(days=k): return f'x={x!r},k={k}'
def D18():
    for x in alld():
        for k in range(-30,31):
            if M.add_months(x,k).day>x.day: return f'x={x!r},k={k}'
def D19(): return each(lambda x: M.weekday_name(M.add_days(x,7))==M.weekday_name(x))
run('dates',{
'D01':lambda:eq(lambda:M.add_months(date(2024,1,31),1),date(2024,2,29)),
'D02':D02,'D03':D03,'D04':D04,'D05':D05,
'D06':lambda:eq(lambda:M.is_leap(1900),False),
'D07':lambda:eq(lambda:M.is_leap(2000),True),
'D08':D08,
'D09':lambda:eq(lambda:M.weekday_name(date(2024,1,1)),'Monday'),
'D10':lambda:eq(lambda:M.quarter(date(2024,4,1)),2),
'D11':D11,
'D12':lambda:eq(lambda:M.end_of_month(date(2023,2,10)),date(2023,2,28)),
'D13':D13,
'D14':lambda:eq(lambda:M.iso_week(date(2021,1,1)),1),
'D15':lambda:eq(lambda:M.parse_br('31/12/2024'),date(2024,12,31)),
'D16':D16,'D17':D17,'D18':D18,'D19':D19})
