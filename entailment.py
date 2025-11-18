from itertools import product

# -----------------------------
# 1. Expression Evaluation
# -----------------------------
def evaluate(expr, model):
    """Evaluate a propositional logic expression under a given model."""
    if isinstance(expr, str):
        return model[expr]

    op = expr[0]

    if op == 'not':
        return not evaluate(expr[1], model)
    elif op == 'and':
        return evaluate(expr[1], model) and evaluate(expr[2], model)
    elif op == 'or':
        return evaluate(expr[1], model) or evaluate(expr[2], model)
    elif op == 'implies':
        return (not evaluate(expr[1], model)) or evaluate(expr[2], model)
    else:
        raise ValueError("Unknown operator", op)

# -----------------------------
# 2. Collect all propositional symbols
# -----------------------------
def get_symbols(expr):
    """Return a set of all propositional symbols inside expr."""
    if isinstance(expr, str):
        return {expr}

    op = expr[0]

    if op == 'not':
        return get_symbols(expr[1])

    # binary ops
    return get_symbols(expr[1]) | get_symbols(expr[2])

# -----------------------------
# 3. Truth Table Entailment Check
# -----------------------------
def tt_entails(KB, query):
    """
    Return True if KB entails query using truth-table enumeration.
    KB and query are expressions.
    """
    symbols = sorted(list(get_symbols(KB) | get_symbols(query)))

    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        if evaluate(KB, model) and not evaluate(query, model):
            # Found a model where KB is True but query is False → NOT entailment
            return False

    return True

# -----------------------------
# 4. Truth Table Printer
# -----------------------------
def print_truth_table(KB, query):
    symbols = sorted(list(get_symbols(KB) | get_symbols(query)))
    header = " | ".join(symbols) + " || KB | Query"
    print(header)
    print("-" * len(header))

    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        symbol_vals = " | ".join('T' if model[s] else 'F' for s in symbols)
        kb_val = 'T' if evaluate(KB, model) else 'F'
        q_val = 'T' if evaluate(query, model) else 'F'

        print(f"{symbol_vals} ||  {kb_val}  |   {q_val}")

# -----------------------------
# 5. Hard-coded Example
# -----------------------------
# KB = (A ∨ C) ∧ (B ∨ ¬C)
KB = ('and',
        ('or', 'A', 'C'),
        ('or', 'B', ('not', 'C'))
     )

# Query α = A ∨ B
query = ('or', 'A', 'B')

# -----------------------------
# 6. Run example
# -----------------------------
print("Truth Table:")
print_truth_table(KB, query)

print("\nDoes KB entail query?")
print(tt_entails(KB, query))
