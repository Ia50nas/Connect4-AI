import math
import random

class Node:
    """
    Node of a game tree. A tree is a connected acyclic graph.
    Note: self.wins is from the perspective of playerJustMoved.
    """
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # Move taken to reach this game state
        self.parentNode = parent  # None for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # Future childNodes
        self.playerJustMoved = state.playerJustMoved

    def IsFullyExpanded(self):
        return self.untriedMoves == []

    def AddChild(self, move, state):
        node = Node(move=move, parent=self, state=state)
        self.untriedMoves.remove(move)
        self.childNodes.append(node)
        return node

    def Update(self, result):
        self.visits += 1
        self.wins += result


def UCB1(node, child, exploration_constant=math.sqrt(2)):
    return child.wins / child.visits + exploration_constant * math.sqrt(math.log(node.visits) / child.visits)


class Player2:
    def __init__(self, computational_budget):
        """
        Initialize Player 2 with a computational budget.
        :param computational_budget: Maximum number of iterations for MCTS.
        """
        self.computational_budget = computational_budget

    def MCTS_UCT(self, rootstate):
        """
        Perform MCTS with a given computational budget.
        :param rootstate: The root game state.
        :return: The best move determined by MCTS.
        """
        rootnode = Node(state=rootstate)
        for _ in range(self.computational_budget):
            node = rootnode
            state = rootstate.Clone()
            node = self.selection_phase(node, state)
            node = self.expansion_phase(node, state)
            self.rollout_phase(state)
            self.backpropagation_phase(node, state)
        return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move

    def selection_phase(self, node, state):
        while node.IsFullyExpanded() and node.childNodes:
            node = sorted(node.childNodes, key=lambda child: UCB1(node, child))[-1]
            state.DoMove(node.move)
        return node

    def expansion_phase(self, node, state):
        if node.untriedMoves:
            move = random.choice(node.untriedMoves)
            state.DoMove(move)
            node = node.AddChild(move, state)
        return node

    def rollout_phase(self, state):
        while state.GetMoves():
            state.DoMove(random.choice(state.GetMoves()))

    def backpropagation_phase(self, node, state):
        while node:
            node.Update(state.GetResult(node.playerJustMoved))
            node = node.parentNode

    def choose_move(self, state):
        """
        Use MCTS to choose the best move for Player 2.
        :param state: Current game state.
        :return: Best move (column index).
        """
        return self.MCTS_UCT(state)
