
def Minimax(state, depth, alpha, beta, maximizingPlayer):
    # If maximum depth is reached or the game is over, evaluate the current state
    if (depth == 0) or state.IsGameOver():
        return EvaluateState(state)

    if maximizingPlayer:
        # Maximizing Player 1's turn
        bestScore = -float('inf')
        for move in state.GetMoves():
            newState = state.Clone()  # Clone the state
            newState.DoMove(move)  # Apply the move
            score = Minimax(newState, depth - 1, alpha, beta, False)  # Recursive call for minimizing player
            bestScore = max(bestScore, score)
            alpha = max(alpha, score)  # Update alpha
            if beta <= alpha:  # Beta cut-off
                break
        return bestScore
    else:
        # Minimizing Player 2's turn
        bestScore = float('inf')
        for move in state.GetMoves():
            newState = state.Clone()  # Clone the state
            newState.DoMove(move)  # Apply the move
            score = Minimax(newState, depth - 1, alpha, beta, True)  # Recursive call for maximizing player
            bestScore = min(bestScore, score)
            beta = min(beta, score)  # Update beta
            if beta <= alpha:  # Alpha cut-off
                break
        return bestScore

def EvaluateState(state):
    """
    Higher scores favor Player 1; 
    lower scores favor Player 2.
    """
    score = 0
    center_column = state.width // 2

    # Central column bias: Encourage moves closer to the center
    for row in range(state.height):
        if state.board[center_column][row] == 1:  # Player 1's piece
            score += 3  
        elif state.board[center_column][row] == 2:  # Player 2's piece
            score -= 3

    # Evaluate all board positions
    for x in range(state.width):
        for y in range(state.height):
            if state.board[x][y] == 1:  # Player 1
                score += EvaluatePosition(state, x, y, 1)
            elif state.board[x][y] == 2:  # Player 2
                score -= EvaluatePosition(state, x, y, 2)

    return score


def EvaluatePosition(state, x, y, player):
    """
    Evaluates a specific position on the board for potential connections.
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # vertical, horizontal, diagonal
    position_score = 0

    for dx, dy in directions:
        count = 1  # Start with the current piece
        blocked_front = False
        blocked_back = False

        # Check forward direction
        step = 1
        while state.IsOnBoard(x + step * dx, y + step * dy):
            if state.board[x + step * dx][y + step * dy] == player:
                count += 1
            elif state.board[x + step * dx][y + step * dy] != 0:
                blocked_front = True
                break
            else:
                break
            step += 1

        # Check backward direction
        step = 1
        while state.IsOnBoard(x - step * dx, y - step * dy):
            if state.board[x - step * dx][y - step * dy] == player:
                count += 1
            elif state.board[x - step * dx][y - step * dy] != 0:
                blocked_back = True
                break
            else:
                break
            step += 1

        # Scoring for potential connections
        if count >= state.connect:  # Winning move
            position_score += 1000000
        elif count == state.connect - 1:  # Near-win
            if not (blocked_front and blocked_back):
                position_score += 100
        elif count == state.connect - 2:  # Building connections
            if not (blocked_front and blocked_back):
                position_score += 10

    return position_score



class Player1:
    def choose_move(self, state):
        bestMove = None  # Initialize the best move as None.
        bestScore = -float('inf')  # Start with the lowest possible score.
        alpha = -float('inf')  # Initialize alpha
        beta = float('inf')  # Initialize beta

        # Loop through all possible moves.
        for move in state.GetMoves():
            newState = state.Clone()  # Create a copy of the current state to simulate the move.
            newState.DoMove(move)  # Apply the move to the copied state.
            # Call Minimax for Player 2's turn (depth reduced by 1).
            score = Minimax(newState, depth=4, alpha=alpha, beta=beta, maximizingPlayer=False)
            if score > bestScore:  # If the score is better than the current best score.
                bestScore = score  # Update the best score.
                bestMove = move  # Update the best move.
            alpha = max(alpha, bestScore)  # Update alpha

        return bestMove  # Return the column index of the best move.
