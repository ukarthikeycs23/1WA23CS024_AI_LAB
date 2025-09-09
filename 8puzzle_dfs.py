from heapq import heappop, heappush
import sys

# Increase the maximum recursion depth
sys.setrecursionlimit(2000)

start = ((2, 3, 1),
         (4, 8, 6),
         (5, 7, 0))  # 0 represents the empty block

goal = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 0))

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
move_names = ['up', 'down', 'left', 'right']


def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def swap(state, r1, c1, r2, c2):
    state = [list(row) for row in state]
    state[r1][c1], state[r2][c2] = state[r2][c2], state[r1][c1]
    return tuple(tuple(row) for row in state)

def print_state(state):
    for row in state:
        print(' '.join(str(x) if x != 0 else 'x' for x in row))
    print()

def dfs_recursive(current_state, goal_state, visited, path, moves_list):
    if current_state == goal_state:
        return True

    visited.add(current_state)
    zero_r, zero_c = find_zero(current_state)

    for i, (dr, dc) in enumerate(moves):
        nr, nc = zero_r + dr, zero_c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            neighbor = swap(current_state, zero_r, zero_c, nr, nc)
            if neighbor not in visited:
                path.append(neighbor)
                moves_list.append(move_names[i])
                if dfs_recursive(neighbor, goal_state, visited, path, moves_list):
                    return True
                path.pop()  # Backtrack
                moves_list.pop() # Backtrack

    return False

# Initialize variables for DFS
visited = set()
path = [start]
moves_list = []

print("Searching for a solution using DFS...")

if dfs_recursive(start, goal, visited, path, moves_list):
    print(f"Solution found in {len(path)-1} moves:\n")
    for i in range(len(path)):
        if i > 0:
            print(f"Move empty block {moves_list[i-1]}")
        print_state(path[i])
else:
    print("No solution found within the search limits.")
