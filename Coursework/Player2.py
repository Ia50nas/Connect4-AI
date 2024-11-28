import math
import random

# Extracted and refactored Player 2 class with MCTS logic integrated
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


def selection_phase(node, state):
    while node.IsFullyExpanded() and node.childNodes:
        node = sorted(node.childNodes, key=lambda child: UCB1(node, child))[-1]
        state.DoMove(node.move)
    return node


def expansion_phase(node, state):
    if node.untriedMoves:
        move = random.choice(node.untriedMoves)
        state.DoMove(move)
        node = node.AddChild(move, state)
    return node


def rollout_phase(state):
    while state.GetMoves():
        state.DoMove(random.choice(state.GetMoves()))


def backpropagation_phase(node, state):
    while node:
        node.Update(state.GetResult(node.playerJustMoved))
        node = node.parentNode


def MCTS_UCT(rootstate, itermax):
    rootnode = Node(state=rootstate)
    for _ in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        node = selection_phase(node, state)
        node = expansion_phase(node, state)
        rollout_phase(state)
        backpropagation_phase(node, state)
    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move


# Refactored Player 2 class
class Player2:
    def choose_move(self, state):
        """
        Uses MCTS to choose the best move for Player 2.
        :param state: Current game state
        :return: Best move (column index)
        """
        computational_budget = 1000  # Number of iterations for MCTS
        return MCTS_UCT(state, itermax=computational_budget)  # Best move chosen by MCTS

# Player2 class now integrated with MCTS logic. Let me know if you'd like further refinements!
