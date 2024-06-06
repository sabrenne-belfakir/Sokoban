# Sokoban Game Solver

This project is a Sokoban game implemented in Python. It includes various scripts to set up the game, display the game, and evently solve levels (if I figure it out), and manage the game's state. The game uses the Pygame library for rendering the game and handling user interactions.

## File Descriptions

### `main.py`
This is the main script to run the Sokoban game. It includes functions to start the game, handle user inputs, and manage game states. The script sets up the initial game environment and runs the game loop.

### `sokoban_solver.py`
This script contains the logic for solving Sokoban levels. It implements algorithms to find the optimal solution to the puzzle, allowing the player to see the correct sequence of moves needed to solve a level.

### `levels.py`
This script defines the levels of the Sokoban game. It includes the layout of each level and the positions of the player, boxes, and targets. The levels are represented as matrices.

### `setup_db.py`
This script sets up a database to store the game state and player progress. It initialises the database and includes functions to save and retrieve game data.

### `display_game.py`
This script handles the display of the game using Pygame. It includes functions to render the game board, draw the player, boxes, and targets, and update the display based on user actions.

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

## Customising Levels

You can customise the levels by modifying the `levels.py` file. Each level is represented as a matrix, where different numbers represent the player, boxes, targets, and walls.

## Solving Levels

The `sokoban_solver.py` script can be used to find solutions to the levels. This can be useful for players who are stuck and need hints on how to proceed.

## Saving and Loading Game State

The game state and player progress are managed using a database set up by the `setup_db.py` script. This ensures that the player's progress is saved between sessions.

## Credits

This game was developed by Sabrenne Belfakir.
