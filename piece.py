import pygame
from common import *
import os

class Piece(pygame.sprite.Sprite):

    def __init__(self, character, isWhite, startingPosition=None):
        super().__init__()

        # parameters
        self.character = character
        self.colour = 'white' if isWhite else 'black'
        self.position = (0, 0) if (startingPosition is None) else startingPosition

        # piece size
        self.width = PIECE_WIDTH
        self.height = PIECE_WIDTH

        # load the image
        characterImagePath = os.path.join('images', f'{self.colour}_{self.character}.png')
        characterImage = pygame.image.load(characterImagePath)
        # scale the image
        self.image = pygame.transform.scale(characterImage, (self.width, self.height))

        # todo: draw actual image here

        self.rect = self.image.get_rect()
        # row placement
        self.rect.x = self.position[1] * TILE_WIDTH + BORDER_WIDTH
        # column placement
        self.rect.y = self.position[0] * TILE_WIDTH + BORDER_WIDTH

class Pawn(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'pawn'
        if startingPosition is None:
            row = 1 if isWhite else 6
            column = number - 1
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)

class Rook(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'rook'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 0 if (number == 1) else 7
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)

class Knight(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'knight'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 1 if (number == 1) else 6
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)

class Bishop(Piece):
    def __init__(self, isWhite, number=1, startingPosition=None):
        character = 'bishop'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 2 if (number == 1) else 5
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)

class King(Piece):
    def __init__(self, isWhite, startingPosition=None):
        character = 'king'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 3
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)

class Queen(Piece):
    def __init__(self, isWhite, startingPosition=None):
        character = 'queen'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 4
            startingPosition = (row, column)
        super().__init__(character, isWhite, startingPosition)


