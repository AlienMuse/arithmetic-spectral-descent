"""
A2-gap-attack numerics.
=======================

Supports Appendix J (the A2-star analysis).

What is computed
----------------
(1) Lambda(n) for n <= X by a linear sieve.
(2) R_k(N) = sum_{n_1+...+n_k=N} Lambda(n_1)...Lambda(n_k)  for k = 2,3,4
    by FFT convolution, and the summatory function S_k(X) = sum_{N<=X} R_k(N).
(3) The level-1 ("rho-linear") term of the k-linear explicit formula,
        H_k(x) = -k * sum_rho x^{k-1+rho} / ( rho (1+rho) ... (k-1+rho) ),
    truncated at the first NZ nontrivial zeros (and their conjugates).
(4) The two normalised residuals

        D1_k(x) = ( S_k(x) - x^k/k! ) / x^{k-1/2}          (level-1 signal)
        D2_k(x) = ( S_k(x) - x^k/k! - H_k(x) ) / x^{k-1}   (level->=2 residual)

    The claim tested is Bhowmik-Schlage-Puchta, Corollary 1 (arXiv:1002.4806):
    D2_k(x) does NOT shrink as k grows -- i.e. amplification buys nothing.
(5) The exact archimedean constants of the fully diagonal level-2 term,
        sum_rho |Gamma(rho)|^2 = 2 pi sum_{gamma>0} sech(pi gamma)   (under RH)
        sum_rho |Gamma(rho)|    = 2 sqrt(pi) sum_{gamma>0} sech(pi gamma)^{1/2}
    which quantify the "amplification-amplitude trade-off".
(6) The abscissa ledger:  level j of Phi_k sits at Re s = (k-j) + j*Theta.

Outputs (written next to this script):
    A2_zeta_zeros_2000.csv
    A2_level_residuals.csv
    A2_abscissa_ledger.csv
    A2_archimedean_constants.json
"""

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NZ = 2000          # number of nontrivial zeros (positive ordinates) to use
XMAX = 1 << 17     # 131072


