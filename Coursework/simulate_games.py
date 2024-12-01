from multiprocessing import Pool
from Player1 import Player1
from Player2 import Player2
from game_logic import Connect4State

def simulate_single_game(args):
    # Import dependencies explicitly within the function
    from game_logic import Connect4State
    from Player1 import Player1
    from Player2 import Player2

    budget, game_id = args
    state = Connect4State()
    player1 = Player1(computational_budget=budget)
    player2 = Player2(computational_budget=budget)

    while not state.IsGameOver():
        if state.playerJustMoved == 1:
            move = player2.choose_move(state)
        else:
            move = player1.choose_move(state)
        state.DoMove(move)

    return state.winner

def simulate_games_parallel(num_games, budgets):
    results = {budget: {"Player1_Wins": 0, "Player2_Wins": 0, "Draws": 0} for budget in budgets}
    for budget in budgets:
        print(f"Simulating games for budget: {budget}")
        with Pool() as pool:
            outcomes = pool.map(simulate_single_game, [(budget, i) for i in range(num_games)])
            for outcome in outcomes:
                if outcome == 1:
                    results[budget]["Player1_Wins"] += 1
                elif outcome == 2:
                    results[budget]["Player2_Wins"] += 1
                else:
                    results[budget]["Draws"] += 1
    return results

if __name__ == "__main__":
    budgets = [100]#100, 500, 1000, 10000
    num_games = 1000  # Increase this number as needed
    results = simulate_games_parallel(num_games, budgets)
    for budget, result in results.items():
        print(f"\nResults for budget {budget}:")
        print(f"Player1 Wins: {result['Player1_Wins']}")
        print(f"Player2 Wins: {result['Player2_Wins']}")
        print(f"Draws: {result['Draws']}")
