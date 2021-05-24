import config
from collections import deque


class Game:
    def __init__(self) -> None:
        self.rows = config.BOARD_RESOLUTION[0]
        self.cols = config.BOARD_RESOLUTION[1]
        self.board = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.snapshot = [[None for i in range(self.cols)] for j in range(self.rows)]  # last snapshot of the board
        self.turn = 1
        self.log = []
        self.white_region_count = 0
        self.black_region_count = 0

    def pass_turn(self):
        self.log.append((self.turn, None, None))
        self.nextTurn()

    def play(self, r, c):
        if self.can_play(r, c):
            self.take_snapshot()
            self.log.append((self.turn, r, c))
            self.board[r][c] = self.turn
            self.nextTurn()
            paths = self.compute_captures()
            self.remove_paths((r, c), paths)

    def take_snapshot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.snapshot[i][j] = self.board[i][j]

    def can_play(self, r, c):
        # range check
        if r < 0 or r >= self.rows:
            return False
        if c < 0 or c >= self.cols:
            return False
        # needs to be empty cell
        if self.board[r][c] > 0:
            return False
        # make the move
        played = [[self.board[i][j] for j in range(self.cols)] for i in range(self.rows)]
        played[r][c] = self.turn
        paths = self.compute_captures(played)
        self.remove_paths((r, c), paths, played)
        # cannot play where no liberty
        if len(paths) == 1 and (r, c) in paths[0]:
            return False
        # no replay in Ko position
        for i in range(self.rows):
            for j in range(self.cols):
                if played[i][j] > 0 and self.snapshot[i][j] != played[i][j]:
                    return True
        return False

    def compute_scores(self):
        self.compute_territories()
        white_score = 0
        black_score = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 1 or self.board[i][j] == -1:
                    black_score += 1
                elif self.board[i][j] == 2 or self.board[i][j] == -2:
                    white_score += 1
        return black_score, white_score

    def game_over(self):
        if len(self.log) < 2:
            return False
        return self.log[-1][1] == None and self.log[-2][1] == None

    def remove_paths(self, last_played, paths, board=None):
        board = self.board if board == None else board
        if len(paths) > 1:
            for path in paths:
                if not last_played in path:
                    self.capture_stone(path, board)
        elif len(paths) == 1:
            path = paths[0]
            self.capture_stone(path, board)

    def capture_stone(self, path, board=None):
        board = self.board if board == None else board
        for r, c in path:
            board[r][c] = 0

    def compute_captures(self, board=None):
        board = self.board if board == None else board
        visited = set()
        paths = []
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] > 0 and not (i, j) in visited:
                    color = board[i][j]
                    liberties = set()
                    qq = deque()
                    path = [(i, j)]
                    qq.append((i, j))
                    visited.add((i, j))
                    while len(qq) != 0:
                        for neighbour in self.get_all_neighbours(qq.popleft()):
                            nr, nc = neighbour
                            if not neighbour in visited and board[nr][nc] == color:
                                qq.append(neighbour)
                                visited.add(neighbour)
                                path.append(neighbour)
                            elif board[nr][nc] <= 0:
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
