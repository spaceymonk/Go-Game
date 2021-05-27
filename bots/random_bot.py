from time import sleep
from random import randint


class RandomBot:
    def __init__(self, game) -> None:
        self.game = game
        self.status = False  # false: ready, true: thinking

    def play(self):
        self.status = True
        if len(self.game.log) > 0:
            t, r, c = self.game.log[-1]
            print(t, r, c)
            if r == None:
                self.game.pass_turn()
                self.status = False
                return
        # sleep(2)
        positions = self.get_available_positions()
        if len(positions) <= 1:
            self.game.pass_turn()
        else:
            pos = randint(0, len(positions)-1)
            self.game.play(positions[pos])
        self.status = False

    def get_available_positions(self):
        result = []
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                if self.game.can_play(i, j):
                    result.append((i, j))
        return result
