# Sokoban Game

This project is a Sokoban game implemented in Python. It includes various scripts to set up the game, display the game, solve levels, and manage the game's state. The game uses the Pygame library for rendering the game and handling user interactions.

## File Descriptions

### `main.py`
This is the main script to run the Sokoban game. It includes functions to start the game, handle user inputs, and manage game states. The script sets up the initial game environment and runs the game loop.

Key functions and their descriptions:
- `start_screen()`: Displays the start screen where the player can input their name and select game options.
- `main()`: Initializes the game, loads levels, and starts the main game loop.
- `handle_event(event)`: Processes user inputs and updates the game state accordingly.

### `sokoban_solver.py (work in progress)`
This script contains the logic for solving Sokoban levels. It implements algorithms to find the optimal solution to the puzzle, allowing the player to see the correct sequence of moves needed to solve a level.

Key functions and their descriptions:
- `solve_level(level)`: Takes a level as input and returns a sequence of moves to solve the level.
- `is_solved(level)`: Checks if the given level is solved.
- `find_solution(level)`: Uses search algorithms like BFS or DFS to find the solution.

### `levels.py`
This script defines the levels of the Sokoban game. It includes the layout of each level and the positions of the player, boxes, and targets. The levels are represented as matrices.

Example level representation:
```python
levels = [
    [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 2, 1],
        [1, 0, 3, 0, 1],
        [1, 0, 0, 4, 1],
        [1, 1, 1, 1, 1]
    ],
    # Add more levels here
]
```
- `1` represents a wall.
- `0` represents an empty space.
- `2` represents the player.
- `3` represents a box.
- `4` represents a target.

### `setup_db.py`
This script sets up a database to store the game state and player progress. It initializes the database and includes functions to save and retrieve game data.

Key functions and their descriptions:
- `init_db()`: Initializes the SQLite database.
- `save_game_state(player_name, level, moves)`: Saves the current game state to the database.
- `load_game_state(player_name)`: Loads the saved game state for a player from the database.

### `display_game.py`
This script handles the display of the game using Pygame. It includes functions to render the game board, draw the player, boxes, and targets, and update the display based on user actions.

Key functions and their descriptions:
- `draw_board(level)`: Renders the current state of the level on the screen.
- `update_display()`: Updates the display after each move.
- `display_game(background, box, player)`: Manages the main game display loop.

## Installation

To run this project, you need to have Python and Pygame installed. You can install Pygame using pip:

```sh
pip install pygame
```

## Running the Game

To start the game, run the `main.py` script:

```sh
python main.py
```

## Game Controls

- **Arrow Keys**: Move the player.
- **Reset**: Restart the current level.
- **Undo**: Undo the last move.
- **Next**: Move to the next level.
- **Quit**: Quit the game.

## Customizing Levels

You can customize the levels by modifying the `levels.py` file. Each level is represented as a matrix, where different numbers represent the player, boxes, targets, and walls.

## Solving Levels

The `sokoban_solver.py` script can be used to find solutions to the levels. This can be useful for players who are stuck and need hints on how to proceed.

## Saving and Loading Game State

The game state and player progress are managed using a database set up by the `setup_db.py` script. This ensures that the player's progress is saved between sessions.

## Detailed Code Explanation

### `main.py`

- **Initialization**: The script initializes Pygame and sets up the game window and various assets like images for the player, boxes, and targets.
- **Game Loop**: The main game loop handles user inputs, updates the game state, and redraws the game board. It checks for level completion and manages transitions between levels.
- **Event Handling**: User inputs like key presses are processed to move the player, restart the level, undo moves, or navigate between levels.

### `sokoban_solver.py`

- **Search Algorithms**: The script uses algorithms like Breadth-First Search (BFS) to explore possible moves and find the shortest path to solve the level.
- **State Representation**: The game state is represented as a matrix, and each move generates a new state that is checked for validity (i.e., boxes are not pushed into walls or each other).

### `levels.py`

- **Level Design**: Levels are designed as matrices with specific values representing different elements of the game. This modular approach makes it easy to add or modify levels.

### `setup_db.py`

- **Database Management**: Uses SQLite to create a local database for storing game states. This includes functions to initialize the database, save game progress, and load saved states.

### `display_game.py`

- **Rendering**: Handles all aspects of rendering the game using Pygame. This includes drawing the game board, player, boxes, and targets. It also updates the display based on game events.

## Credits

This game was developed by Sabrenne Belfakir.
