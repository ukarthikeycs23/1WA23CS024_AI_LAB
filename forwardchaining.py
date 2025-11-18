# Minimal forward chaining (rule-based inference)
# - Terms: strings (variables start with lowercase, e.g. 'p', constants 'Robert')
# - Atom: tuple (predicate:str, args: tuple[str,...])
# - Fact: same as Atom
# - Rule: (premises: list[Atom], conclusion: Atom)

from itertools import product

def is_var(x): return isinstance(x, str) and x and x[0].islower()

def apply_subst_term(t, subst):
    return subst.get(t, t)

def apply_subst_atom(atom, subst):
    pred, args = atom
    return (pred, tuple(apply_subst_term(a, subst) for a in args))

def unify_terms(t1, t2, subst):
    # apply current substitution
    t1 = apply_subst_term(t1, subst)
    t2 = apply_subst_term(t2, subst)
    if t1 == t2:
        return subst
    if is_var(t1):
        new = dict(subst); new[t1] = t2; return new
    if is_var(t2):
        new = dict(subst); new[t2] = t1; return new
    return None

def unify_atoms(a, b, subst=None):
    """Unify atom a with atom b (same predicate), return substitution or None."""
    if subst is None: subst = {}
    p1, args1 = a; p2, args2 = b
    if p1 != p2 or len(args1) != len(args2):
        return None
    s = dict(subst)
    for x,y in zip(args1, args2):
        s = unify_terms(x, y, s)
        if s is None: return None
    return s

def match_premises_to_facts(premises, facts):
    """
    Try to find substitutions that make all premises true w.r.t facts.
    Returns list of substitutions (possibly multiple matches).
    """
    # For each premise, find facts with same predicate and try unify.
    # We perform a simple backtracking to combine substitutions consistently.
    matches = []

    def backtrack(i, current_subst):
        if i == len(premises):
            matches.append(dict(current_subst))
            return
        prem = premises[i]
        for f in facts_by_pred.get(prem[0], []):
            s = unify_atoms(prem, f, dict(current_subst))
            if s is not None:
                backtrack(i+1, s)

    # index facts by predicate for speed
    facts_by_pred = {}
    for f in facts:
        facts_by_pred.setdefault(f[0], []).append(f)

    backtrack(0, {})
    return matches

def forward_chain(facts, rules, query=None, verbose=False):
    """
    facts: set of Atom tuples
    rules: list of (premises:list[Atom], conclusion:Atom)
    query: Atom or None
    Returns (derived_facts_set, proved_bool)
    """
    derived = set(facts)
    while True:
        new_facts = set()
        for premises, conclusion in rules:
            subs_list = match_premises_to_facts(premises, derived)
            for subst in subs_list:
                inferred = apply_subst_atom(conclusion, subst)
                if inferred not in derived:
                    if verbose:
                        print("Applying rule:", " ^ ".join(format_atom(p) for p in premises),
                              "=>", format_atom(conclusion), "with", subst)
                        print("  Inferred:", format_atom(inferred))
                    new_facts.add(inferred)
        if not new_facts:
            break
        derived |= new_facts
        if query and query in derived:
            return derived, True
    return derived, (query in derived) if query else (len(new_facts)>0)

# ---------- small helpers for display / building ----------
def atom(pred, *args):
    return (pred, tuple(args))

def format_atom(a):
    p, args = a
    return f"{p}({', '.join(args)})"

# ---------------- Hard-coded example (from your notebook) ----------------
if __name__ == "__main__":
    # Facts
    facts = {
        atom("American", "Robert"),
        atom("Weapons", "T1"),
        atom("Sells", "Robert", "T1", "A"),
        atom("Hostile", "A"),
    }

    # Rule: American(p) ^ Weapons(q) ^ Sells(p,q,r) ^ Hostile(r) => Criminal(p)
    rule_premises = [
        atom("American", "p"),
        atom("Weapons", "q"),
        atom("Sells", "p", "q", "r"),
        atom("Hostile", "r"),
    ]
    rule_conclusion = atom("Criminal", "p")
    rules = [(rule_premises, rule_conclusion)]

    query = atom("Criminal", "Robert")

    derived, proved = forward_chain(facts, rules, query=query, verbose=True)

    print("\n--- Final Derived Facts ---")
    for f in sorted(derived):
        print(" ", format_atom(f))
    print("\nQuery:", format_atom(query))
    print("Result:", "TRUE" if proved else "FALSE")
