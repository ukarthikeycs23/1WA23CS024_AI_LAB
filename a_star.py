import heapq
import copy

# Goal state
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]   # 0 = blank

# Manhattan distance heuristic
def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, 3)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

# Find blank tile
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate neighbors
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    moves = [(1,0), (-1,0), (0,1), (0,-1)]  # down, up, right, left
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# Print board
def print_state(state):
    for row in state:
        print(row)
    print()

# Convert state to tuple (hashable for sets/dicts)
def to_tuple(state):
    return tuple(tuple(row) for row in state)

# Reconstruct path from goal back to start
def reconstruct_path(parents, node):
    path = []
    while node is not None:
        path.append(node)
        node = parents.get(to_tuple(node))
    return path[::-1]  # reverse

# A* algorithm
def a_star(start_state):
    open_list = []
    heapq.heappush(open_list, (manhattan(start_state), 0, start_state))  # (f, g, state)

    parents = {to_tuple(start_state): None}
    g_score = {to_tuple(start_state): 0}
    visited = set()

    while open_list:
        f, g, current = heapq.heappop(open_list)

        print(f"Expanding state with g={g}, h={manhattan(current)}, f={f}")
        print_state(current)

        if current == goal_state:
            print("Reached goal!")
            return reconstruct_path(parents, current)

        visited.add(to_tuple(current))

        for neighbor in get_neighbors(current):
            neighbor_t = to_tuple(neighbor)
            tentative_g = g + 1

            if neighbor_t in visited:
                continue

            if neighbor_t not in g_score or tentative_g < g_score[neighbor_t]:
                parents[neighbor_t] = current
                g_score[neighbor_t] = tentative_g
                h = manhattan(neighbor)
                f = tentative_g + h
                heapq.heappush(open_list, (f, tentative_g, neighbor))

    return None  # No solution found


# Example start state
start_state = [[2, 8, 3],
               [1, 6, 4],
               [7, 0, 5]]

solution_path = a_star(start_state)

print("\nSolution path:")
for step, state in enumerate(solution_path):
    print(f"Step {step}:")
    print_state(state)
