import random
from Player1 import Player1
from Player2 import Player2
from game_logic import Connect4State

def simulate_games(num_games, computational_budget):
    p1_wins = 0
    p2_wins = 0
    draws = 0

    for _ in range(num_games):
        state = Connect4State()
        player1 = Player1(computational_budget=computational_budget)
        player2 = Player2(computational_budget=computational_budget)

        while not state.IsGameOver():
            if state.playerJustMoved == 1:
                move = player2.choose_move(state)
            else:
                move = player1.choose_move(state)
            state.DoMove(move)

        if state.winner == 1:
            p1_wins += 1
        elif state.winner == 2:
            p2_wins += 1
        else:
            draws += 1

    return {"Player1_Wins": p1_wins, "Player2_Wins": p2_wins, "Draws": draws}

if __name__ == "__main__":
    num_games = 10
    computational_budget = 1000  # Adjust this value as needed

    results = simulate_games(num_games, computational_budget)
    print(f"Results after {num_games} games:")
    print(f"Player1 Wins: {results['Player1_Wins']}")
    print(f"Player2 Wins: {results['Player2_Wins']}")
    print(f"Draws: {results['Draws']}")
