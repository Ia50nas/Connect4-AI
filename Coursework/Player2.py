import random
from math import sqrt, log

# The implementaion of MCTS for player 2 was designed and written by James Stovold and further adjusted to fit the coursework

class Node:
    """ Node of a game tree. A tree is a connected acyclic graph.
        Note: self.wins is from the perspective of playerJustMoved.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # Move that was taken to reach this game state 
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # Future childNodes
        self.playerJustMoved = state.playerJustMoved  # To check who won or who lost.

    def IsFullyExpanded(self):
        return self.untriedMoves == []

    def AddChild(self, move, state):
        """
        Adds a new child node to this Node. 
        :param move: (int) action taken by the player
        :param state: (GameState) state corresponding to new child node
        :returns: new expanded node added to the tree
        """
        node = Node(move=move, parent=self, state=state)
        self.untriedMoves.remove(move)
        self.childNodes.append(node)
        return node

    def Update(self, result):
        """
        Updates the node statistics saved in this node with the param result
         which is the information obtained during the latest rollout.
        :param result: (bool) 1 for victory, 0 for draw / loss.
        """
        self.visits += 1
        self.wins += result


def UCB1(node, child, exploration_constant=sqrt(2)):
    return child.wins / child.visits + exploration_constant * sqrt(log(node.visits) / child.visits)


def selection_phase(node, state, selection_policy=UCB1, selection_policy_args=[]):
    if not node.IsFullyExpanded() or node.childNodes == []:
        return node
    selected_node = sorted(node.childNodes, key=lambda child: selection_policy(node, child, *selection_policy_args))[-1]
    state.DoMove(selected_node.move)
    return selection_phase(selected_node, state)


def expansion_phase(node, state):
    if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
        move = random.choice(node.untriedMoves)
        state.DoMove(move)
        node = node.AddChild(move, state)
    return node


def rollout_phase(state):
    while state.GetMoves() != []:
        state.DoMove(random.choice(state.GetMoves()))


def backpropagation_phase(node, state):
    if node is not None:
        node.Update(state.GetResult(node.playerJustMoved))
        backpropagation_phase(node.parentNode, state)


def action_selection_phase(node):
    return sorted(node.childNodes, key=lambda c: c.wins / c.visits)[-1].move


def MCTS_UCT(rootstate, itermax, exploration_factor_ucb1=sqrt(2)):
    """ 
    Conducts a game tree search using the MCTS-UCT algorithm
    for a total of param itermax iterations. The search begins
    in the param rootstate. Assumes that 2 players are alternating
    with results being [0.0, 1.0].

    :param rootstate: The game state for which an action must be selected.
    :param itermax: number of MCTS iterations to be carried out. Also known as the computational budget.
    :returns: (int) Action that will be taken by an agent.
    """
    rootnode = Node(state=rootstate)
    
    for i in range(itermax):
        node  = rootnode
        state = rootstate.Clone()

        node  = selection_phase(node, state, selection_policy=UCB1, selection_policy_args=[exploration_factor_ucb1])

        node  = expansion_phase(node, state)
            
        rollout_phase(state)
            
        backpropagation_phase(node, state)
    
    return action_selection_phase(rootnode)


# Example `choose_move` method for a player
class Player2:
    def __init__(self, computational_budget):
        self.computational_budget = computational_budget

    def choose_move(self, state):
        return MCTS_UCT(state, self.computational_budget)
