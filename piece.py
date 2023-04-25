import pygame as game
from common import *
import os

class Piece(game.sprite.Sprite):

    def __init__(self, character, isWhite, startingPosition=None):
        super().__init__()

        # placement parameters
        self.character = character
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
        self.snapToTile(self.position)

        # base pieces have no valid moves
        self.validMoves = []

        # basics
        self.captured = False

    def snapToTile(self, tile):
        self.rect.x = tile[COL_INDEX] * TILE_WIDTH + BORDER_WIDTH
        self.rect.y = tile[ROW_INDEX] * TILE_WIDTH + BORDER_WIDTH

    def setCords(self, cords):
        self.rect.x = cords[0]
        self.rect.y = cords[1]

    def getCurrentTile(self):
        return cordsToTile(self.rect.x, self.rect.y)

    def getCurrentCords(self):
        return self.rect.x, self.rect.y

    def detectCollision(self, cords):
        return self.rect.collidepoint(cords[0], cords[1])


class Pawn(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'pawn'
        if startingPosition is None:
            row = 1 if isWhite else 6
            column = number - 1
            startingPosition = (column, row)
        else:
            row = startingPosition[ROW_INDEX]
            column = startingPosition[COL_INDEX]
        super().__init__(character, isWhite, startingPosition)

        self.firstMoveMade = False

        # define initial valid moves
        self.validMoves.append((column - 1 if isWhite else column + 1, row))
        self.validMoves.append((column - 2 if isWhite else column + 2, row))

    def isValidMove(self, newPosition):
        if newPosition is None:
            return False
        if newPosition in self.validMoves:
            return True
        return False

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
