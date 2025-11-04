from collections import deque

initial_state = {"A": "B", "B": "C", "C": "Floor1"}
goal_state = {"A": "B", "B": "C", "C": "Floor3"}

floors = ["Floor1", "Floor2", "Floor3"]

def get_floor(block, state):
    while True:
        if state[block] in floors:
            return state[block]
        else:
            block = state[block]

def is_valid_move(block, destination):
    if block == "B" and destination == "A":
        return False
    if block == "C" and destination in ["A", "B"]:
        return False
    return True

def is_top_block(block, state):
    for blocks in state:
        if state[blocks] == block:
            return False
    return True

def get_possible_destinations(current_block, state):
    possible_destinations = list(floors) + list(state.keys())

    # Remove the block itself
    possible_destinations.remove(current_block)

    # Remove all floors that have something else on it
    occupied_floors = []
    for block in state:
        occupied_floors.append(get_floor(block, state))
    for floor in occupied_floors:
        if floor in possible_destinations:
            possible_destinations.remove(floor)

    # Remove all destinations that are more than one step away
    far_away_floors = []
    current_floor = get_floor(current_block, state)
    current_index = floors.index(current_floor)
    for destination in possible_destinations:
        dest_floor = get_floor(destination, state) if destination in state else destination
        if abs(floors.index(dest_floor) - current_index) > 1:
            far_away_floors.append(destination)
    for floor in far_away_floors:
        if floor in possible_destinations:
            possible_destinations.remove(floor)

    # Remove destinations that are not top blocks
    non_top_blocks = []
    for destination in possible_destinations:
        if destination in state:
            if not is_top_block(destination, state):
                non_top_blocks.append(destination)
    for block in non_top_blocks:
        if block in possible_destinations:
            possible_destinations.remove(block)

    # Remove destinations that are not valid (B on A etc)
    invalid_destinations = []
    for destination in possible_destinations:
        if not is_valid_move(current_block, destination):
            invalid_destinations.append(destination)
    for destination in invalid_destinations:
        if destination in possible_destinations:
            possible_destinations.remove(destination)

    return possible_destinations

def action(block, destination, state):
    state[block] = destination

    return state

# Helper function just to print out the state on the board
def print_state(state):
    bottom_line = ["X", "X", "X"]
    middle_line = ["X", "X", "X"]
    top_line = ["X", "X", "X"]
    blocks = list(state.keys())
    for block in blocks:
        if state[block] in floors:
            bottom_line[floors.index(state[block])] = block
    blocks = [block for block in blocks if block not in bottom_line]

    for block in blocks:
        if state[block] in bottom_line:
            middle_line[floors.index(get_floor(block, state))] = block
    blocks = [block for block in blocks if block not in middle_line]

    for block in blocks:
        if state[block] in middle_line:
            top_line[floors.index(get_floor(block, state))] = block
    blocks = [block for block in blocks if block not in top_line]

    result_string = (" ".join(top_line) + "\n" + " ".join(middle_line) + "\n" + " ".join(bottom_line)
                     + "\n" + "---------")
    print(result_string)

def bfs():
    queue = deque([(initial_state, [initial_state])])  # Start with initial state in the path

    visited = set()
    visited.add(str(initial_state))

    while queue:
        current_state, state_path = queue.popleft()

        # Check if we've reached the goal state
        if current_state == goal_state:
            return state_path  # Returns list of states from initial to goal

        # Generate actions for each block
        for block in current_state:
            if is_top_block(block, current_state):
                possible_destinations = get_possible_destinations(block, current_state)

                # Generate new states based on valid destinations
                for destination in possible_destinations:
                    # Create a copy of the current state to make a valid move
                    new_state = current_state.copy()
                    new_state = action(block, destination, new_state)

                    # Add the new state to the path
                    new_state_path = state_path + [new_state]

                    # Check if new_state is already visited, if not add it to queue
                    if str(new_state) not in visited:
                        visited.add(str(new_state))
                        queue.append((new_state, new_state_path))

                        # Print out all paths for problem space graph
                        print(f"{current_state} --[move {block} to {destination}]--> {new_state}")
                        print_state(current_state)
                        print_state(new_state)

    return None

solution = bfs()
print("Solution sequence:", solution)
for state in solution:
    print_state(state)