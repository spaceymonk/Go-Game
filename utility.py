import config


def convertToBoardCoord(x_y):
    x, y = x_y
    col = (x - config.GAP_SIZE//2 + config.STONE_SIZE//2) // config.STONE_SIZE
    row = (y - config.GAP_SIZE//2 + config.STONE_SIZE//2) // config.STONE_SIZE
    return (row, col)


def inBoardRange(x, y):
    if x < 0 or y < 0 or x >= config.BOARD_RESOLUTION[0] or y >= config.BOARD_RESOLUTION[1]:
        return False
    return True


def get_available_neighbours(x_y):
    x, y = x_y
    neighbours = []
    if inBoardRange(x - 1, y - 1):
        neighbours.append((x - 1, y - 1))
    if inBoardRange(x - 0, y - 1):
        neighbours.append((x - 0, y - 1))
    if inBoardRange(x + 1, y - 1):
        neighbours.append((x + 1, y - 1))
    if inBoardRange(x - 1, y + 1):
        neighbours.append((x - 1, y + 1))
    if inBoardRange(x - 0, y + 1):
        neighbours.append((x - 0, y + 1))
    if inBoardRange(x + 1, y + 1):
        neighbours.append((x + 1, y + 1))
    if inBoardRange(x - 1, y - 0):
        neighbours.append((x - 1, y - 0))
    if inBoardRange(x + 1, y - 0):
        neighbours.append((x + 1, y - 0))
    return neighbours