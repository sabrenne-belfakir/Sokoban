import levels
from collections import deque

# Helper function to get the player position
def get_player_position(level):
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '@':
                return (x, y)
    return None

# Helper function to check if the game is solved
def is_goal_state(level):
    for row in level:
        if '$' in row:
            return False
    return True

# Helper function to get the possible moves
def get_possible_moves(level, player_pos):
    x, y = player_pos
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if level[new_y][new_x] != '#':  # Not a wall
            moves.append((new_x, new_y))
    return moves

# Helper function to apply a move
def apply_move(level, player_pos, move):
    level_copy = [list(row) for row in level]
    px, py = player_pos
    mx, my = move
    level_copy[py][px] = '.'  # Clear old player position
    level_copy[my][mx] = '@'  # Set new player position
    return ["".join(row) for row in level_copy]

# BFS solver
def bfs_solver(level_number):
    level = levels.get_level(level_number)
    if not level:
        return "Level not found"
    
    start_state = (level, get_player_position(level))
    queue = deque([start_state])
    visited = set()
    visited.add(tuple(tuple(row) for row in start_state[0]))
    
    while queue:
        current_level, player_pos = queue.popleft()
        if is_goal_state(current_level):
            return "Level Solved!"
        
        for move in get_possible_moves(current_level, player_pos):
            new_level = apply_move(current_level, player_pos, move)
            new_state = (new_level, move)
            new_state_tuple = tuple(tuple(row) for row in new_state[0])
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append(new_state)

    return "No solution found"

if __name__ == "__main__":
    level = 0
    print(f"Solution for level {level}: {bfs_solver(level)}")
