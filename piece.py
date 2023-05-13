import pygame as game
from common import *
import os

class Piece(game.sprite.Sprite):

    def __init__(self, character, isWhite, startingPosition=None):
        super().__init__()

        # placement parameters
        self.character = character
        self.isWhite = True if isWhite else False
        self.colour = 'white' if isWhite else 'black'
        self.position = (0, 0) if (startingPosition is None) else startingPosition

        # piece size
        self.width = PIECE_WIDTH
        self.height = PIECE_WIDTH

        # load the image
        characterImagePath = os.path.join('images', f'{self.colour}_{self.character}.png')
        characterImage = game.image.load(characterImagePath)
        # scale the image
        self.image = game.transform.scale(characterImage, (self.width, self.height))

        # place the image (as a rectangle) at its starting position
        self.rect = self.image.get_rect()
        self.updateTilePosition(self.position)

        # base pieces have no valid moves
        self.validMoves = []

        # some pieces have special privileges on their first move
        self.firstMoveMade = False

        # define initial valid moves
        self.calculateNewValidMoves()

    def getPosition(self):
        return self.position

    def getPositionColumn(self):
        return self.getPosition()[COL_INDEX]

    def getPositionRow(self):
        return self.getPosition()[ROW_INDEX]

    def getCurrentTile(self):
        return cordsToTile(self.rect.x, self.rect.y)

    def getCurrentColumn(self):
        return self.getCurrentTile()[COL_INDEX]

    def getCurrentRow(self):
        return self.getCurrentTile()[ROW_INDEX]

    def getCurrentCords(self):
        return self.rect.x, self.rect.y

    def detectCollision(self, cords):
        return self.rect.collidepoint(cords[0], cords[1])

    def snapToTile(self, tile):
        self.rect.x = tile[COL_INDEX] * TILE_WIDTH + BORDER_WIDTH
        self.rect.y = tile[ROW_INDEX] * TILE_WIDTH + BORDER_WIDTH

    def updateTilePosition(self, tile):
        self.snapToTile(tile)
        self.position = cordsToTile(self.rect.x, self.rect.y)

    def goBackToPosition(self):
        self.snapToTile(self.position)

    def setCords(self, cords):
        self.rect.x = cords[0]
        self.rect.y = cords[1]

    def isValidMove(self, tile):
        if tile is None:
            return False
        if tile in self.validMoves:
            return True
        return False

    def calculateNewValidMoves(self):
        self.validMoves = []

    def addNewValidMove(self, tile):
        if tile[COL_INDEX] < 0 or tile[COL_INDEX] >= TILE_COUNT:
            return
        if tile[ROW_INDEX] < 0 or tile[ROW_INDEX] >= TILE_COUNT:
            return
        self.validMoves.append(tile)

    def move(self, tile):
        self.firstMoveMade = True

        # move to new tile
        self.updateTilePosition(tile)

        # calculate new valid moves
        self.calculateNewValidMoves()


class Pawn(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'pawn'
        if startingPosition is None:
            row = 1 if isWhite else 6
            column = number - 1
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + 1 if self.isWhite else self.getPositionRow() - 1))
        if self.firstMoveMade is not True:
            self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + 2 if self.isWhite else self.getPositionRow() - 2))

class Rook(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'rook'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 0 if (number == 1) else 7
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)

class Knight(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'knight'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 1 if (number == 1) else 6
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        self.addNewValidMove((self.getPositionColumn() + 2, self.getPositionRow() + 1))
        self.addNewValidMove((self.getPositionColumn() + 2, self.getPositionRow() - 1))
        self.addNewValidMove((self.getPositionColumn() - 2, self.getPositionRow() + 1))
        self.addNewValidMove((self.getPositionColumn() - 2, self.getPositionRow() - 1))
        self.addNewValidMove((self.getPositionColumn() - 1, self.getPositionRow() + 2))
        self.addNewValidMove((self.getPositionColumn() + 1, self.getPositionRow() + 2))
        self.addNewValidMove((self.getPositionColumn() - 1, self.getPositionRow() - 2))
        self.addNewValidMove((self.getPositionColumn() + 1, self.getPositionRow() - 2))


class Bishop(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'bishop'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 2 if (number == 1) else 5
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)

class King(Piece):
    def __init__(self, isWhite, startingPosition=None):
        character = 'king'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 3
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)

class Queen(Piece):
    def __init__(self, isWhite, startingPosition=None):
        character = 'queen'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 4
            startingPosition = (column, row)
        super().__init__(character, isWhite, startingPosition)
