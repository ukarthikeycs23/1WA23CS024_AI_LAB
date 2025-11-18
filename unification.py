# Minimal unification utilities (terms as strings or lists like ['f','x','a'])
# - Variables: strings starting with a lowercase letter (e.g., 'x', 'y')
# - Constants / function symbols: other strings (e.g., 'A', 'John', 'f')
# - Compound term: list where first element is function symbol and rest are args

def is_variable(x):
    """Return True iff x is a variable (string starting with lowercase)."""
    return isinstance(x, str) and len(x) > 0 and x[0].islower()

def occur_check(var, term):
    """Return True if var occurs anywhere inside term (prevents infinite bindings)."""
    if var == term:
        return True
    if isinstance(term, list):
        return any(occur_check(var, t) for t in term)
    return False

def apply_subst(term, subst):
    """Apply substitution mapping to a term (recursive)."""
    if isinstance(term, str):
        return subst.get(term, term)
    # compound term (list)
    return [apply_subst(t, subst) for t in term]

def unify(x, y, subst=None):
    """
    Unify terms x and y under initial substitution `subst` (dict).
    Returns a substitution dict or None on failure.
    Substitution maps variable-name -> term (string or list).
    """
    if subst is None:
        subst = {}

    # Apply current substitution to both sides
    x = apply_subst(x, subst)
    y = apply_subst(y, subst)

    # identical after applying substitution
    if x == y:
        return subst

    # variable cases
    if is_variable(x):
        if occur_check(x, y):
            return None
        new = dict(subst); new[x] = y
        return new

    if is_variable(y):
        if occur_check(y, x):
            return None
        new = dict(subst); new[y] = x
        return new

    # both compound terms (lists): check arity and functor
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        # optional: check same functor name at position 0
        if x[0] != y[0]:
            return None
        cur = dict(subst)
        for a, b in zip(x, y):
            cur = unify(a, b, cur)
            if cur is None:
                return None
        return cur

    # both are different constants -> fail
    return None

# -------------------------
# Examples / quick tests
# -------------------------
if __name__ == "__main__":
    # Example 1: unify f(x,b) with f(a,y)  -> { x: 'a', y: 'b' }
    expr1 = ['f', 'x', 'b']
    expr2 = ['f', 'a', 'y']
    res = unify(expr1, expr2)
    print("Unify", expr1, "with", expr2, "=>", res)

    # Example 2: different functor -> failure
    expr3 = ['f', 'x', 'b']
    expr4 = ['g', 'a', 'y']
    res2 = unify(expr3, expr4)
    print("Unify", expr3, "with", expr4, "=>", res2)

    # Example 3: occur-check prevents x = f(x)
    expr5 = 'x'
    expr6 = ['f', 'x']
    res3 = unify(expr5, expr6)
    print("Unify", expr5, "with", expr6, "=>", res3)
