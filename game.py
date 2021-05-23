import config
from collections import deque


class Game:
    def __init__(self) -> None:
        self.rows = config.BOARD_RESOLUTION[0]
        self.cols = config.BOARD_RESOLUTION[1]
        self.board = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.turn = 1
        self.round = 0

    def play(self, r, c):
        if self.canPlay(r, c):
            self.round += 1
            self.board[r][c] = self.turn
            self.nextTurn()

    def canPlay(self, r, c):
        if r < 0 or r >= self.rows:
            return False
        if c < 0 or c >= self.cols:
            return False
        if self.board[r][c] > 0:
            return False
        return True

    def get_all_liberties(self, r_c):
        def inBoardRange(x, y): return not (x < 0 or y < 0 or x >= self.rows or y >= self.cols)
        r, c = r_c
        neighbours = []
        if inBoardRange(r - 0, c - 1):
            neighbours.append((r - 0, c - 1))
        if inBoardRange(r - 0, c + 1):
            neighbours.append((r - 0, c + 1))
        if inBoardRange(r - 1, c - 0):
            neighbours.append((r - 1, c - 0))
        if inBoardRange(r + 1, c - 0):
            neighbours.append((r + 1, c - 0))
        return neighbours

    def get_available_liberties(self, r_c):
        libs = self.get_all_liberties(r_c)
        r, c = r_c
        avail = []
        for lib in libs:
            lr, lc = lib
            if self.board[r][c] == self.board[lr][lc]:
                avail.append(lib)
        return avail

    def compute_territories(self):
        if self.round <= 1:
            return
        visited = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] <= 0 and not (i, j) in visited:
                    valid = True
                    path = []
                    qq = deque()
                    qq.append((i, j))
                    visited.add((i, j))
                    path.append((i, j))
                    current_color = 0
                    color_picked = False
                    while len(qq) != 0:
                        for nr, nc in self.get_all_liberties(qq.popleft()):
                            if not color_picked and self.board[nr][nc] > 0:
                                current_color = self.board[nr][nc]
                                color_picked = True
                            if color_picked and self.board[nr][nc] == 1 and current_color == 2:
                                valid = False
                            if color_picked and self.board[nr][nc] == 2 and current_color == 1:
                                valid = False
                            if not (nr, nc) in visited:
                                if self.board[nr][nc] <= 0:
                                    visited.add((nr, nc))
                                    qq.append((nr, nc))
                                    path.append((nr, nc))
                    for r, c in path:
                        self.board[r][c] = -current_color if valid else 0

    def nextTurn(self):
        self.turn = 1 if self.turn == 2 else 2