# ----------------------------------------------------------------------
# 1. von Mangoldt
# ----------------------------------------------------------------------
def von_mangoldt(n_max: int) -> np.ndarray:
    """Lam[n] = log p if n = p^a, else 0.  Index 0..n_max."""
    lam = np.zeros(n_max + 1, dtype=np.float64)
    spf = np.zeros(n_max + 1, dtype=np.int64)      # smallest prime factor
    primes = []
    for i in range(2, n_max + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n_max:
                break
            spf[i * p] = p
    for i in range(2, n_max + 1):
        p = spf[i]
        m = i
        while m % p == 0:
            m //= p
        if m == 1:
            lam[i] = math.log(p)
    return lam


# ----------------------------------------------------------------------
# 2. k-fold additive convolution by FFT
# ----------------------------------------------------------------------
def additive_power(lam: np.ndarray, k: int, n_max: int) -> np.ndarray:
    """R_k[N] for N = 0..n_max, via zero-padded real FFT."""
    size = 1
    while size < k * n_max + 2:
        size <<= 1
    f = np.zeros(size, dtype=np.float64)
    f[: len(lam)] = lam
    F = np.fft.rfft(f)
    G = np.fft.irfft(F ** k, n=size)
    return G[: n_max + 1]


# ----------------------------------------------------------------------
# 3. zeros of zeta
# ----------------------------------------------------------------------
def zeta_zeros(n: int) -> np.ndarray:
    """First n positive ordinates, cached to CSV."""
    path = os.path.join(HERE, "A2_zeta_zeros_2000.csv")
    if os.path.exists(path):
        arr = np.loadtxt(path, delimiter=",", skiprows=1, usecols=1)
        if len(arr) >= n:
            return arr[:n]
    import mpmath as mp

    mp.mp.dps = 25
    out = []
    for j in range(1, n + 1):
        out.append(float(mp.im(mp.zetazero(j))))
        if j % 200 == 0:
            print(f"    ... {j} zeros")
    arr = np.array(out)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("index,ordinate\n")
        for j, g in enumerate(arr, 1):
            fh.write(f"{j},{g:.15f}\n")
    return arr


def H_k(x: np.ndarray, k: int, gammas: np.ndarray) -> np.ndarray:
    """
    H_k(x) = -k sum_rho x^{k-1+rho} / (rho (1+rho) ... (k-1+rho)),
    rho = 1/2 + i gamma running over conjugate pairs (RH assumed for the model).
    Returned as a real array (the sum over rho and bar-rho is real).
    """
    rho = 0.5 + 1j * gammas                       # (NZ,)
    denom = np.ones_like(rho)
    for j in range(k):                            # rho (1+rho) ... (k-1+rho)
        denom = denom * (j + rho)
    logx = np.log(x)                              # (M,)
    # x^{k-1+rho} = x^{k-1/2} * exp(i gamma log x)
    pref = x ** (k - 0.5)                         # (M,)
    # sum over rho and conjugate = 2 * Re( sum_{gamma>0} e^{i gamma log x}/denom )
    S = np.zeros_like(x)
    chunk = 200
    for a in range(0, len(rho), chunk):
        g = gammas[a : a + chunk]
        d = denom[a : a + chunk]
        S += 2.0 * np.real(np.exp(1j * np.outer(logx, g)) @ (1.0 / d))
    return -k * pref * S


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main() -> None:
    print(f"[1] von Mangoldt up to {XMAX} ...")
    lam = von_mangoldt(XMAX)

    print("[2] zeros of zeta ...")
    gammas = zeta_zeros(NZ)
    print(f"    gamma_1 = {gammas[0]:.6f},  gamma_{NZ} = {gammas[-1]:.4f}")

    # sample points, geometric, in the upper half of the range
    xs = np.unique(np.round(np.geomspace(2000, XMAX, 60)).astype(np.int64))

    rows = []
    for k in (2, 3, 4):
        print(f"[3] k = {k}: additive {k}-fold convolution ...")
        Rk = additive_power(lam, k, XMAX)
        Sk = np.cumsum(Rk)
        kfact = math.factorial(k)
        Sx = Sk[xs].astype(np.float64)
        main_term = xs.astype(np.float64) ** k / kfact
        Hx = H_k(xs.astype(np.float64), k, gammas)

        D1 = (Sx - main_term) / xs.astype(np.float64) ** (k - 0.5)
        D2 = (Sx - main_term - Hx) / xs.astype(np.float64) ** (k - 1.0)
        for x, d1, d2 in zip(xs, D1, D2):
            rows.append((k, int(x), float(d1), float(d2)))
        print(f"    max |D1_k| = {np.max(np.abs(D1)):.4f}   "
              f"rms D1 = {np.sqrt(np.mean(D1**2)):.4f}")
        print(f"    max |D2_k| = {np.max(np.abs(D2)):.4f}   "
              f"rms D2 = {np.sqrt(np.mean(D2**2)):.4f}")
        # Predicted x^{k-1} coefficient: residue of Phi_k(s) X^s / s at s = k-1,
        # coming from the (level 0, one E_0-factor) term of the k-linear formula:
        #     Res_{s=k-1} Gamma(s) Phi_k(s) = -k log(2 pi) + binom(k,2) sum_rho|Gamma(rho)|^2
        # hence the coefficient of X^{k-1} is  -k log(2pi) / ((k-1) Gamma(k-1)).
        pred = -k * math.log(2 * math.pi) / ((k - 1) * math.gamma(k - 1))
        print(f"    predicted x^(k-1) coefficient = {pred:+.4f} "
              f"  (observed mean D2 = {np.mean(D2):+.4f})")
        # log-log slope of |D2|: ~0 confirms Delta_k(x) asymp x^{k-1} for every k
        slope = np.polyfit(np.log(xs.astype(float)),
                           np.log(np.abs(D2) + 1e-300), 1)[0]
        print(f"    d log|D2| / d log x = {slope:+.4f}   "
              f"(0 == 'error term does NOT improve with k')")

    path = os.path.join(HERE, "A2_level_residuals.csv")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("k,x,D1_level1_normalised,D2_level2_normalised\n")
        for k, x, d1, d2 in rows:
            fh.write(f"{k},{x},{d1:.8e},{d2:.8e}\n")
    print(f"    wrote {path}")

    # ---- archimedean constants -------------------------------------
    #  |Gamma(1/2 + i t)|^2 = pi / cosh(pi t)   (exact)
    with np.errstate(over="ignore"):
        sech = 1.0 / np.cosh(math.pi * gammas)
    c2 = 2.0 * math.pi * float(np.sum(sech))                 # sum_rho |Gamma(rho)|^2
    c1 = 2.0 * math.sqrt(math.pi) * float(np.sum(np.sqrt(sech)))  # sum_rho |Gamma(rho)|
    consts = {
        "gamma_1": float(gammas[0]),
        "sum_rho_abs_Gamma_rho": c1,
        "sum_rho_abs_Gamma_rho_squared": c2,
        "comment": ("Under RH, |Gamma(1/2+i gamma)|^2 = pi sech(pi gamma) exactly; "
                    "these are the amplitudes of the fully diagonal level-2 term "
                    "and of the level-1 term in the LAPLACE form of the k-linear "
                    "explicit formula. Their minuteness is the amplification-"
                    "amplitude trade-off: each extra level costs a factor "
                    "~ e^{-pi gamma_1 / 2} = %.3e." % math.exp(-math.pi * gammas[0] / 2)),
        "cost_per_level_exp_factor": math.exp(-math.pi * float(gammas[0]) / 2),
    }
    path = os.path.join(HERE, "A2_archimedean_constants.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(consts, fh, indent=2)
    print(f"    wrote {path}")
    print(f"    sum_rho |Gamma(rho)|   = {c1:.6e}")
    print(f"    sum_rho |Gamma(rho)|^2 = {c2:.6e}")

    # ---- abscissa ledger -------------------------------------------
    path = os.path.join(HERE, "A2_abscissa_ledger.csv")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("k,level_j,abscissa_unnormalised,abscissa_normalised_RH,"
                 "abscissa_normalised_offline_delta\n")
        for k in range(2, 13):
            for j in range(0, k + 1):
                unnorm = f"({k-j}) + {j}*Theta"
                norm_rh = (k - j) + j * 0.5 - (k - 1) / 2.0
                norm_off = f"{(k - j) + j*0.5 - (k-1)/2.0:.2f} + {j}*delta"
                fh.write(f"{k},{j},{unnorm},{norm_rh:.4f},{norm_off}\n")
    print(f"    wrote {path}")

    print("\n[4] EXACT CRITICALITY CHECK (algebraic identity)")
    print("    constraint at level j*:  1/2 + k*delta  <=  (k-j*) + j*Theta - (k-1)/2")
    for k in (2, 3, 5, 10, 50):
        for js in (0, 1, 2, k - 1, k):
            if js < 0 or js > k:
                continue
            # solve for delta: (k - js) delta <= (k - js)/2
            print(f"      k={k:3d} j*={js:3d}  =>  delta <= "
                  f"{'1/2 (TRIVIAL)' if js < k else 'vacuous 0<=0'}")
    print("\ndone.")


if __name__ == "__main__":
    main()
