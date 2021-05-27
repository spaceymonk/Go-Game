# ---------------------------------------------------------------------------- #
#                                 game settings                                #
# ---------------------------------------------------------------------------- #

BOARD_RESOLUTION = (9, 9)

# 1 - one player (computer vs player)
# 2 - two player (player vs player)
GAMEMODE = 2

# 1 - player will be black
# 2 - player will be white
PLAYER = 1

# ---------------------------------------------------------------------------- #
#                               display settings                               #
# ---------------------------------------------------------------------------- #

STONE_SIZE = 40
GAP_SIZE = 80
SCREEN_RESOLUTION = ((BOARD_RESOLUTION[0]-1) * STONE_SIZE, (BOARD_RESOLUTION[1]-1) * STONE_SIZE)
SCREEN_RESOLUTION_WITH_GAPS = (SCREEN_RESOLUTION[0]+GAP_SIZE, SCREEN_RESOLUTION[1]+GAP_SIZE)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
