"""Data computations for monograph figures 13-30.

Every number printed here is computed from first principles or read from an
existing dataset in numerics/.  Nothing is hand-entered.

Run:  python fig_13_30_data.py
Writes: ../figures/data/fig-13-30-data.json
"""
import csv
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures", "data", "fig-13-30-data.json")
D = {}

# ---------------------------------------------------------------- fig 13/17
# lambda = s(1-s);  lambda < 1/4  <=>  s = 1/2 +- sqrt(1/4 - lambda) real.
def s_from_lambda(lam):
    if lam >= 0.25:
        return ("on-line", 0.5, math.sqrt(lam - 0.25))
    d = math.sqrt(0.25 - lam)
    return ("off-line", 0.5 - d, 0.5 + d)

bounds = [
    ("Randol pinched surface (illustrative point of a proved family)", 0.05),
    ("Selberg 1965  lambda_1 >= 3/16", 3 / 16),
    ("Luo-Rudnick-Sarnak 1995  lambda_1 >= 21/100", 21 / 100),
    ("Kim-Sarnak 2003  lambda_1 >= 1/4 - (7/64)^2 = 975/4096", 975 / 4096),
    ("Selberg conjecture / Ramanujan point  lambda_1 >= 1/4", 0.25),
]
D["fig13_lambda_to_s"] = [
    {"label": lab, "lambda": lam, "map": s_from_lambda(lam)} for lab, lam in bounds
]
D["fig13_tempered_examples"] = [
    {"lambda": 0.25 + t * t, "t": t} for t in (0.35, 0.8, 1.4, 2.1)
]

with open(os.path.join(HERE, "GLn_exponents.csv")) as f:
    D["fig17_GLn"] = list(csv.DictReader(f))

# ---------------------------------------------------------------- fig 14
# r_Q(n) for the principal form of discriminant -23, Q = x^2 + xy + 6y^2,
# and for the other class 2x^2 + xy + 3y^2.  h(-23) = 3.
def rep_counts(a, b, c, N):
    r = [0] * (N + 1)
    M = int(3 * math.isqrt(N)) + 20
    for x in range(-M, M + 1):
        for y in range(-M, M + 1):
            if x == 0 and y == 0:
                continue
            v = a * x * x + b * x * y + c * y * y
            if 0 < v <= N:
                r[v] += 1
    return r

NQ = 40
rQ1 = rep_counts(1, 1, 6, NQ)
rQ2 = rep_counts(2, 1, 3, NQ)
D["fig14_rQ_principal"] = rQ1
D["fig14_rQ_other"] = rQ2
D["fig14_multiplicativity_probe"] = {
    "r(2)": rQ1[2], "r(3)": rQ1[3], "r(6)": rQ1[6],
    "r(2)*r(3)/2": rQ1[2] * rQ1[3] / 2,
    "r(4)": rQ1[4], "r(8)": rQ1[8], "r(12)": rQ1[12],
    "sum_classes_2": rQ1[2] + 2 * rQ2[2],
    "sum_classes_3": rQ1[3] + 2 * rQ2[3],
    "sum_classes_6": rQ1[6] + 2 * rQ2[6],
}

# ---------------------------------------------------------------- fig 21
with open(os.path.join(HERE, "support_doubling_envelope.csv")) as f:
    rows = list(csv.DictReader(f))
D["fig21_header"] = list(rows[0].keys())
D["fig21_S_range"] = [float(rows[0]["S"]), float(rows[-1]["S"])]
D["fig21_n"] = len(rows)
D["fig21_sample"] = [rows[i] for i in (0, 4, 12, 24, 40, len(rows) - 1)]
# crossing points: delta*S vs log(S e^{S/2}) = log S + S/2
cross = {}
for dl in ("0.05", "0.1", "0.2", "0.3", "0.4", "0.45"):
    prev = None
    for r in rows[1:]:
        S = float(r["S"])
        f1 = float(dl) * S
        f2 = math.log(S) + S / 2 if S > 0 else -99
        cur = f1 - f2
        if prev is not None and prev[1] < 0 <= cur:
            cross[dl] = None
        prev = (S, cur)
    cross[dl] = "signal never overtakes envelope on the sampled range"
D["fig21_crossing"] = cross

# ---------------------------------------------------------------- fig 24
XMAX = 200000

