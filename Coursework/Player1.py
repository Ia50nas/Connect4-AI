class Player1:
    def __init__(self, computational_budget):
        """
        Initialize Player 1 with a computational budget.
        :param computational_budget: Maximum number of evaluations allowed.
        """
        self.computational_budget = computational_budget
        self.evaluations = 0  # Track the number of evaluations performed

    def Minimax(self, state, depth, alpha, beta, maximizingPlayer):
        """
        Perform the Minimax search with alpha-beta pruning and budget tracking.
        :param state: The current game state.
        :param depth: The depth of the search.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param maximizingPlayer: True if it's the maximizing player's turn.
        :return: The evaluated score of the current state.
        """
        if depth == 0 or state.IsGameOver() or self.evaluations >= self.computational_budget:
            self.evaluations += 1  # Increment evaluation counter
            return EvaluateState(state)

        if maximizingPlayer:
            bestScore = -float('inf')
            for move in sorted(state.GetMoves(), key=lambda x: abs(x - state.width // 2)):
                if self.evaluations >= self.computational_budget:
                    break  # Stop if the budget is exceeded
                newState = state.Clone()
                newState.DoMove(move)
                score = self.Minimax(newState, depth - 1, alpha, beta, False)
                bestScore = max(bestScore, score)
                alpha = max(alpha, score)
                if beta <= alpha:  # Beta cut-off
                    break
            return bestScore
        else:
            bestScore = float('inf')
            for move in sorted(state.GetMoves(), key=lambda x: abs(x - state.width // 2)):
                if self.evaluations >= self.computational_budget:
                    break  # Stop if the budget is exceeded
                newState = state.Clone()
                newState.DoMove(move)
                score = self.Minimax(newState, depth - 1, alpha, beta, True)
                bestScore = min(bestScore, score)
                beta = min(beta, score)
                if beta <= alpha:  # Alpha cut-off
                    break
            return bestScore

    def choose_move(self, state):
        """
        Choose the best move using Minimax search, respecting the computational budget.
        :param state: The current game state.
        :return: The column index of the best move.
        """
        bestMove = None
        bestScore = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        self.evaluations = 0  # Reset evaluation counter

        # Determine dynamic depth based on game phase
        filled_cells = sum(sum(1 for cell in col if cell != 0) for col in state.board)
        total_cells = state.width * state.height
        game_phase = filled_cells / total_cells
        depth = 4 if game_phase < 0.5 else 6  # Increase depth in mid/late game

        for move in sorted(state.GetMoves(), key=lambda x: abs(x - state.width // 2)):
            if self.evaluations >= self.computational_budget:
                break  # Stop if the budget is exceeded
            newState = state.Clone()
            newState.DoMove(move)
            score = self.Minimax(newState, depth=depth, alpha=alpha, beta=beta, maximizingPlayer=False)
            if score > bestScore:
                bestScore = score
                bestMove = move
            alpha = max(alpha, bestScore)

        return bestMove


def EvaluateState(state):
    """
    Evaluate the current state of the board.
    A positive score favors Player 1, and a negative score favors Player 2.
    """
    score = 0
    center_column = state.width // 2

    # Game phase: Early, mid, or late based on board fill percentage
    filled_cells = sum(sum(1 for cell in col if cell != 0) for col in state.board)
    total_cells = state.width * state.height
    game_phase = filled_cells / total_cells  # 0 (early) to 1 (late)

    # Center column heuristic: Encourage center play in early game
    center_weight = 4 if game_phase < 0.5 else 2
    for row in range(state.height):
        if state.board[center_column][row] == 1:
            score += center_weight
        elif state.board[center_column][row] == 2:
            score -= center_weight

    # Evaluate all positions on the board
    for x in range(state.width):
        for y in range(state.height):
            if state.board[x][y] == 1:  # Player 1's piece
                score += EvaluatePosition(state, x, y, 1, game_phase)
            elif state.board[x][y] == 2:  # Player 2's piece
                score -= EvaluatePosition(state, x, y, 2, game_phase)

    return score


def EvaluatePosition(state, x, y, player, game_phase):
    """
    Evaluate the potential of a single position for the given player.
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Vertical, horizontal, diagonal
    position_score = 0

    for dx, dy in directions:
        count = 1
        blocked_front, blocked_back = False, False

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

        # Scoring for potential lines
        if count >= state.connect:  # Winning line
            position_score += 10000
        elif count == state.connect - 1 and not (blocked_front and blocked_back):  # Near-win
            position_score += 500 * (1 if game_phase > 0.5 else 2)
        elif count == state.connect - 2 and not (blocked_front and blocked_back):  # Building potential
            position_score += 50 * (1 if game_phase > 0.5 else 1.5)

    return position_score
