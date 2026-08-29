#!/usr/bin/env python3
"""Helmholtz B at center and along the axis. SI units."""
from __future__ import annotations

import argparse
import math

MU0 = 4 * math.pi * 1e-7


def loop_bz(R: float, I: float, z: float) -> float:
    return MU0 * I * R**2 / (2 * (R**2 + z**2) ** 1.5)


def pair(radius_cm: float, turns: float, current: float, z_cm: float = 0.0) -> dict:
    R = radius_cm / 100
    z = z_cm / 100
    b = turns * (loop_bz(R, current, z - R / 2) + loop_bz(R, current, z + R / 2))
    k = 8 / (5**1.5)
    center = (k * MU0 * turns * current) / R if R else 0
    return {"B_mT": b * 1000, "B_T": b, "center_T": center, "z_cm": z_cm}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--r", type=float, default=7, help="radius cm")
    p.add_argument("--n", type=float, default=140)
    p.add_argument("--i", type=float, default=1.2)
    p.add_argument("--z", type=float, default=0)
    p.add_argument("--scan", action="store_true")
    a = p.parse_args()
    if a.scan:
        for z in [i * a.r / 10 for i in range(-10, 11)]:
            o = pair(a.r, a.n, a.i, z)
            print(f"z={z:6.2f} cm   B={o['B_mT']:.4f} mT")
    else:
        o = pair(a.r, a.n, a.i, a.z)
        print(f"B = {o['B_mT']:.4f} mT  ({o['B_T']:.6e} T)")


if __name__ == "__main__":
    main()
