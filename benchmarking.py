import time, numpy as np, symengine as se

def _parse(s):
    n=[]; a=[]; b=[]; c=[]
    for blk in s.split(";"):
        if blk.strip():
            x,y,z,w=[t.strip() for t in blk.split(",")]
            n.append(x); a.append(float(y)); b.append(float(z)); c.append(int(w))
    return n,a,b,c

def _cap(cnt, L=10**7):
    if int(np.prod(cnt))<=L: return cnt
    s=(L/np.prod(cnt))**(1.0/len(cnt))
    cnt=[max(1,int(c*s)) for c in cnt]
    while int(np.prod(cnt))>L:
        i=cnt.index(max(cnt)); cnt[i]=max(1,cnt[i]-1)
    return cnt

def bench_blocks(expr_s, blocks_s, reps_s="1", limit_s="2"):
    e=se.sympify(expr_s)
    names,starts,steps,counts=_parse(blocks_s)
    counts=_cap([int(c) for c in counts])
    syms=[se.Symbol(n) for n in names]
    try: g=se.lambdify(syms,[e],"numpy")
    except Exception: g=se.lambdify(syms,[e])
    f=lambda *a: g(*a)[0]
    axes=[s+u*np.arange(k) for s,u,k in zip(starts,steps,counts)]
    grids=np.meshgrid(*axes, indexing="ij")
    ts=[]; reps=int(reps_s)
    for _ in range(reps):
        t0=time.perf_counter(); _=f(*grids); t1=time.perf_counter(); ts.append(t1-t0)
    dt=min(ts); n=int(np.prod(counts))
    return {"n":n,"ms":dt*1e3,"evals_per_s":n/max(dt,1e-12)}


def bench_blocks_subs(expr_s, blocks_s, reps_s="1", limit_s="2"):
    e = se.sympify(expr_s)
    names, starts, steps, counts = _parse(blocks_s)
    counts = _cap([int(c) for c in counts])
    syms = [se.Symbol(n) for n in names]

    reps = int(reps_s)
    shape = tuple(counts)
    ts = []
    best_dt = float("inf")
    best = None

    for _ in range(reps):
        t0 = time.perf_counter()
        res = np.empty(shape, dtype=object)
        for idx in np.ndindex(*counts):
            sub = {syms[i]: starts[i] + steps[i] * idx[i] for i in range(len(syms))}
            res[idx] = e.subs(sub).n()
        dt = time.perf_counter() - t0
        ts.append(dt)
        if dt < best_dt:
            best_dt = dt
            best = res

    flat = best.ravel()
    values = (flat[0], flat[1] if flat.size > 1 else None, flat[-1])
    return best, min(ts) * 1e3, values


def bench_blocks_py(expr_s, blocks_s, reps_s="1", limit_s="2"):
    code = compile(expr_s, "<expr>", "eval")
    names, starts, steps, counts = _parse(blocks_s)
    counts = _cap([int(c) for c in counts])

    axes = [s + u * np.arange(k) for s, u, k in zip(starts, steps, counts)]
    grids = np.meshgrid(*axes, indexing="ij")
    env = dict(np.__dict__); [env.__setitem__(k, v) for k, v in zip(names, grids)]

    reps = int(reps_s)
    ts = []
    best_dt = float("inf")
    best = None
    target = tuple(counts)
    n = int(np.prod(counts))

    for _ in range(reps):
        t0 = time.perf_counter()
        val = eval(code, env, {})
        dt = time.perf_counter() - t0
        ts.append(dt)

        arr = np.asarray(val)
        if arr.shape == ():
            arr = np.full(target, arr.item())
        elif arr.shape == target:
            arr = arr
        elif arr.size == n:
            arr = arr.reshape(target)
        else:
            arr = np.resize(arr, n).reshape(target)

        if dt < best_dt:
            best_dt = dt
            best = arr

    flat = best.ravel()
    values = (flat[0], flat[1] if flat.size > 1 else None, flat[-1])
    return best, min(ts) * 1e3, values



#print(bench_blocks_py("x**9+x**8+x**7+x**6+x**5+x**4+(1.0000001)**x", "x,0,0.001,1000000"))