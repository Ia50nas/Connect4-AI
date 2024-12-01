import colorama
from colorama import Fore, Back
from Player1 import Player1
from Player2 import Player2

class GameState:
    def __init__(self):
        self.playerJustMoved = 2  # Game starts with Player 1.

    def Clone(self):
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        pass

    def IsGameOver(self):
        return self.GetMoves() == []

    def GetResult(self, player):
        pass


class Connect4State(GameState):
    def __init__(self, width=7, height=6, connect=4):
        super().__init__()
        self.winner = 0
        self.width = width
        self.height = height
        self.connect = connect
        self.InitializeBoard()

    def InitializeBoard(self):
        self.board = [[0] * self.height for _ in range(self.width)]

    def Clone(self):
        st = Connect4State(width=self.width, height=self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = [self.board[col][:] for col in range(self.width)]
        return st

    def DoMove(self, movecol):
        assert 0 <= movecol < self.width and self.board[movecol][self.height - 1] == 0
        row = self.height - 1
        while row >= 0 and self.board[movecol][row] == 0:
            row -= 1
        row += 1
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[movecol][row] = self.playerJustMoved
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved

    def GetMoves(self):
        if self.winner != 0:
            return []
        return [col for col in range(self.width) if self.board[col][self.height - 1] == 0]

    def DoesMoveWin(self, x, y):
        me = self.board[x][y]
        for (dx, dy) in [(0, 1), (1, 1), (1, 0), (1, -1)]:
            p = 1
            while self.IsOnBoard(x + p * dx, y + p * dy) and self.board[x + p * dx][y + p * dy] == me:
                p += 1
            n = 1
            while self.IsOnBoard(x - n * dx, y - n * dy) and self.board[x - n * dx][y - n * dy] == me:
                n += 1
            if p + n >= self.connect + 1:
                return True
        return False

    def IsOnBoard(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def GetResult(self, player):
        return player == self.winner

    def __repr__(self):
        s = ""
        for x in range(self.height - 1, -1, -1):
            for y in range(self.width):
                s += [Back.WHITE + Fore.WHITE + '.', Back.BLACK + Fore.WHITE + 'X', Back.BLACK + Fore.WHITE + 'O'][self.board[y][x]]
                s += Fore.RESET
                s += Back.RESET
            s += "\n"
        s += "\n\n\n"
        return s


def PrintGameResults(state):
    if state.winner != 0:
        if state.GetResult(state.playerJustMoved) == 1.0:
            print(str(state))
            print(f"Player {state.playerJustMoved} wins!")
        else:
            print(str(state))
            print(f"Player {3 - state.playerJustMoved} wins!")
    else:
        print("Nobody wins!")


def PlayGame(initialState):
    state = initialState
    computational_budget = 100  # Set a shared budget for both players
    player1 = Player1(computational_budget=computational_budget)
    player2 = Player2(computational_budget=computational_budget)
    while not state.IsGameOver():
        print(str(state))
        if state.playerJustMoved == 1:
            move = player2.choose_move(state)
        else:
            move = player1.choose_move(state)
        state.DoMove(move)
    PrintGameResults(state)



if __name__ == "__main__":
    colorama.init()
    env = Connect4State(width=7, height=6)
    PlayGame(env)
