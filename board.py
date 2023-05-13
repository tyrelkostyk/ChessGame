from common import *

class Board:

    def __init__(self):
        # create 2D board array
        self.board = [[None for _ in range(TILE_COUNT)] for _ in range(TILE_COUNT)]

    def getPieceAtTile(self, tile):
        return self.board[tile[ROW_INDEX]][tile[COL_INDEX]]

    def isTileOccupied(self, tile):
        return self.getPieceAtTile(tile) is not None

    def addPieceAtTile(self, piece, tile):
        self.board[tile[ROW_INDEX]][tile[COL_INDEX]] = piece

    def movePieceToTile(self, piece, startingTile, endingTile):
        self.board[startingTile[ROW_INDEX]][startingTile[COL_INDEX]] = None
        self.board[endingTile[ROW_INDEX]][endingTile[COL_INDEX]] = piece



