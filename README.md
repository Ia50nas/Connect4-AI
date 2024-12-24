# Connect 4 AI Simulation

This repository contains an implementation of a Connect 4 game where two AI players compete against each other. The project includes game logic, two AI player strategies (Minimax and Monte Carlo Tree Search), and simulation scripts to analyze their performance under different computational budgets.

## Features

- **Connect 4 Gameplay**: Implements the classic Connect 4 game.
- **AI Players**:
  - **Player 1**: Uses a Minimax algorithm with alpha-beta pruning and a custom evaluation function.
  - **Player 2**: Implements Monte Carlo Tree Search (MCTS) for decision-making.
- **Simulation Tools**: Run single or multiple games to evaluate AI performance under different computational budgets.

## Project Structure

- **`game_logic.py`**: Core game logic for Connect 4, including game state management and win condition checks.
- **`Player1.py`**: Implementation of Player 1 using Minimax with alpha-beta pruning.
- **`Player2.py`**: Implementation of Player 2 using Monte Carlo Tree Search.
- **`simulate_games.py`**: Script for running multiple simulations and analyzing the results.

## Requirements

- Python 3.7 or higher
- Libraries:
  - `colorama`
  - `multiprocessing`
  - `math`
  - `random`

Install dependencies with:
```bash
pip install colorama
```

## Usage

### Running a Single Game

To play a single game between Player 1 and Player 2:

```bash
python game_logic.py (will showcase all moves)
python simulate_games.py (will showcase results)
```

Customize the computational budget by modifying the `computational_budget` variable in the `PlayGame` function.

### Running Multiple Simulations

To simulate multiple games:

1. Set the desired computational budgets in the `budgets` list.
2. Specify the number of games per budget in the `num_games` variable.

Run the script:

```bash
python simulate_games.py
```

The script outputs:
- Win counts for Player 1, Player 2, and draws.
- Winning percentages.
- Average moves and time per move.
- Longest win streaks for each player.

### Adjusting Parameters

- **Game Board Dimensions**: Modify the `width`, `height`, or `connect` parameters in `Connect4State`.
- **AI Computational Budget**: Change the `computational_budget` parameter for Player 1 and Player 2.
- **Evaluation Function**: Enhance or modify the evaluation logic in `Player1.py` for customized AI behavior.


### Single Game Output
```
. . . . . . .
. . . . . . .
. . . . . . .
. . . X O . .
. . X O X . .
O X O X O X O

Player 2 wins!
```

### Simulation Results
```
Results for budget 100:
Player1 Wins: 53
Player2 Wins: 42
Draws: 5
Winning Percentage: {'Player1': 53.0, 'Player2': 42.0, 'Draws': 5.0}
Average Moves: {'Player1': 14, 'Player2': 25}
Average Time Per Move: {'Player1': 0.002, 'Player2': 0.005}
Longest Win Streak: {'Player1': 12, 'Player2': 8}

**These are not the actual results for the results please refer to running the program**
```


