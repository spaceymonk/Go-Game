import pygame
import config


class Stone:

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    def draw(self, display):
        pygame.draw.circle(display, self.color,
                           (self.col * config.STONE_SIZE + config.GAP_SIZE//2,
                            self.row * config.STONE_SIZE + config.GAP_SIZE//2),
                           config.STONE_SIZE//2)
