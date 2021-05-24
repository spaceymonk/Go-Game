import pygame
import config
from game import Game
from utility import *


class App:
    def __init__(self):
        self._running = False
        self.DISPLAYSURF = None
        self.refresh = False
        self.game = Game()

    def on_init(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode(config.SCREEN_RESOLUTION_WITH_GAPS)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            r, c = convertToBoardCoord(pygame.mouse.get_pos())
            self.game.play(r, c)
            self.game.compute_territories()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.game.pass_turn()
                if self.game.game_over():
                    self._running = False

    def on_loop(self):
        pygame.display.set_caption(f"Round: {len(self.game.gamelog)} B: {self.game.black_captures}/{self.game.black_region_count} W: {self.game.white_captures}/{self.game.white_region_count}")

    def on_render(self):
        # -------------------------------- draw board -------------------------------- #
        self.DISPLAYSURF.fill(config.GREEN)
        for i in range(config.BOARD_RESOLUTION[0]):
            xmin = i * config.STONE_SIZE + config.GAP_SIZE//2
            ymin = 0 + + config.GAP_SIZE//2
            xmax = i * config.STONE_SIZE + config.GAP_SIZE//2
            ymax = config.SCREEN_RESOLUTION[1] + config.GAP_SIZE//2
            pygame.draw.line(self.DISPLAYSURF, config.RED, (xmin, ymin), (xmax, ymax))
        for i in range(config.BOARD_RESOLUTION[1]):
            xmin = 0 + + config.GAP_SIZE//2
            ymin = i * config.STONE_SIZE + config.GAP_SIZE//2
            xmax = config.SCREEN_RESOLUTION[0] + config.GAP_SIZE//2
            ymax = i * config.STONE_SIZE + config.GAP_SIZE//2
            pygame.draw.line(self.DISPLAYSURF, config.RED, (xmin, ymin), (xmax, ymax))
        # -------------------------------- draw stones ------------------------------- #
        for i in range(config.BOARD_RESOLUTION[0]):
            for j in range(config.BOARD_RESOLUTION[1]):
                if self.game.board[i][j] == 2:
                    pygame.draw.circle(self.DISPLAYSURF, config.WHITE,
                                       (j * config.STONE_SIZE + config.GAP_SIZE//2,
                                        i * config.STONE_SIZE + config.GAP_SIZE//2),
                                       config.STONE_SIZE//2)
                if self.game.board[i][j] == 1:
                    pygame.draw.circle(self.DISPLAYSURF, config.BLACK,
                                       (j * config.STONE_SIZE + config.GAP_SIZE//2,
                                        i * config.STONE_SIZE + config.GAP_SIZE//2),
                                       config.STONE_SIZE//2)
                if self.game.board[i][j] == -1:
                    pygame.draw.circle(self.DISPLAYSURF, config.BLACK,
                                       (j * config.STONE_SIZE + config.GAP_SIZE//2,
                                        i * config.STONE_SIZE + config.GAP_SIZE//2),
                                       config.STONE_SIZE//8)
                if self.game.board[i][j] == -2:
                    pygame.draw.circle(self.DISPLAYSURF, config.WHITE,
                                       (j * config.STONE_SIZE + config.GAP_SIZE//2,
                                        i * config.STONE_SIZE + config.GAP_SIZE//2),
                                       config.STONE_SIZE//8)
        # --------------------------------- highlight -------------------------------- #
        if len(self.game.gamelog) != 0:
            t, r, c = self.game.gamelog[-1]
            if r != None:
                pygame.draw.circle(self.DISPLAYSURF, config.GRAY,
                                   (c * config.STONE_SIZE + config.GAP_SIZE//2,
                                    r * config.STONE_SIZE + config.GAP_SIZE//2),
                                   config.STONE_SIZE//2, config.STONE_SIZE//8)
            else:
                font = pygame.font.SysFont(None, 24)
                img = font.render(f'{"Black" if t==1 else "White"} passed', True, config.BLUE)
                self.DISPLAYSURF.blit(img, (5, 5))
        # ------------------------------- display time ------------------------------- #
        font = pygame.font.SysFont(None, 24)
        s = f"{pygame.time.get_ticks()//1000}"
        img = font.render(s, True, config.BLUE)
        self.DISPLAYSURF.blit(img, (config.SCREEN_RESOLUTION_WITH_GAPS[0]-font.size(s)[0]-5, 5))
        # --------------------------------- hovering --------------------------------- #
        r, c = convertToBoardCoord(pygame.mouse.get_pos())
        if self.game.can_play(r, c):
            pygame.draw.circle(self.DISPLAYSURF, config.WHITE if self.game.turn == 2 else config.BLACK,
                               (c * config.STONE_SIZE + config.GAP_SIZE//2,
                                r * config.STONE_SIZE + config.GAP_SIZE//2),
                               config.STONE_SIZE//4)
        pygame.display.flip()

    def on_cleanup(self):
        print('Game finished.')
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
