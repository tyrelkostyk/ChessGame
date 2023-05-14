import pygame as game
from typing import Optional
import os

from common import *
from board import Board

class Piece(game.sprite.Sprite):

    def __init__(self, character, isWhite, board, startingPosition=None):
        super().__init__()

        # keep a reference to the board
        self.board: Optional[Board] = board

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

        # place the piece (and its image) at the starting position
        self.rect = self.image.get_rect()
        self.updateTilePosition(self.position)
        self.board.addPieceAtTile(self, self.position)

        # base pieces have no valid moves or attacks
        self.validMoves = []
        self.validAttacks = []

        # some pieces have special privileges on their first move
        self.firstMoveMade = False

        # pawns can be captured via en passant after moving 2 pieces at once
        self.enPassantRisk = False

        # define initial valid moves
        self.calculateNewValidMoves()

    def getIsWhite(self):
        return self.isWhite

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
        self.board.movePieceToTile(self, self.getPosition(), tile)
        self.snapToTile(tile)
        self.position = cordsToTile(self.rect.x, self.rect.y)

    def goBackToPosition(self):
        self.snapToTile(self.position)

    def setCords(self, cords):
        self.rect.x = cords[0]
        self.rect.y = cords[1]

    def isValidMove(self, tile):
        if not isTileInRange(tile):
            return False
        if tile in self.validMoves:
            return True
        return False

    def isValidAttack(self, tile):
        if not isTileInRange(tile):
            return False
        if tile in self.validAttacks:
            return True
        return False

    def isOpenToEnPassant(self):
        return self.enPassantRisk

    def calculateNewValidMoves(self):
        self.validMoves = []

    def addNewValidMove(self, tile):
        if not isTileInRange(tile):
            return False
        if self.board.isTileOccupied(tile):
            if self.board.getPieceAtTile(tile).getIsWhite() != self.isWhite:
                self.validAttacks.append(tile)
            return False
        self.validMoves.append(tile)
        return True

    def move(self, tile):
        self.firstMoveMade = True
        # move to new tile
        self.updateTilePosition(tile)


class Pawn(Piece):
    def __init__(self, isWhite, board, number=1, startingPosition=None):
        character = 'pawn'
        if startingPosition is None:
            row = 1 if isWhite else 6
            column = number - 1
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        direction = 1 if self.isWhite else -1
        # travel forward 1 square
        if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + (1 * direction))):
            # travel forward 2 squares
            if self.firstMoveMade is not True:
                self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + (2 * direction)))
        # capture diagonally
        self.addNewValidAttack((self.getPositionColumn() + 1, self.getPositionRow() + (1 * direction)))
        self.addNewValidAttack((self.getPositionColumn() - 1, self.getPositionRow() + (1 * direction)))

    def addNewValidMove(self, tile):
        if not isTileInRange(tile):
            return False
        if self.board.isTileOccupied(tile):
            return False
        self.validMoves.append(tile)
        return True

    def addNewValidAttack(self, tile):
        if not isTileInRange(tile):
            return False
        if self.board.isTileOccupied(tile):
            if self.board.getPieceAtTile(tile).getIsWhite() != self.isWhite:
                self.validAttacks.append(tile)
            return False
        self.validAttacks.append(tile)
        return True

    def move(self, tile):
        # check if we're open to en passant attack (moving 2 spaces after first move)
        if not self.firstMoveMade:
            distance = abs(self.getPositionRow() - tile[ROW_INDEX])
            if distance == 2:
                self.enPassantRisk = True
                print(f"opening myself up to en passant {tile[COL_INDEX]},{tile[ROW_INDEX]}")
        else:
            self.enPassantRisk = False
        super().move(tile)


class Rook(Piece):
    def __init__(self, isWhite, board, number=1, startingPosition=None):
        character = 'rook'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 0 if (number == 1) else 7
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        # travel right
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow())) is False:
                break
        # travel left
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow())) is False:
                break
        # travel up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() - (i+1))) is False:
                break
        # travel down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + (i+1))) is False:
                break


class Knight(Piece):
    def __init__(self, isWhite, board, number=1, startingPosition=None):
        character = 'knight'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 1 if (number == 1) else 6
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

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
    def __init__(self, isWhite, board, number=1, startingPosition=None):
        character = 'bishop'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 2 if (number == 1) else 5
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        # travel right & down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow() + (i+1))) is False:
                break
        # travel right & up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow() - (i+1))) is False:
                break
        # travel left & up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow() - (i+1))) is False:
                break
        # travel left & down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow() + (i+1))) is False:
                break


class King(Piece):
    def __init__(self, isWhite, board, startingPosition=None):
        character = 'king'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 3
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        self.validMoves = []
        self.addNewValidMove((self.getPositionColumn() + 1, self.getPositionRow() + 1))
        self.addNewValidMove((self.getPositionColumn() + 1, self.getPositionRow() - 1))
        self.addNewValidMove((self.getPositionColumn() + 1, self.getPositionRow()))
        self.addNewValidMove((self.getPositionColumn() - 1, self.getPositionRow() + 1))
        self.addNewValidMove((self.getPositionColumn() - 1, self.getPositionRow() - 1))
        self.addNewValidMove((self.getPositionColumn() - 1, self.getPositionRow()))
        self.addNewValidMove((self.getPositionColumn(),     self.getPositionRow() + 1))
        self.addNewValidMove((self.getPositionColumn(),     self.getPositionRow() - 1))


class Queen(Piece):
    def __init__(self, isWhite, board, startingPosition=None):
        character = 'queen'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 4
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)


    def calculateNewValidMoves(self):
        self.validMoves = []
        # travel right
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow())) is False:
                break
        # travel left
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow())) is False:
                break
        # travel up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() - (i+1))) is False:
                break
        # travel down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + (i+1))) is False:
                break
        # travel right & down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow() + (i+1))) is False:
                break
        # travel right & up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() + (i+1), self.getPositionRow() - (i+1))) is False:
                break
        # travel left & up
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow() - (i+1))) is False:
                break
        # travel left & down
        for i in range(TILE_COUNT):
            if self.addNewValidMove((self.getPositionColumn() - (i+1), self.getPositionRow() + (i+1))) is False:
                break
