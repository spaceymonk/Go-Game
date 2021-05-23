import config
from utility import *


class Game:
    def __init__(self) -> None:
        self.board = [[0 for i in range(config.BOARD_RESOLUTION[1])] for j in range(config.BOARD_RESOLUTION[0])]
        self.turn = 1

    def play(self, r, c):
        if self.canPlay(r, c):
            self.board[r][c] = self.turn
            self.nextTurn()

    def canPlay(self, r, c):
        if r < 0 or r >= config.BOARD_RESOLUTION[0]:
            return False
        if c < 0 or c >= config.BOARD_RESOLUTION[1]:
            return False
        if self.board[r][c] > 0:
            return False
        return True

    def get_territories(self, color):
        pass

    def nextTurn(self):
        self.turn = 1 if self.turn == 2 else 2
