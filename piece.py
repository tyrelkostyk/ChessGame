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

        # each piece needs to track whether it currently has the opposing king in check
        self.kingChecked = False

        # define initial valid moves
        self.calculateNewValidMoves()

    def getIsWhite(self):
        return self.isWhite

    def getCharacterName(self):
        return self.character

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

    def getCurrentCoordinates(self):
        return self.rect.x, self.rect.y

    def hasKingChecked(self):
        return self.kingChecked

    def detectCoordinateCollision(self, cords):
        return self.rect.collidepoint(cords[0], cords[1])

    def detectTileCollision(self, tile):
        return self.position == tile

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

    def calculateNewValidMoves(self):
        self.validMoves = []
        self.validAttacks = []
        self.kingChecked = False

    def addNewValidMove(self, tile):
        if not isTileInRange(tile):
            return False
        if self.board.isTileOccupied(tile):
            if self.board.getPieceAtTile(tile).getIsWhite() != self.isWhite:
                self.validAttacks.append(tile)
                if self.board.getPieceAtTile(tile).getCharacterName() == 'king':
                    self.kingChecked = True
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
        self.direction = 1 if isWhite else -1
        self.enPassantRiskTurn = 0

        if startingPosition is None:
            row = 1 if isWhite else 6
            column = number - 1
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        super().calculateNewValidMoves()
        # travel forward 1 square
        if self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + self.direction)):
            # travel forward 2 squares
            if self.firstMoveMade is not True:
                self.addNewValidMove((self.getPositionColumn(), self.getPositionRow() + (2 * self.direction)))
        # capture diagonally
        self.addNewValidAttack((self.getPositionColumn() + 1, self.getPositionRow() + self.direction))
        self.addNewValidAttack((self.getPositionColumn() - 1, self.getPositionRow() + self.direction))

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
                if self.board.getPieceAtTile(tile).getCharacterName() == 'king':
                    self.kingChecked = True
            return False
        self.validAttacks.append(tile)
        return True

    def move(self, tile):
        # check if we're open to en passant attack (moving 2 spaces after first move)
        if not self.firstMoveMade:
            distance = abs(self.getPositionRow() - tile[ROW_INDEX])
            if distance == 2:
                self.enPassantRiskTurn = getTurnNumber()
        else:
            self.enPassantRiskTurn = 0
        super().move(tile)

    def getDirection(self):
        return self.direction

    def isOpenToEnPassant(self):
        return getTurnNumber() - self.enPassantRiskTurn == 1


class Rook(Piece):
    def __init__(self, isWhite, board, number=1, startingPosition=None):
        character = 'rook'
        if startingPosition is None:
            row = 0 if isWhite else 7
            column = 0 if (number == 1) else 7
            startingPosition = (column, row)
        super().__init__(character, isWhite, board, startingPosition)

    def calculateNewValidMoves(self):
        super().calculateNewValidMoves()
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
        super().calculateNewValidMoves()
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
        super().calculateNewValidMoves()
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
        super().calculateNewValidMoves()
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
        super().calculateNewValidMoves()
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
