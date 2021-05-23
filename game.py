import config
from collections import deque


class Game:
    def __init__(self) -> None:
        self.rows = config.BOARD_RESOLUTION[0]
        self.cols = config.BOARD_RESOLUTION[1]
        self.board = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.turn = 1
        self.round = 0
        self.white_captures = []
        self.black_captures = []

    def play(self, r, c):
        if self.canPlay(r, c):
            self.round += 1
            self.board[r][c] = self.turn
            self.nextTurn()
            self.compute_captures((r, c))

    def canPlay(self, r, c):
        if r < 0 or r >= self.rows:
            return False
        if c < 0 or c >= self.cols:
            return False
        if self.board[r][c] > 0:
            return False
        return True

    def compute_captures(self, played):
        def remove_cells(p):
            for r, c in p:
                if self.board[r][c] == 1:
                    self.white_captures.append((r, c))
                if self.board[r][c] == 2:
                    self.black_captures.append((r, c))
                self.board[r][c] = 0
        visited = set()
        paths = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] > 0 and not (i, j) in visited:
                    color = self.board[i][j]
                    liberties = set()
                    qq = deque()
                    path = [(i, j)]
                    qq.append((i, j))
                    visited.add((i, j))
                    while len(qq) != 0:
                        for liberty in self.get_all_liberties(qq.popleft()):
                            if not liberty in visited and self.board[liberty[0]][liberty[1]] == color:
                                qq.append(liberty)
                                visited.add(liberty)
                                path.append(liberty)
                            elif self.board[liberty[0]][liberty[1]] <= 0:
                                liberties.add(liberty)
                    if len(liberties) == 0:
                        paths.append(path)
        if len(paths) > 1:
            for path in paths:
                if not played in path:
                    remove_cells(path)
        elif len(paths) == 1:
            path = paths[0]
            remove_cells(path)

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
