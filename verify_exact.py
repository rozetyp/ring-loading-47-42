#!/usr/bin/env python3
"""Exact checker for ring-loading discrepancy instances (pure Python, fractions only).

Instance: rationals u_i, v_i >= 0 with u_i + v_i <= 1 (demand d_i = u_i + v_i; D = max d_i).
For every unsplittable rounding z with z_i in {v_i, -u_i}, its additive performance (Skutella 2016) is
    perf(z) = max_{k=1..m} | sum_{i<=k} z_i - sum_{i>k} z_i |.
The instance certifies  alpha >= min_z perf(z) / D  (Schrijver-Seymour-Winkler / Skutella formulation; via
Daeubel 2019, Lemma 7, a ring loading instance with L - L* >= (min_z perf(z)) exists when D = 1).
Usage: python3 verify_exact.py instance.json
"""
import sys, json, itertools
from fractions import Fraction as F
d = json.load(open(sys.argv[1]))
u = [F(x) for x in d["u"]]; v = [F(x) for x in d["v"]]
m = len(u)
assert len(v) == m and all(x >= 0 for x in u + v) and all(a + b <= 1 for a, b in zip(u, v)), "invalid instance"
D = max(a + b for a, b in zip(u, v))
best = None; worst_z = None
for z in itertools.product(*[(vi, -ui) for ui, vi in zip(u, v)]):
    S = sum(z); pre = F(0); perf = F(0)
    for k in range(m):
        pre += z[k]
        perf = max(perf, abs(2 * pre - S))
    if best is None or perf < best:
        best, worst_z = perf, z
print(f"m = {m}, D = max demand = {D}")
print(f"min over all {2**m} roundings of additive performance = {best} = {float(best):.12f}")
print(f"normalised by D: {best / D} = {float(best / D):.12f}")
