import config
from collections import deque


class Game:
    def __init__(self) -> None:
        self.rows = config.BOARD_RESOLUTION[0]
        self.cols = config.BOARD_RESOLUTION[1]
        self.board = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.turn = 1
        self.gamelog = []
        self.white_captures = 0
        self.black_captures = 0
        self.white_region_count = 0
        self.black_region_count = 0

    def pass_turn(self):
        self.gamelog.append((self.turn, None, None))
        self.nextTurn()

    def play(self, r, c):
        if self.can_play(r, c):
            self.gamelog.append((self.turn, r, c))
            self.board[r][c] = self.turn
            self.nextTurn()
            paths = self.compute_captures()
            if len(paths) > 1:
                for path in paths:
                    if not (r, c) in path:
                        self.capture_stone(path)
            elif len(paths) == 1:
                path = paths[0]
                self.capture_stone(path)

    def can_play(self, r, c):
        # range check
        if r < 0 or r >= self.rows:
            return False
        if c < 0 or c >= self.cols:
            return False
        # needs to be empty cell
        if self.board[r][c] > 0:
            return False
        # cannot play where no liberty
        tmp = self.board[r][c]
        self.board[r][c] = self.turn
        paths = self.compute_captures()
        self.board[r][c] = tmp
        if len(paths) == 1 and (r, c) in paths[0]:
            return False
        # no replay in Ko position
        # todo
        return True

    def game_over(self):
        if len(self.gamelog) < 2:
            return False
        return self.gamelog[-1][1] == None and self.gamelog[-2][1] == None

    def capture_stone(self, p):
        for r, c in p:
            if self.board[r][c] == 1:
                self.white_captures += 1
            if self.board[r][c] == 2:
                self.black_captures += 1
            self.board[r][c] = 0

    def compute_captures(self):
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
                        for neighbour in self.get_all_neighbours(qq.popleft()):
                            nr, nc = neighbour
                            if not neighbour in visited and self.board[nr][nc] == color:
                                qq.append(neighbour)
                                visited.add(neighbour)
                                path.append(neighbour)
                            elif self.board[nr][nc] <= 0:
                                liberties.add(neighbour)
                    if len(liberties) == 0:
                        paths.append(path)
        return paths

    def get_all_neighbours(self, r_c):
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
        self.white_region_count = 0
        self.black_region_count = 0
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
                        for nr, nc in self.get_all_neighbours(qq.popleft()):
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
                        if valid:
                            self.board[r][c] = -current_color
                            if current_color == 1:
                                self.black_region_count += 1
                            if current_color == 2:
                                self.white_region_count += 1
                        else:
                            self.board[r][c] = 0

    def nextTurn(self):
        self.turn = 1 if self.turn == 2 else 2
