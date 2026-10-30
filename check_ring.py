# Independent check: build the actual 30-node ring, route demands, compute edge loads directly from paths.
from fractions import Fraction as F
from itertools import product
u = [F(25,28),F(3,7),F(1,2),F(1,3),F(11,42),F(9,28),F(31,42),F(1,2),F(1,7),F(19,28),F(5,21),F(2,3),F(17,42),F(4,7),F(5,84)]
m=len(u); v=[u[m-1-i] for i in range(m)]
n=2*m
# nodes 0..n-1, edge e connects e and e+1 mod n. Demand i (0-based) from node i to node i+m.
def cw_edges(a,b):  # edges on clockwise path a->a+1->...->b
    out=[];x=a
    while x!=b: out.append(x); x=(x+1)%n
    return out
def ccw_edges(a,b): # edges on counterclockwise path a->a-1->...->b
    out=[];x=a
    while x!=b: out.append((x-1)%n); x=(x-1)%n
    return out
CW=[set(cw_edges(i,i+m)) for i in range(m)]
CCW=[set(ccw_edges(i,i+m)) for i in range(m)]
assert all(CW[i].isdisjoint(CCW[i]) and len(CW[i]|CCW[i])==n for i in range(m))
def loads(flow_cw, flow_ccw):
    L=[F(0)]*n
    for i in range(m):
        for e in CW[i]: L[e]+=flow_cw[i]
        for e in CCW[i]: L[e]+=flow_ccw[i]
    return L
base=loads(u,v)
print("split loads:",[str(x) for x in base]); lmax=max(base); print("lmax",lmax,"lmin",min(base),"spread",lmax-min(base))
d=[u[i]+v[i] for i in range(m)]
best=None
for bits in product((0,1),repeat=m):
    cw=[d[i] if b else F(0) for i,b in enumerate(bits)]
    ccw=[F(0) if b else d[i] for i,b in enumerate(bits)]
    Lz=loads(cw,ccw)
    inc=max(Lz[e]-base[e] for e in range(n))
    if best is None or inc<best: best=inc
print("min over unsplittable of max edge increase:",best,float(best))
