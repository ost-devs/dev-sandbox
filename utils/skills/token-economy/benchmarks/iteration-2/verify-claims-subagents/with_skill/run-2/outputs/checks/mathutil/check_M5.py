import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import is_prime
N = 1000
sieve = [True]*(N+1); sieve[0]=sieve[1]=False
for i in range(2, int(N**0.5)+1):
    if sieve[i]:
        for j in range(i*i, N+1, i): sieve[j] = False
def prop(n): return is_prime(n) == sieve[n]
cases = [4, 9, 25, 0, 1, 2, 3] + list(range(0, N+1))
res = search("M5", cases, prop, "exhaustive 0..1000 vs sieve of Eratosthenes")
