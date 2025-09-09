import random

class VacuumCleanerAgent:
    def __init__(self, location, state):
        # location: 'A' or 'B'
        # state: dictionary {'A': 'Dirty' or 'Clean', 'B': 'Dirty' or 'Clean'}
        self.location = location
        self.state = state

    def perceive(self):
        # Agent perceives its current location and the state of both rooms
        return self.location, self.state[self.location], self.state['A'], self.state['B']

    def act(self, perception):
        location, current_room_state, room_a_state, room_b_state = perception

        # Goal: Both rooms are clean
        if room_a_state == 'Clean' and room_b_state == 'Clean':
            return 'NoOp' # Do nothing if goal is achieved

        # If current room is dirty, suck the dirt
        if current_room_state == 'Dirty':
            return 'Suck'
        else:
            # If current room is clean, move to the other room
            if location == 'A':
                return 'MoveToB'
            else:
                return 'MoveToA'

    def run(self, steps):
        print("Initial State:", self.state, "Agent Location:", self.location)
        for _ in range(steps):
            perception = self.perceive()
            action = self.act(perception)
            print("Perception:", perception, "Action:", action)
            self.update_state(action)
            print("New State:", self.state, "Agent Location:", self.location)
            if self.state['A'] == 'Clean' and self.state['B'] == 'Clean':
                print("Goal achieved: Both rooms are clean!")
                break
        print("Simulation finished.")


    def update_state(self, action):
        if action == 'Suck':
            self.state[self.location] = 'Clean'
        elif action == 'MoveToA':
            self.location = 'A'
        elif action == 'MoveToB':
            self.location = 'B'
        # NoOp does not change the state or location

# --- Simulation ---

# Example 1: Agent starts in A, both rooms are dirty
initial_state_1 = {'A': 'Dirty', 'B': 'Dirty'}
agent1 = VacuumCleanerAgent(location='A', state=initial_state_1)
print("--- Running Simulation 1 ---")
agent1.run(steps=10)

print("\n" + "="*20 + "\n")

# Example 2: Agent starts in B, room A is dirty, room B is clean
initial_state_2 = {'A': 'Dirty', 'B': 'Clean'}
agent2 = VacuumCleanerAgent(location='B', state=initial_state_2)
print("--- Running Simulation 2 ---")
agent2.run(steps=10)
