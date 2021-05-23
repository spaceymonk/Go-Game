import config


def convertToBoardCoord(x_y):
    x, y = x_y
    col = (x - config.GAP_SIZE//2 + config.STONE_SIZE//2) // config.STONE_SIZE
    row = (y - config.GAP_SIZE//2 + config.STONE_SIZE//2) // config.STONE_SIZE
    return (row, col)