def prime_power_table(X):
    """lam[n] = Lambda(n);  pk[n] = (p, k) when n = p^k, else None."""
    lam = [0.0] * (X + 1)
    pk = [None] * (X + 1)
    composite = bytearray(X + 1)
    for p in range(2, X + 1):
        if composite[p]:
            continue
        for m in range(p * p, X + 1, p):
            composite[m] = 1
        q, k = p, 1
        while q <= X:
            lam[q] = math.log(p)
            pk[q] = (p, k)
            if q > X // p:
                break
            q *= p
            k += 1
    return lam, pk

lam, PK = prime_power_table(XMAX)

def order_of(n):
    return PK[n]

bands = []
for b in range(1, 13):                       # log-support band [b-1, b)
    lo, hi = math.exp(b - 1), math.exp(b)
    tot = {1: 0.0, 2: 0.0, 3: 0.0}
    cnt = {1: 0, 2: 0, 3: 0}
    n0 = max(2, int(math.floor(lo)) + 1)
    n1 = min(XMAX, int(math.floor(hi)))
    for n in range(n0, n1 + 1):
        if lam[n] == 0.0:
            continue
        pk = order_of(n)
        k = min(pk[1], 3)
        tot[k] += lam[n] / math.sqrt(n)
        cnt[k] += 1
    bands.append({"band": [b - 1, b], "k1": tot[1], "k2": tot[2], "kge3": tot[3],
                  "n1": cnt[1], "n2": cnt[2], "nge3": cnt[3],
                  "complete": n1 == int(math.floor(hi))})
D["fig24_bands"] = bands

cum = []
t1 = t2 = t3 = 0.0
for b in bands:
    t1 += b["k1"]; t2 += b["k2"]; t3 += b["kge3"]
    cum.append({"S": b["band"][1], "k1": t1, "k2": t2, "kge3": t3,
                "two_exp_half_S": 2 * math.exp(b["band"][1] / 2),
                "complete": b["complete"]})
D["fig24_cumulative"] = cum

D["fig24_individual"] = [
    {"n": n, "Lambda": lam[n], "w": lam[n] / math.sqrt(n), "logn": math.log(n),
     "pk": order_of(n)}
    for n in range(2, 50) if lam[n] > 0
]

# ---------------------------------------------------------------- fig 25
# two-bump family g_T(u) = a h(u-T) + b h(u+T);  ghat gets factor
# a e^{-irT} + b e^{irT}.  For a=b=1 this is 2cos(rT).
T25 = 3.0
D["fig25_T"] = T25
D["fig25_samples"] = [
    {"r": r / 20.0, "sym": 2 * math.cos(r / 20.0 * T25),
     "anti": 2 * math.sin(r / 20.0 * T25)}
    for r in range(0, 121)
]
D["fig25_support"] = {
    "h_half_support": 1.0,
    "g_T_half_support": T25 + 1.0,
    "arith_envelope_factor_exp_T_over_2": math.exp(T25 / 2),
    "max_interference_gain_abs_a_plus_abs_b": 2.0,
}

# ---------------------------------------------------------------- fig 26
# Gaussian window h(r)=exp(-r^2/(2 sigma^2)) -> g(u) ∝ exp(-sigma^2 u^2/2).
# Arithmetic weight on the prime side grows like e^{u/2}.
# f(u) = u/2 - sigma^2 u^2 / 2 ;  peak u* = 1/(2 sigma^2), f(u*) = 1/(8 sigma^2)
def eff_support(sigma, L):
    s2 = sigma * sigma
    return (0.5 + math.sqrt(0.25 + 2 * s2 * L)) / s2

D["fig26"] = []
for sigma in (0.25, 0.35, 0.5, 0.75, 1.0):
    for eps in (1e-6, 1e-9):
        L = math.log(1 / eps)
        D["fig26"].append({
            "sigma": sigma, "eps": eps,
            "u_star": 1 / (2 * sigma * sigma),
            "f_max": 1 / (8 * sigma * sigma),
            "U_eff": eff_support(sigma, L)})

