import random


def Minimax(state,depth,maximizingPlayer):
    #if maximum depth has been reaches or the game evaluate current state
    if (depth == 0) or state.IsGameOver():
        return EvaluateState(state)

    if maximizingPlayer:
        #It is Player's 1 turn so Maximise Score
        #Initialize with the smallest possible value
        bestScore = -float('inf')

        #loop through all moves
        for move in state.GetMoves():
            #create a copy of current state
            newState = state.Clone()
            #apply move to state
            newState.DoMove(move)
            score = Minimax(newState, depth -1, False)
            if score > bestScore:
                bestScore = score
        return bestScore
    else:
        #It is Player's 2 turn so Minimise Score
        # Initialize with the largest possible value
        bestScore = float('inf')
        for move in state.GetMoves():
            newState = state.Clone()
            newState.DoMove(move)
            score = Minimax(newState, depth - 1, True) 
            # Update the best score if this move is worse for Player 1.
            if score < bestScore:
                bestScore = score
        return bestScore  # Return the lowest score found for Player 2.

def EvaluateState(state):
    score = 0  # Initialize the score.
    # Loop through the entire board.
    for x in range(state.width):  # x for colums
        for y in range(state.height):  # y for rows.
            if state.board[x][y] == 1:
                score += 1
            elif state.board[x][y] == 2:
                score -= 1
    return score

class Player1:
    def choose_move(self, state):
        """
        Determines the best move for Player 1 using the Minimax algorithm.
        :param state: Current game state.
        :return: The column index of the best move for Player 1.
        """
        bestMove = None  # Initialize the best move as None.
        bestScore = -float('inf')  # Start with the lowest possible score.
        # Loop through all possible moves.
        for move in state.GetMoves():
            newState = state.Clone()  # Create a copy of the current state to simulate the move.
            newState.DoMove(move)  # Apply the move to the copied state.
            # Call Minimax for Player 2's turn (depth reduced by 1).
            score = Minimax(newState, depth=4, maximizingPlayer=False)
            if score > bestScore:  # If the score is better than the current best score.
                bestScore = score  # Update the best score.
                bestMove = move  # Update the best move.
        return bestMove  # Return the column index of the best move.
