# Minimal resolution prover (small teaching example)
# - Literals: (pred, args_tuple, positive_bool)
# - Clause: frozenset of literals
# - Very small unifier (variables start lowercase). No standardization/occurs-check.

from itertools import combinations

def is_var(t): return isinstance(t, str) and t[0].islower()

def unify(t1, t2, subs):
    # apply existing subs
    t1 = subs.get(t1, t1)
    t2 = subs.get(t2, t2)
    if t1 == t2: return subs
    if is_var(t1):
        subs2 = dict(subs); subs2[t1] = t2; return subs2
    if is_var(t2):
        subs2 = dict(subs); subs2[t2] = t1; return subs2
    return None

def unify_args(a1, a2, subs):
    if len(a1) != len(a2): return None
    s = dict(subs)
    for x, y in zip(a1, a2):
        s = unify(x, y, s)
        if s is None: return None
    return s

def substitute_literal(lit, subs):
    p, args, pos = lit
    return (p, tuple(subs.get(a, a) for a in args), pos)

def substitute_clause(clause, subs):
    return frozenset(substitute_literal(l, subs) for l in clause)

def tautology(cl):  # clause contains L and ¬L
    lits = set((p, args, pos) for (p, args, pos) in cl)
    for p,args,pos in lits:
        if (p,args, not pos) in lits: return True
    return False

def resolve(ci, cj):
    resolvents = set()
    for li in ci:
        for lj in cj:
            pi, ai, posi = li
            pj, aj, posj = lj
            if pi == pj and posi != posj:
                s = unify_args(ai, aj, {})
                if s is None: continue
                new = set(ci); new.remove(li)
                new |= set(cj); new.remove(lj)
                r = substitute_clause(frozenset(new), s)
                if not tautology(r):
                    resolvents.add(r)
    return resolvents

def resolution(kb, query):
    # add negated query
    q = (query[0], query[1], not query[2])
    clauses = set(kb)
    clauses.add(frozenset({q}))
    new = set()
    while True:
        pairs = list(combinations(list(clauses), 2))
        generated = set()
        for ci, cj in pairs:
            for r in resolve(ci, cj):
                if not r:  # empty clause
                    return True
                if r not in clauses:
                    generated.add(r)
        if not generated:
            return False
        clauses |= generated

# --- Example KB (converted from your notebook) ---
def L(pred, args, pos=True): return (pred, tuple(args), pos)
def C(*lits): return frozenset(lits)

KB = [
    C(L("Food", ("x",), False), L("Likes", ("John","x"), True)),
    C(L("Food", ("Apple",), True)),
    C(L("Food", ("Vegetable",), True)),
    C(L("Eats", ("x","y"), False), L("Killed", ("x",), True), L("Food", ("y",), True)),
    C(L("Eats", ("Anil","Peanuts"), True)),
    C(L("Alive", ("Anil",), True)),
    C(L("Eats", ("Anil","y"), False), L("Eats", ("Harry","y"), True)),
    C(L("Alive", ("x",), False), L("Killed", ("x",), False)),
    C(L("Killed", ("x",), True), L("Alive", ("x",), True)),
]

query = L("Likes", ("John","Peanuts"), True)

if __name__ == "__main__":
    print("Proving Likes(John,Peanuts)...")
    print("Result:", resolution(KB, query))
