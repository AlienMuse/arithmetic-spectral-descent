"""Generate reproducible datasets for Part IX.  Runtime target <10 minutes."""
import csv, math, json, os
import numpy as np
from mpmath import mp
OUT=os.path.dirname(__file__)
# A/B: sieve to 10^7
N=10_000_000
checks=[1_000,10_000,100_000,1_000_000,10_000_000]
isprime=np.ones(N+1,dtype=bool); isprime[:2]=False
for p in range(2,math.isqrt(N)+1):
    if isprime[p]: isprime[p*p:N+1:p]=False
primes=np.flatnonzero(isprime)
lam=np.zeros(N+1); 
for p in primes:
    q=int(p); lp=math.log(p)
    while q<=N: lam[q]=lp; q*=int(p)
psi=np.cumsum(lam); n=np.arange(N+1,dtype=float); n[0]=1
weighted=np.cumsum(lam/np.sqrt(n))
with open(os.path.join(OUT,'square_root_psi_data.csv'),'w',newline='') as f:
 w=csv.writer(f); w.writerow(['X','psi_minus_X','error_over_sqrtX','schoenfeld_factor_log2_over_8pi','weighted_lambda','two_sqrtX','weighted_ratio'])
 for x in checks:
  w.writerow([x,psi[x]-x,(psi[x]-x)/math.sqrt(x),math.log(x)**2/(8*math.pi),weighted[x],2*math.sqrt(x),weighted[x]/(2*math.sqrt(x))])
# C/D zeros and gaps
mp.dps=40
zeros=[mp.im(mp.zetazero(k)) for k in range(1,201)]
with open(os.path.join(OUT,'zeta_first_200_zeros.csv'),'w',newline='') as f:
 w=csv.writer(f); w.writerow(['index','ordinate'])
 for i,z in enumerate(zeros,1): w.writerow([i,mp.nstr(z,25)])
gaps=[]
for i in range(199):
 mid=(zeros[i]+zeros[i+1])/2
 local_mean=2*mp.pi/mp.log(mid/(2*mp.pi))
 gaps.append(float((zeros[i+1]-zeros[i])/local_mean))
counts,edges=np.histogram(gaps,bins=np.arange(0,4.05,.1),density=True)
with open(os.path.join(OUT,'zero_gap_histogram.csv'),'w',newline='') as f:
 w=csv.writer(f); w.writerow(['left','right','density','wigner_surmise_GUE_midpoint'])
 for c,l,r in zip(counts,edges[:-1],edges[1:]):
  s=(l+r)/2; w.writerow([l,r,c,(32/math.pi**2)*s*s*math.exp(-4*s*s/math.pi)])
# E support envelope
with open(os.path.join(OUT,'support_doubling_envelope.csv'),'w',newline='') as f:
 w=csv.writer(f); ds=[.05,.1,.2,.3,.4,.45]; w.writerow(['S','arithmetic_S_exp_S_over_2']+[f'injected_delta_{d}' for d in ds])
 for S in np.linspace(0,40,161): w.writerow([S,S*math.exp(S/2)]+[math.exp(d*S) for d in ds])
# F normalized shape functions; constants c=1 are explicitly dimensionless plotting normalizations, not claimed explicit regions.
with open(os.path.join(OUT,'zero_free_boundary_shapes.csv'),'w',newline='') as f:
 w=csv.writer(f); w.writerow(['t','sigma_classical_c1','sigma_VK_c1','sigma_one','sigma_critical_half'])
 for t in np.logspace(1,10,181):
  L=math.log(t); LL=math.log(max(L,math.e))
  w.writerow([t,1-1/L,1-1/(L**(2/3)*LL**(1/3)),1,.5])
# G exponents
with open(os.path.join(OUT,'GLn_exponents.csv'),'w',newline='') as f:
 w=csv.writer(f); w.writerow(['n','LRS_theta_half_minus_1_over_n2_plus_1','best_annotation','theta_used'])
 for k in range(2,11):
  lrs=.5-1/(k*k+1); used=7/64 if k==2 else lrs
  ann='Kim-Sarnak 7/64 (GL2)' if k==2 else 'Luo-Rudnick-Sarnak general bound'
  w.writerow([k,lrs,ann,used])
summary={'N_sieve':N,'zero_count':len(zeros),'gap_count':len(gaps),'gap_mean':float(np.mean(gaps)),'gap_std':float(np.std(gaps)),'first_zero':str(zeros[0]),'last_zero':str(zeros[-1]),'weighted_at_1e7':float(weighted[N]),'psi_error_at_1e7':float(psi[N]-N)}
with open(os.path.join(OUT,'part_ix_dataset_summary.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
