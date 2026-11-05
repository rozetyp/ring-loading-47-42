# Compute L, the optimal unsplittable load, of an instance written by construct.py, directly and without Lemma 7.
# Usage: python3 solve_L.py instance.json   (needs ortools, numpy and scipy)
# Data are scaled to integers, so L is an integer and both solvers decide it exactly:
#   1. CP-SAT (integer arithmetic) minimises the maximum edge load and proves optimality;
#   2. CP-SAT again with the maximum load forced to at most L - 1: must be infeasible;
#   3. HiGHS MILP (through scipy) on the same model, as a second solver.
import sys, json
from fractions import Fraction as F
from math import lcm
from ortools.sat.python import cp_model
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

inst = json.load(open(sys.argv[1]))
N = inst['N']; dem = [(d['a'], d['b'], F(d['val'])) for d in inst['dem']]; lmax = F(inst['lmax'])
S = lcm(*[x.denominator for _, _, x in dem], lmax.denominator)
val = [int(x * S) for _, _, x in dem]
def cw_edges(a, b):
    out = []; x = a
    while x != b: out.append(x); x = (x + 1) % N
    return out
cw = [set(cw_edges(a, b)) for a, b, _ in dem]
D = max(x for _, _, x in dem)
print(f"{sys.argv[1]}: {N} nodes, {len(dem)} demands, D = {D}, L* = {lmax}, scale {S}")

def cpsat(cap=None):
    m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{j}') for j in range(len(dem))]   # x = 1: clockwise
    T = m.NewIntVar(0, sum(val), 'T')
    for e in range(N):
        m.Add(sum(val[j] * x[j] if e in cw[j] else val[j] * (1 - x[j]) for j in range(len(dem))) <= T)
    if cap is not None: m.Add(T <= cap)
    else: m.Minimize(T)
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 600
    st = s.Solve(m)
    return s.StatusName(st), (int(s.Value(T)) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None), s

status, T, s = cpsat()
print(f"CP-SAT: {status}, L = {T}/{S} = {F(T, S)}, best bound {s.BestObjectiveBound()}")
assert status == 'OPTIMAL'
L = F(T, S)
status2, _, _ = cpsat(T - 1)
print(f"CP-SAT with max load <= {T - 1}: {status2}")

n = len(dem)   # x_j in {0,1}, T >= 0; per edge: sum_cw val x - sum_ccw val x - T <= -(ccw constant)
A = np.array([[val[j] if e in cw[j] else -val[j] for j in range(n)] + [-1] for e in range(N)], dtype=float)
ub = np.array([-sum(val[j] for j in range(n) if e not in cw[j]) for e in range(N)], dtype=float)
res = milp(c=np.r_[np.zeros(n), 1.0], constraints=LinearConstraint(A, -np.inf, ub),
           integrality=np.r_[np.ones(n), 0], bounds=Bounds(np.r_[np.zeros(n), 0], np.r_[np.ones(n), np.inf]),
           options=dict(mip_rel_gap=0))
hv = res.fun
print(f"HiGHS MILP (scipy): {res.message}, L = {hv:.6f}/{S} (rounded {round(hv)})")
print(f"L - L* = {L - lmax} = {(L - lmax) / D} D;  CP-SAT and HiGHS agree: {round(hv) == T};  "
      f"lower bound proved by CP-SAT: {status2 == 'INFEASIBLE'}")
