## misc
COL_INDEX = 0
ROW_INDEX = 1
LEFT_MOUSE_BUTTON = 1

## colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BROWN = (245, 222, 179)
DARK_BROWN = (139, 69, 19)

## tiles
LIGHT_TILE_COLOUR = LIGHT_BROWN
DARK_TILE_COLOUR = DARK_BROWN
TILE_COUNT = 8
WINDOW_WIDTH = 640
TILE_WIDTH = WINDOW_WIDTH // TILE_COUNT
BORDER_WIDTH = TILE_WIDTH // 10 * 2
PIECE_WIDTH = TILE_WIDTH - (2 * BORDER_WIDTH)

## turn & time
turnNumber = 0

## tile functions
def cordsToTile(x, y):
    row = y // TILE_WIDTH
    col = x // TILE_WIDTH
    return col, row

def isTileInRange(tile):
    if tile is None:
        return False
    if tile[COL_INDEX] < 0 or tile[COL_INDEX] >= TILE_COUNT:
        return False
    if tile[ROW_INDEX] < 0 or tile[ROW_INDEX] >= TILE_COUNT:
        return False
    return True

## turn & time functions

def incrementTurnNumber():
    global turnNumber
    turnNumber = turnNumber + 1

def getTurnNumber():
    global turnNumber
    return turnNumber

