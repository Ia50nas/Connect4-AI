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
        Perform the Minimax search with alpha-beta pruning and move sorting.
        :param state: The current game state.
        :param depth: The depth of the search.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param maximizingPlayer: True if it's the maximizing player's turn.
        :return: The evaluated score of the current state.
        """
        if depth == 0 or state.IsGameOver() or self.evaluations >= self.computational_budget:
            self.evaluations += 1
            return self.EvaluateState(state)

        moves = state.GetMoves()
        # Sort moves to prioritize central positions
        moves = sorted(moves, key=lambda move: -abs(move - state.width // 2))

        if maximizingPlayer:
            bestScore = -float('inf')
            for move in moves:
                if self.evaluations >= self.computational_budget:
                    break
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
            for move in moves:
                if self.evaluations >= self.computational_budget:
                    break
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

        # Determine dynamic depth based on computational budget
        depth = self.calculate_depth(self.computational_budget)

        # Defensive move priority
        for move in state.GetMoves():
            new_state = state.Clone()
            new_state.DoMove(move)
            if new_state.DoesMoveWin(move, 0):  # Prevent Player 2's win
                return move  # Immediately block the threat

        # Evaluate moves
        for move in sorted(state.GetMoves(), key=lambda x: abs(x - state.width // 2)):
            if self.evaluations >= self.computational_budget:
                break
            newState = state.Clone()
            newState.DoMove(move)
            score = self.Minimax(newState, depth=depth, alpha=alpha, beta=beta, maximizingPlayer=False)
            if score > bestScore:
                bestScore = score
                bestMove = move
            alpha = max(alpha, bestScore)

        return bestMove

    def calculate_depth(self, budget, branching_factor=7):
        """
        Calculate the maximum depth based on the computational budget.
        """
        depth = 0
        total_evaluations = 0
        while total_evaluations < budget:
            total_evaluations = (branching_factor**(depth + 1) - 1) // (branching_factor - 1)
            if total_evaluations > budget:
                break
            depth += 1
        return depth - 1

    def EvaluateState(self, state):
        """
        Enhanced evaluation function for Player1.
        Evaluates the board state based on opportunities, threats, and forks.
        """
        score = 0
        center_column = state.width // 2

        # Center control weighting
        center_weight = 4
        for row in range(state.height):
            if state.board[center_column][row] == 1:
                score += center_weight
            elif state.board[center_column][row] == 2:
                score -= center_weight

        # Evaluate each cell for both players
        for x in range(state.width):
            for y in range(state.height):
                if state.board[x][y] == 1:  # Player 1's piece
                    score += self.EvaluatePosition(state, x, y, 1)
                elif state.board[x][y] == 2:  # Player 2's piece
                    score -= self.EvaluatePosition(state, x, y, 2)

        return score

    def EvaluatePosition(self, state, x, y, player):
        """
        Evaluate the potential of a single position for the given player.
        Considers threats, opportunities, and forks.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Vertical, horizontal, diagonal
        position_score = 0
        opponent = 3 - player

        for dx, dy in directions:
            count = 1
            blocked_front, blocked_back = False, False

            # Check forward direction
            step = 1
            while state.IsOnBoard(x + step * dx, y + step * dy):
                if state.board[x + step * dx][y + step * dy] == player:
                    count += 1
                elif state.board[x + step * dx][y + step * dy] == opponent:
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
                elif state.board[x - step * dx][y - step * dy] == opponent:
                    blocked_back = True
                    break
                else:
                    break
                step += 1

            # Scoring based on count and blocked status
            if count >= state.connect:
                position_score += 10000  # Winning line
            elif count == state.connect - 1 and not (blocked_front and blocked_back):
                position_score += 500  # Offensive near-win
            elif count == state.connect - 2 and not (blocked_front and blocked_back):
                position_score += 50  # Building potential

            # Reduced penalty for unblocked threats to balance defense/offense
            if count == state.connect - 1 and (blocked_front or blocked_back):
                position_score -= 300  # Less harsh penalty for threats

        return position_score