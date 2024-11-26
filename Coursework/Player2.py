import random

class Player2:
    def choose_move(self, state):
        """
        Logic for Player 2 to choose a move.
        :param state: Current game state
        :return: Selected move (column index)
        """
        return random.choice(state.GetMoves())
