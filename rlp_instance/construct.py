# Build the RLP instance per Daubel Lemma 7 (step 1: subdivide every edge & add short demands; step 2: split short demands > D)
from fractions import Fraction as F
from itertools import product
import json
u = [F(25,28),F(3,7),F(1,2),F(1,3),F(11,42),F(9,28),F(31,42),F(1,2),F(1,7),F(19,28),F(5,21),F(2,3),F(17,42),F(4,7),F(5,84)]
m=len(u); v=[u[m-1-i] for i in range(m)]; n0=2*m; Dm=F(1)
d=[u[i]+v[i] for i in range(m)]
# split loads on original ring: edge e = (e,e+1)
def onCW(i,e): # is edge e on clockwise path i -> i+m ?
    return (e - i) % n0 < m
l=[sum((u[i] if onCW(i,e) else v[i]) for i in range(m)) for e in range(n0)]
lmax=max(l)
# new ring: list of nodes; record original node positions
nodes=[]; orig_pos={}; demands=[]  # demands: (a_pos, b_pos, value, kind, short_dir_cw_from_a) ; positions later
gadgets=[]
for e in range(n0):
    p=len(nodes); nodes.append(('orig',e)); orig_pos[e]=p
    s=lmax-l[e]
    if s<=Dm:
        h=len(nodes); nodes.append(('h',e))
        gadgets.append((e,'S1',s,[('p','h',s),('h','q',s)],p))
    else:
        t=s-Dm
        a=len(nodes); nodes.append(('a',e)); h=len(nodes); nodes.append(('h',e)); b=len(nodes); nodes.append(('b',e))
        gadgets.append((e,'S2',s,[('p','h',Dm),('h','q',Dm),('p','a',t),('a','h',t),('h','b',t),('b','q',t)],p))
N=len(nodes)
# resolve gadget node names to positions; q = next original node
dem=[]  # (a,b,val,splitcw) with a->b clockwise being the 'short'/u-direction
for (e,kind,s,ds,p) in gadgets:
    q=orig_pos.get((e+1)%n0, None)
    if q is None: q=0 if (e+1)%n0==0 else None
    names={'p':p}
    if kind=='S1': names.update(h=p+1)
    else: names.update(a=p+1,h=p+2,b=p+3)
    names['q']= (p+ (2 if kind=='S1' else 4)) % N
    for (x,y,val) in ds:
        dem.append(dict(a=names[x],b=names[y],val=val,kind='short',gadget=e,ucw=val,vccw=F(0)))
for i in range(m):
    dem.append(dict(a=orig_pos[i],b=orig_pos[i+m],val=d[i],kind='cross',idx=i,ucw=u[i],vccw=v[i]))
def cw_edges(a,b):
    out=[];x=a
    while x!=b: out.append(x); x=(x+1)%N
    return out
for dd in dem:
    cw=set(cw_edges(dd['a'],dd['b'])); dd['cw']=cw; dd['ccw']=set(range(N))-cw
print("N nodes",N,"#demands",len(dem),"#short",sum(1 for x in dem if x['kind']=='short'),"max demand",max(x['val'] for x in dem))
print("#gadgets with s>1:",sum(1 for g in gadgets if g[1]=='S2'), " max s",max(g[2] for g in gadgets), " #zero s", sum(1 for g in gadgets if g[2]==0))
# load of given split routing
L0=[F(0)]*N
for dd in dem:
    for e in dd['cw']: L0[e]+=dd['ucw']
    for e in dd['ccw']: L0[e]+=dd['vccw']
print("split routing loads all equal lmax?", set(L0)=={lmax}, "lmax=",lmax)
# exact 2-edge cut lower bound on L*
best=F(0)
for e1 in range(N):
    for e2 in range(e1+1,N):
        sep=F(0)
        for dd in dem:
            if (e1 in dd['cw']) != (e2 in dd['cw']): sep+=dd['val']
        if sep/2>best: best=sep/2
print("2-edge cut lower bound on L*:",best, float(best), " equals lmax?",best==lmax)
# gadget property check: in every configuration of a gadget's own demands, some internal edge gets >= s
ok=True
for (e,kind,s,ds,p) in gadgets:
    gd=[x for x in dem if x['kind']=='short' and x['gadget']==e]
    k=len(gd); ne=2 if kind=='S1' else 4
    internal=[(p+j)%N for j in range(ne)]
    for bits in product((0,1),repeat=k):
        g={f:F(0) for f in internal}
        for b,x in zip(bits,gd):
            path = x['cw'] if b else x['ccw']
            for f in internal:
                if f in path: g[f]+=x['val']
        if max(g.values())<s: ok=False; print("gadget fails",e,bits)
print("gadget property holds for all gadgets:",ok)
# min over 2^15 crossing routings of max_e (c(e)+s_e) with shorts short
crossd=[x for x in dem if x['kind']=='cross']
shortload=[F(0)]*N
for x in dem:
    if x['kind']=='short':
        for e in x['cw']: shortload[e]+=x['val']
bestL=None
for bits in product((0,1),repeat=m):
    Ld=shortload[:]
    for b,x in zip(bits,crossd):
        for e in (x['cw'] if b else x['ccw']): Ld[e]+=x['val']
    M=max(Ld)
    if bestL is None or M<bestL: bestL=M
print("L (all shorts short, best crossing) =",bestL," L - lmax =",bestL-lmax)
json.dump(dict(N=N,dem=[dict(a=x['a'],b=x['b'],val=str(x['val'])) for x in dem],lmax=str(lmax)),open('instance.json','w'))
