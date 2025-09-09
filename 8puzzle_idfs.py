from collections import deque

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

def dfs_iterative(start_state, goal_state):
    stack = deque([(start_state, [start_state], [])])  # (current_state, path, moves_list)
    visited = set()

    print("Searching for a solution using iterative DFS...")

    while stack:
        current_state, path, moves_list = stack.pop()

        # If we've found the goal state, return the path and moves
        if current_state == goal_state:
            return path, moves_list

        # Skip this state if it has already been visited
        if current_state in visited:
            continue

        visited.add(current_state)  # Mark this state as visited
        zero_r, zero_c = find_zero(current_state)


        for i in reversed(range(len(moves))):
            dr, dc = moves[i]
            nr, nc = zero_r + dr, zero_c + dc

            if 0 <= nr < 3 and 0 <= nc < 3:
                neighbor = swap(current_state, zero_r, zero_c, nr, nc)
                
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_moves_list = moves_list + [move_names[i]]
                    stack.append((neighbor, new_path, new_moves_list))

    return None, None


solution_path, moves_list = dfs_iterative(start, goal)

if solution_path:
    print(f"Solution found in {len(solution_path)-1} moves:\n")
    for i in range(len(solution_path)):
        if i > 0:
            print(f"Move empty block {moves_list[i-1]}")
        print_state(solution_path[i])
else:
    print("No solution found.")
