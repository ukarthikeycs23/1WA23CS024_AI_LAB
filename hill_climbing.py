import random
import copy

# Goal state
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]   # 0 = blank

# Calculate Manhattan distance
def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:  # skip blank
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

# Hill climbing algorithm
def hill_climbing(start_state):
    current = start_state
    current_h = manhattan(current)
    
    step = 0
    while True:
        print(f"Step {step}: h = {current_h} (Manhattan distance)")
        print_state(current)
        
        if current_h == 0:
            print("Reached goal!")
            break
        
        neighbors = get_neighbors(current)
        best_neighbor = None
        best_h = float("inf")
        
        for neighbor in neighbors:
            h = manhattan(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
        
        # If no improvement, stop
        if best_h >= current_h:
            print("No better neighbor found. Stopping.")
            break
        
        # Move to better neighbor
        current = best_neighbor
        current_h = best_h
        step += 1


# Example start state (scrambled)
start_state = [[2, 8, 3],
               [1, 6, 4],
               [7, 0, 5]]

hill_climbing(start_state)
