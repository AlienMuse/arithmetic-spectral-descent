"""Numerical Li coefficients and ordinary Turan differences.

We use the generating function

    log xi(1/(1-z)) = log xi(1) + sum_{n>=1} lambda_n z^n/n

and extract Taylor coefficients by a Cauchy/FFT calculation on |z|=0.65.
The output is numerical evidence only, not a positivity certificate.
"""

from __future__ import annotations

import csv
from pathlib import Path

import mpmath as mp
import numpy as np


OUT = Path(__file__).resolve().parent / "li_coefficients_logconcavity.csv"


def xi(s: mp.mpc) -> mp.mpc:
    return (
        mp.mpf("0.5")
        * s
        * (s - 1)
        * mp.power(mp.pi, -s / 2)
        * mp.gamma(s / 2)
        * mp.zeta(s)
    )


def main(count: int = 50, samples: int = 512, radius: float = 0.65) -> None:
    mp.mp.dps = 60
    boundary = []
    for k in range(samples):
        z = mp.mpf(radius) * mp.e ** (2j * mp.pi * k / samples)
        boundary.append(complex(mp.log(xi(1 / (1 - z)))))

    values = np.asarray(boundary)
    values = values.real + 1j * np.unwrap(values.imag)
    coefficients = np.fft.fft(values) / samples
    li = [
        float((n * coefficients[n] / radius**n).real)
        for n in range(1, count + 1)
    ]

    rows = []
    for n, value in enumerate(li, start=1):
        turan = ""
        if 1 < n < count:
            turan = value * value - li[n - 2] * li[n]
        rows.append({"n": n, "lambda_n": value, "turan_difference": turan})

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
