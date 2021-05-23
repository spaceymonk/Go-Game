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


def get_all_liberties(r_c):
    r, c = r_c
    neighbours = []
    # if inBoardRange(x - 1, y - 1):
    #     neighbours.append((x - 1, y - 1))
    if inBoardRange(r - 0, c - 1):
        neighbours.append((r - 0, c - 1))
    # if inBoardRange(r + 1, c - 1):
    #     neighbours.append((r + 1, c - 1))
    # if inBoardRange(r - 1, c + 1):
    #     neighbours.append((r - 1, c + 1))
    if inBoardRange(r - 0, c + 1):
        neighbours.append((r - 0, c + 1))
    # if inBoardRange(r + 1, c + 1):
    #     neighbours.append((r + 1, c + 1))
    if inBoardRange(r - 1, c - 0):
        neighbours.append((r - 1, c - 0))
    if inBoardRange(r + 1, c - 0):
        neighbours.append((r + 1, c - 0))
    return neighbours