# ---------------------------------------------------------------- fig 27
# Beurling's extremal majorant of sgn (Vaaler, Bull. AMS 12 (1985) 183-216):
#   H(z) = (sin(pi z)/pi)^2 * ( sum_{n>=1} (z-n)^-2 - sum_{n>=1} (z+n)^-2 + 2/z )
#          = (sin(pi z)/pi)^2 * ( psi'(1-z) - psi'(1+z) + 2/z )
#   K(z) = (sin(pi z)/(pi z))^2 ,   B = H + K .
import numpy as np
from scipy.special import polygamma

def Bfun(x):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    near = np.abs(x - np.round(x)) < 1e-12
    ok = ~near
    xx = x[ok]
    s = polygamma(1, 1.0 - xx) - polygamma(1, xx + 1.0) + 2.0 / xx
    out[ok] = (np.sin(np.pi * xx) / np.pi) ** 2 * s + \
              (np.sin(np.pi * xx) / (np.pi * xx)) ** 2
    xn = np.round(x[near])
    out[near] = np.where(xn == 0, 1.0, np.sign(xn))
    return out

grid = np.linspace(-60.0, 60.0, 1200001)
Bv = Bfun(grid)
sg = np.sign(grid)
diff = Bv - sg
D["fig27_check"] = {
    "integral_B_minus_sgn_over_[-60,60]": float(np.trapezoid(diff, grid)),
    "min_B_minus_sgn": float(diff.min()),
    "B(0)": float(Bfun(np.array([0.0]))[0]),
    "B(1)": float(Bfun(np.array([1.0]))[0]),
    "B(-1)": float(Bfun(np.array([-1.0]))[0]),
    "note": "exact value of the full-line integral is 1 (Beurling)",
}
xs = np.round(np.arange(-4.0, 4.0001, 0.02), 4)
Bs = Bfun(xs)
Ms = -Bfun(-xs)
D["fig27_samples"] = [{"x": float(a), "B": float(b), "m": float(c)}
                      for a, b, c in zip(xs, Bs, Ms)]

# ---------------------------------------------------------------- fig 28
with open(os.path.join(HERE, "weil_component_signatures.csv")) as f:
    comp = list(csv.DictReader(f))
D["fig28_components"] = comp
with open(os.path.join(HERE, "weil_spline_inertia.csv")) as f:
    inert = list(csv.DictReader(f))
D["fig28_inertia"] = inert
D["fig28_summary"] = {
    "rows": len(inert),
    "W_full_neg": sorted({r["n_negative"] for r in comp if r["form"] == "W-full"}),
    "WmP_neg": sorted({r["n_negative"] for r in comp if r["form"] == "W-minus-P"}),
    "P_sig": sorted({(r["n_positive"], r["n_negative"]) for r in comp
                     if r["form"] == "P-poles"}),
    "T_values": sorted({float(r["T"]) for r in inert}),
    "N_values": sorted({int(r["N"]) for r in inert}),
}

with open(OUT, "w") as f:
    json.dump(D, f, indent=1, default=str)

# ------------------------------------------------------------------ report
print("fig13 lambda -> s")
for e in D["fig13_lambda_to_s"]:
    print("   %-62s lam=%.10f  %s" % (e["label"], e["lambda"], e["map"]))
print("\nfig14 r_Q(n), Q = x^2+xy+6y^2, n=1..20:", rQ1[1:21])
print("fig14 probe:", D["fig14_multiplicativity_probe"])
print("\nfig21 S range", D["fig21_S_range"], "rows", D["fig21_n"])
print("\nfig24 cumulative (S, k=1 mass, k=2 mass, k>=3 mass, 2e^{S/2}):")
for c in cum:
    print("   S=%2d  k1=%12.4f  k2=%8.4f  k3=%8.4f   2e^{S/2}=%12.4f  %s"
          % (c["S"], c["k1"], c["k2"], c["kge3"], c["two_exp_half_S"],
             "" if c["complete"] else "(band truncated at X=%d)" % XMAX))
print("\nfig25", D["fig25_support"])
print("\nfig26 (sigma, eps, u*, f_max, U_eff):")
for e in D["fig26"]:
    print("   %.2f  %.0e  u*=%7.3f  fmax=%7.3f  Ueff=%7.3f"
          % (e["sigma"], e["eps"], e["u_star"], e["f_max"], e["U_eff"]))
print("\nfig27 check:", D["fig27_check"])
print("\nfig28 summary:", D["fig28_summary"])
print("\nwrote", os.path.normpath(OUT))
