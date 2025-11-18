# Minimal Alpha-Beta (simple, modular, trace of pruned branches)
# - Tree: nested lists; leaves are ints (scores)
# - Returns best value, best path (list of child indices), and pruned info

import math
from typing import Tuple, List, Any

PruneInfo = Tuple[str, int, List[int]]  # (who, depth, remaining_child_indices)

def alpha_beta(node: Any, depth: int, alpha: float, beta: float,
               maximizing: bool) -> Tuple[float, List[int], List[PruneInfo]]:
    """
    Returns (best_value, best_path, pruned_list) for the subtree rooted at node.
    best_path is a list of indices from this node down to the chosen leaf.
    pruned_list collects prune events occurring in this subtree (local indexing).
    """
    pruned: List[PruneInfo] = []

    # Leaf node
    if isinstance(node, int):
        return float(node), [], pruned

    if maximizing:
        best_val = -math.inf
        best_path: List[int] = []
        for i, child in enumerate(node):
            val, path, child_pruned = alpha_beta(child, depth + 1, alpha, beta, False)
            pruned.extend(child_pruned)
            if val > best_val:
                best_val, best_path = val, [i] + path
            alpha = max(alpha, best_val)
            if alpha >= beta:  # prune remaining children
                remaining = list(range(i + 1, len(node)))
                pruned.append(("MAX", depth, remaining))
                break
        return best_val, best_path, pruned
    else:  # minimizing
        best_val = math.inf
        best_path: List[int] = []
        for i, child in enumerate(node):
            val, path, child_pruned = alpha_beta(child, depth + 1, alpha, beta, True)
            pruned.extend(child_pruned)
            if val < best_val:
                best_val, best_path = val, [i] + path
            beta = min(beta, best_val)
            if alpha >= beta:
                remaining = list(range(i + 1, len(node)))
                pruned.append(("MIN", depth, remaining))
                break
        return best_val, best_path, pruned


# --- Hard-coded tree from your notebook ---
# Root is a maximizing node; each sublist is children (MIN level next)
tree = [
    [   # Left subtree (MIN)
        [21, 5],
        [15, 11],
        [12, 8]
    ],
    [   # Middle subtree (MIN)
        [9, 13],
        [5, 12],
        [13, 12]
    ],
    [   # Right subtree (MIN)
        [13, 14],
        [7, 10]
    ]
]

if __name__ == "__main__":
    value, path, pruned_events = alpha_beta(tree, depth=0, alpha=-math.inf, beta=math.inf, maximizing=True)
    print("Root value:", value)
    print("Path (indices at each level):", path)   # e.g. [0,1,0] -> root's child 0, then 1, then 0
    print("Pruned events (who, depth, remaining child indices):")
    for e in pruned_events:
        print(" ", e)
