# Ring loading: an exact instance with additive gap 47/42 > 11/10

**Ring Loading Problem.** Demands on a cycle must each be routed along one of the two arcs. L is the best maximum edge load of such an unsplittable routing, L\* is the best load when demands may be split, and D is the largest demand. The question is the smallest α with L ≤ L\* + αD for all instances.

Known bounds:
- Schrijver, Seymour and Winkler [SSW98] proved 1.01 ≤ α ≤ 1.5.
- Skutella [Sku16] proved 1.1 ≤ α ≤ 19/14 and conjectured **α = 11/10**.
- Däubel [Däu19] proved α ≤ 13/10.

This repository gives an exact certificate that

    α ≥ 47/42 = 1.1190476…

so Skutella's conjecture α = 11/10 does not hold. The window becomes [47/42, 13/10].

## Credit

The construction is AlphaEvolve's. Georgiev, Gómez-Serrano, Tao and Wagner [GGTW25, Problem 6.61] report a 15-number instance of the Schrijver–Seymour–Winkler discrepancy problem with score about 1.119. That paper compares it with Skutella's bounds. It does not mention Skutella's conjecture, Däubel's 13/10, or the resulting gap L − L\*. A June 2026 paper [AS26] still quotes 1.1 as the lower bound.

What this repository adds:
1. **A rational version of the AlphaEvolve construction with value exactly 47/42.** Four entries move by about 0.017; the floating-point original scores 1.11904757.
2. **An exact check**, with the additive performance defined as in [Sku16].
3. **The connection to the conjecture** through Däubel's Lemma 7, together with the explicit ring instance that the lemma produces.

## The instance

m = 15 crossing demands, D = 1, flows uᵢ clockwise and vᵢ counterclockwise:

    u = (25/28, 3/7, 1/2, 1/3, 11/42, 9/28, 31/42, 1/2, 1/7, 19/28, 5/21, 2/3, 17/42, 4/7, 5/84)
    v = u in reverse order

For a rounding z with zᵢ ∈ {vᵢ, −uᵢ}, the additive performance [Sku16] is max over k = 1..m of |Σ_{i≤k} zᵢ − Σ_{i>k} zᵢ|. The minimum over all 2¹⁵ roundings is exactly **47/42**; 38 roundings attain it. Dropping the term k = m, as the public AlphaEvolve scorer does, gives the same value.

By [Däu19, Lemma 7] (arXiv numbering), a split routing whose best rounding forces an increase αD yields a Ring Loading instance with L − L\* ≥ αD.

## Verify

Python 3 only; there are no dependencies. Everything runs in exact rational arithmetic.

    python3 verify_exact.py instance_47_42.json     # all 2^15 roundings, about 1 s
    python3 check_ring.py                           # the same value from a 30-node ring with explicit paths
    cd rlp_instance && python3 construct.py         # the explicit instance of Lemma 7

**`check_ring.py`** routes the demands on an actual 30-node ring. It confirms that the split routing has the stated loads and that every unsplittable routing raises some edge by at least 47/42.

**`rlp_instance/construct.py`** builds the instance of Lemma 7: 84 nodes and 123 demands (2 of them zero), with largest demand 1. It writes `instance.json` and checks the following.
- **L\* = 53/7:** the split routing has load 53/7 on every edge, and a 2-edge cut gives the matching lower bound.
- **The gadget property used in the proof of the lemma:** whatever way a gadget's own short demands are routed, some inner edge of that gadget carries at least its slack s_e. So every unsplittable routing has load at least 53/7 + 47/42.
- **L = 365/42:** routing every short demand along its short arc and the crossing demands by the best rounding achieves this, so L − L\* = 47/42 exactly.

Scaled by 84, the instance has D = 84, L\* = 636 and L = 730.

## Search

A local search (a witness LP from many random restarts, m = 15 to 17) never went above 47/42. This is evidence, not a proof, that 47/42 is the limit of this kind of construction.

## References

- [SSW98] A. Schrijver, P. Seymour, P. Winkler, *The ring loading problem*, SIAM J. Discrete Math. 11 (1998), 1–14.
- [Sku16] M. Skutella, *A note on the ring loading problem*, SIAM J. Discrete Math. 30 (2016), 327–342. arXiv:1405.0789.
- [Däu19] K. Däubel, *An improved upper bound for the ring loading problem*, arXiv:1904.02119; SIAM J. Discrete Math. (2022).
- [GGTW25] B. Georgiev, J. Gómez-Serrano, T. Tao, A. Z. Wagner, *Mathematical exploration and discovery at scale*, arXiv:2511.02864, Problem 6.61.
- [AS26] Alemán Espinosa, Schlomberg, *Pinning on tight cuts: improved algorithm and bounds for unsplittable multicommodity flows in outerplanar graphs*, arXiv:2606.04456.

## AI disclosure

The rational instance, the checks and this text were prepared with the help of an AI assistant (Claude, Anthropic). An independent AI agent that saw only the papers, not our code, re-derived the value 47/42 and the explicit instance. Every claim above is checked by the exact scripts in this repository.
