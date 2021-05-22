import config
from objects import Stone


class Game:
    def __init__(self) -> None:
        self.stones = []
        self.turn = config.BLACK

    def play(self, r, c):
        if self.canPlay(r, c):
            self.stones.append(Stone(self.turn, r, c))
            self.turn = config.WHITE if self.turn == config.BLACK else config.BLACK

    def canPlay(self, r, c):
        if r < 0 or r >= config.BOARD_RESOLUTION[0]:
            return False
        if c < 0 or c >= config.BOARD_RESOLUTION[1]:
            return False
        for stone in self.stones:
            if r == stone.row and c == stone.col:
                return False
        return True

    def get_territories(self):
        visited = []
        for x in range(config.BOARD_RESOLUTION[0]):
            for y in range(config.BOARD_RESOLUTION[1]):
                if not (x, y) in visited and not (x, y) in [(s.row, s.col) for s in self.stones]:
                    pass
