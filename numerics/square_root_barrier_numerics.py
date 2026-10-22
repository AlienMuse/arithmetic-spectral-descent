"""Numerical diagnostics for the square-root-barrier chapter.
Computes psi(X), sum Lambda(n)/sqrt(n), and Schoenfeld-normalized psi error.
"""
import math
import numpy as np

N=10_000_000
checks=np.array([1_000,10_000,100_000,1_000_000,10_000_000],dtype=np.int64)
isprime=np.ones(N+1,dtype=bool); isprime[:2]=False
for p in range(2,math.isqrt(N)+1):
    if isprime[p]: isprime[p*p:N+1:p]=False
primes=np.flatnonzero(isprime)
lam=np.zeros(N+1,dtype=np.float64)
for p in primes:
    q=int(p); lp=math.log(p)
    while q<=N:
        lam[q]=lp; q*=int(p)
psi=np.cumsum(lam)
n=np.arange(N+1,dtype=np.float64); n[0]=1.0
weighted=np.cumsum(lam/np.sqrt(n))
print('| X | psi(X)-X | (psi(X)-X)/sqrt(X) | Schoenfeld factor log^2(X)/(8pi) | sum Lambda/sqrt(n) | 2sqrt(X) | ratio |')
print('|---:|---:|---:|---:|---:|---:|---:|')
for X in checks:
    err=psi[X]-X
    norm=err/math.sqrt(X)
    sch=math.log(X)**2/(8*math.pi)
    sw=weighted[X]; two=2*math.sqrt(X)
    print(f'| {X:,} | {err:.8f} | {norm:.8f} | {sch:.8f} | {sw:.8f} | {two:.8f} | {sw/two:.8f} |')
