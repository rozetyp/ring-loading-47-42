# Ring loading: explicit instances with additive gap 47/42 and 9/8

> **Update (5 Nov 2026).** We had missed earlier work on the AlphaEvolve problems repository, which predates our 30 Oct post; see Credit below. The best known lower bound is 9/8 (Maks23, issue #12). At K. Däubel's suggestion ([RingLoading#1](https://github.com/karldaeubel/RingLoading/issues/1)), `rlp_instance/construct.py` now takes any instance, and `rlp_instance/solve_L.py` computes L of the resulting Ring Loading instance directly, without using Lemma 7. Both 9/8 certificates give instances with L − L\* = 9/8 D exactly.

**Ring Loading Problem.** Demands on a cycle must each be routed along one of the two arcs. L is the best maximum edge load of such an unsplittable routing, L\* is the best load when demands may be split, and D is the largest demand. The question is the smallest α with L ≤ L\* + αD for all instances.

Known bounds:
- Schrijver, Seymour and Winkler [SSW98] proved 1.01 ≤ α ≤ 1.5.
- Skutella [Sku16] proved 1.1 ≤ α ≤ 19/14 and conjectured **α = 11/10**.
- Däubel [Däu19] proved α ≤ 13/10.
- AlphaEvolve [GGTW25, Problem 6.61] found a discrepancy instance with value about 1.119.
- Maks23 [AE12] gave an exact instance with value **9/8**.

So Skutella's conjecture α = 11/10 does not hold, and the window is [9/8, 13/10]. This repository gives explicit Ring Loading instances with L − L\* = 47/42 D and 9/8 D, with L computed directly.

## Credit

The construction is AlphaEvolve's [GGTW25, Problem 6.61]. V. Yadav posted an exact rational 47/42 version [AE11] on 6 Oct 2026. Maks23 improved the bound to 9/8 [AE12] on 8 Oct. On 13 Oct, K. Däubel gave a 12-demand 9/8 instance in the same thread, and noted that Lemma 7 of [Däu19] turns these certificates into Ring Loading instances. We found this work only after posting on 30 Oct.

What this repository adds:
1. **A different, symmetric rational 47/42 instance** (below).
2. **Explicit Lemma 7 Ring Loading instances**, for it and for both 9/8 certificates:
   - L\* is checked exactly;
   - L is computed directly by two solvers.

## The instance

m = 15 crossing demands, D = 1, flows uᵢ clockwise and vᵢ counterclockwise:

    u = (25/28, 3/7, 1/2, 1/3, 11/42, 9/28, 31/42, 1/2, 1/7, 19/28, 5/21, 2/3, 17/42, 4/7, 5/84)
    v = u in reverse order

For a rounding z with zᵢ ∈ {vᵢ, −uᵢ}, the additive performance [Sku16] is max over k = 1..m of |Σ_{i≤k} zᵢ − Σ_{i>k} zᵢ|. The minimum over all 2¹⁵ roundings is exactly **47/42**; 38 roundings attain it. Dropping the term k = m, as the public AlphaEvolve scorer does, gives the same value.

By [Däu19, Lemma 7] (arXiv numbering), a split routing whose best rounding forces an increase αD yields a Ring Loading instance with L − L\* ≥ αD.

## Verify

Everything except `solve_L.py` is Python 3 only, with no dependencies, and runs in exact rational arithmetic.

    python3 verify_exact.py instances/instance_47_42.json     # all 2^15 roundings, about 1 s
    python3 check_ring.py                           # the same value from a 30-node ring with explicit paths
    cd rlp_instance && python3 construct.py         # the explicit instance of Lemma 7
    python3 construct.py ../instances/instance_9_8_m12.json instance_9_8_m12.json   # the same for 9/8, 12 demands
    python3 construct.py ../instances/instance_9_8_m14.json instance_9_8_m14.json   # the same for 9/8, 14 demands
    python3 ../verify_exact.py ../instances/instance_9_8_m12.json   # the discrepancy value 9/8
    python3 solve_L.py instance_9_8_m12.json        # L computed directly (needs ortools, numpy, scipy); a few seconds

**`rlp_instance/solve_L.py`** computes L of an instance written by `construct.py` without using Lemma 7. The demands are scaled to integers, so L is an integer. CP-SAT (exact integer arithmetic) minimises the maximum edge load and proves optimality, and is then run again with the load capped at L − 1, which must be infeasible. HiGHS solves the same model as a second solver. L\* is taken from `construct.py` (split routing and 2-edge cut, exact). The upper bound on L is an explicit routing checked in exact arithmetic; the lower bound is CP-SAT infeasibility at L − 1, confirmed by HiGHS.

**`check_ring.py`** routes the demands on an actual 30-node ring. It confirms that the split routing has the stated loads and that every unsplittable routing raises some edge by at least 47/42.

**`rlp_instance/construct.py`** builds the instance of Lemma 7: 84 nodes and 123 demands (4 of them zero), with largest demand 1. It writes `instance.json` and checks the following.
- **L\* = 53/7:** the split routing has load 53/7 on every edge, and a 2-edge cut gives the matching lower bound.
- **The gadget property used in the proof of the lemma:** whatever way a gadget's own short demands are routed, some inner edge of that gadget carries at least its slack s_e. So every unsplittable routing has load at least 53/7 + 47/42.
- **L = 365/42:** routing every short demand along its short arc and the crossing demands by the best rounding achieves this, so L − L\* = 47/42 exactly.

Scaled by 42, the instance has D = 42, L\* = 318 and L = 365.

**The 9/8 instances.** For the two 9/8 certificates of [AE12] (in `instances/`), `construct.py` runs the same checks and `solve_L.py` gives L directly:

| certificate | ring | demands | L\* | L (CP-SAT and HiGHS) | L − L\* | scaled by 8 (D = 8) |
|---|---|---|---|---|---|---|
| 12 demands (Däubel) | 48 nodes | 60 (8 zero) | 45/8 | 27/4 | 9/8 | L\* = 45, L = 54 |
| 14 demands (Maks23, issue #12) | 64 nodes | 86 (8 zero) | 53/8 | 31/4 | 9/8 | L\* = 53, L = 62 |

Since L is computed on the ring itself, these gaps do not depend on which range of k the discrepancy score uses (a question left open in issue #12). On the 47/42 instance, `solve_L.py` gives L = 365/42 as well, agreeing with the argument above.

## Search

Our local search (a witness LP from many random restarts, m = 15 to 17) never went above 47/42. The 9/8 instances above show that this was a limit of our search.

## References

- [SSW98] A. Schrijver, P. Seymour, P. Winkler, *The ring loading problem*, SIAM J. Discrete Math. 11 (1998), 1–14.
- [Sku16] M. Skutella, *A note on the ring loading problem*, SIAM J. Discrete Math. 30 (2016), 327–342. arXiv:1405.0789.
- [Däu19] K. Däubel, *An improved upper bound for the ring loading problem*, arXiv:1904.02119; SIAM J. Discrete Math. (2022).
- [GGTW25] B. Georgiev, J. Gómez-Serrano, T. Tao, A. Z. Wagner, *Mathematical exploration and discovery at scale*, arXiv:2511.02864, Problem 6.61.
- [AE11] V. Yadav, *Problem 61 (ring loading): exact rational instance with alpha = 47/42*, google-deepmind/alphaevolve_repository_of_problems issue #11, 6 Oct 2026.
- [AE12] Maks23, *Problem 61 (Ring Loading): new lower bound C ≥ 9/8, exact certificate with m = 14*, issue #12, 8 Oct 2026, with the 12-demand instance of K. Däubel (13 Oct 2026).

## AI disclosure

The rational instance, the checks and this text were prepared with the help of an AI assistant (Claude, Anthropic). An independent AI agent that saw only the papers, not our code, re-derived the value 47/42 and the explicit instance. Every claim above is checked by the exact scripts in this repository.
