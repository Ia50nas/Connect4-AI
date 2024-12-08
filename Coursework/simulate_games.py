import time
from multiprocessing import Pool
from Player1 import Player1
from Player2 import Player2
from game_logic import Connect4State

''' 
Run this file in order to run multiple games at once 
In main add into budgets the number of computational budgets you want to test and
num_games the number of games it should play per computational budget
'''
def simulate_single_game(args):
    from game_logic import Connect4State
    from Player1 import Player1
    from Player2 import Player2

    budget, game_id = args
    state = Connect4State()

    # Alternate starting player
    if game_id % 2 == 0:
        state.playerJustMoved = 2  # Player 1 starts
    else:
        state.playerJustMoved = 1  # Player 2 starts

    player1 = Player1(computational_budget=budget)
    player2 = Player2(computational_budget=budget)

    player_time = {1: 0, 2: 0}
    move_count = 0

    while not state.IsGameOver():
        start_time = time.time()
        if state.playerJustMoved == 1:
            move = player2.choose_move(state)
        else:
            move = player1.choose_move(state)
        end_time = time.time()

        player_time[state.playerJustMoved] += (end_time - start_time)
        state.DoMove(move)
        move_count += 1

    # Ensure a valid return value for outcome
    winner = state.winner
    if winner not in [1, 2]:
        winner = 0  # Treat unexpected outcomes as a draw

    return winner, move_count, player_time

def simulate_games_parallel(num_games, budgets):
    results = {budget: {"Player1_Wins": 0, "Player2_Wins": 0, "Draws": 0} for budget in budgets}
    total_moves = {budget: {1: 0, 2: 0, "Draws": 0} for budget in budgets}
    win_counts = {budget: {1: 0, 2: 0, 0: 0} for budget in budgets}  # Include 0 for draws
    total_time = {budget: {1: 0, 2: 0} for budget in budgets}
    win_streaks = {budget: {1: 0, 2: 0} for budget in budgets}
    current_streak = {budget: {1: 0, 2: 0} for budget in budgets}

    for budget in budgets:
        print(f"Simulating games for budget: {budget}")
        completed_games = 0
        outcomes = []

        with Pool() as pool:
            for outcome in pool.imap(simulate_single_game, [(budget, i) for i in range(num_games)]):
                outcomes.append(outcome)
                completed_games += 1
                if completed_games % 10 == 0 or completed_games == num_games:  # Update progress every 10 games
                    print(f"Games completed: {completed_games}/{num_games}")
            for outcome, moves, player_time in outcomes:
                if outcome not in [1, 2, 0]:  # Handle unexpected outcomes
                    print(f"Unexpected outcome: {outcome}. Defaulting to Draw.")
                    outcome = 0

                if outcome == 1:
                    results[budget]["Player1_Wins"] += 1
                    total_moves[budget][1] += moves
                    total_time[budget][1] += player_time[1]
                    current_streak[budget][1] += 1
                    win_streaks[budget][1] = max(win_streaks[budget][1], current_streak[budget][1])
                    current_streak[budget][2] = 0
                elif outcome == 2:
                    results[budget]["Player2_Wins"] += 1
                    total_moves[budget][2] += moves
                    total_time[budget][2] += player_time[2]
                    current_streak[budget][2] += 1
                    win_streaks[budget][2] = max(win_streaks[budget][2], current_streak[budget][2])
                    current_streak[budget][1] = 0
                else:  # Draw
                    results[budget]["Draws"] += 1
                    total_moves[budget]["Draws"] += moves
                    current_streak[budget] = {1: 0, 2: 0}
                win_counts[budget][outcome] += 1

    metrics = {}
    for budget in budgets:
        metrics[budget] = {
            "Winning_Percentage": {
                "Player1": (results[budget]["Player1_Wins"] / num_games) * 100,
                "Player2": (results[budget]["Player2_Wins"] / num_games) * 100,
                "Draws": (results[budget]["Draws"] / num_games) * 100,
            },
            "Average_Moves": {
                "Player1": total_moves[budget][1] / win_counts[budget][1] if win_counts[budget][1] > 0 else 0,
                "Player2": total_moves[budget][2] / win_counts[budget][2] if win_counts[budget][2] > 0 else 0,
                "Draws": total_moves[budget]["Draws"] / win_counts[budget][0] if win_counts[budget][0] > 0 else 0,
            },
            "Average_Time_Per_Move": {
                "Player1": total_time[budget][1] / results[budget]["Player1_Wins"] if results[budget]["Player1_Wins"] > 0 else 0,
                "Player2": total_time[budget][2] / results[budget]["Player2_Wins"] if results[budget]["Player2_Wins"] > 0 else 0,
            },
            "Longest_Win_Streak": {
                "Player1": win_streaks[budget][1],
                "Player2": win_streaks[budget][2],
            },
        }
    return results, metrics


if __name__ == "__main__":
    budgets = [100,500,1000,10000]  # You can add more budgets like 500, 1000, 10000
    num_games = 1000  # Adjust the number of games as needed
    results, metrics = simulate_games_parallel(num_games, budgets)

    for budget, result in results.items():
        print(f"\nResults for budget {budget}:")
        print(f"Player1 Wins: {result['Player1_Wins']}")
        print(f"Player2 Wins: {result['Player2_Wins']}")
        print(f"Draws: {result['Draws']}")
        print(f"Winning Percentage: {metrics[budget]['Winning_Percentage']}")
        print(f"Average Moves: {metrics[budget]['Average_Moves']}")
        print(f"Average Time Per Move: {metrics[budget]['Average_Time_Per_Move']}")
        print(f"Longest Win Streak: {metrics[budget]['Longest_Win_Streak']}")