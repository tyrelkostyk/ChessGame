import pygame
from typing import Optional

from piece import Piece, Pawn, Rook, Knight, Bishop, King, Queen
from board import Board
from common import *

class Game:

    def __init__(self):
        # create Board to track pieces
        self.board = Board()

        # create active game pieces
        self.activePieces = pygame.sprite.Group()
        self.createStandardPieces()

        # create captured game pieces
        self.capturedPieces = pygame.sprite.Group()

        # can have 1 active piece selected (grabbed) at a time
        self.selectedPiece: Optional[Piece] = None

        # one player (colour) can move at a time, starting with white
        self.isWhitesTurn = True

    def createStandardPieces(self):
        self.createStandardPawns(True)
        self.createStandardSpecialPieces(True)
        self.createStandardPawns(False)
        self.createStandardSpecialPieces(False)
        return

    def createStandardPawns(self, isWhite):
        for i in range(TILE_COUNT):
            self.activePieces.add(Pawn(isWhite, self.board, i+1))

    def createStandardSpecialPieces(self, isWhite):
        self.activePieces.add(Rook(isWhite, self.board, 1))
        self.activePieces.add(Rook(isWhite, self.board, 2))
        self.activePieces.add(Knight(isWhite, self.board, 1))
        self.activePieces.add(Knight(isWhite, self.board, 2))
        self.activePieces.add(Bishop(isWhite, self.board, 1))
        self.activePieces.add(Bishop(isWhite, self.board, 2))
        self.activePieces.add(King(isWhite, self.board))
        self.activePieces.add(Queen(isWhite, self.board))

    def getActivePieces(self):
        return self.activePieces

    def getCapturedPieces(self):
        return self.capturedPieces

    def getSelectedPiece(self):
        return self.selectedPiece

    def selectPiece(self, mousePosition):
        if self.selectedPiece is not None:
            return False
        for piece in self.getActivePieces():
            if piece.detectCollision(mousePosition):
                if not piece.getIsWhite() == self.isWhitesTurn:
                    return False
                self.selectedPiece = piece
                self.selectedPiece.calculateNewValidMoves()
                return True
        return False

    def dragPiece(self, newPosition):
        if self.selectedPiece:
            self.selectedPiece.setCords(newPosition)

    def placePiece(self, mousePosition):
        if self.selectedPiece is None:
            return
        newTile = cordsToTile(mousePosition[0], mousePosition[1])
        if not isTileInRange(newTile):
            self.selectedPiece.goBackToPosition()
            self.selectedPiece = None
            return

        # TODO: implement checks for check/checkmate (entering & exiting)

        # destination tile is empty
        if not self.board.isTileOccupied(newTile):
            # TODO: implement piece revival

            if self.selectedPiece.isValidMove(newTile):
                self.selectedPiece.move(newTile)
                self.isWhitesTurn = not self.isWhitesTurn
            # TODO: capture via en passant
            # elif self.selectedPiece.isValidAttack(newTile):
            #     self.captureViaEnPassant(self.selectedPiece, newTile)
            else:
                self.selectedPiece.goBackToPosition()

        # destination tile has friendly piece
        elif self.board.getPieceAtTile(newTile).getIsWhite() == self.selectedPiece.isWhite:
            # TODO: implement castling
            self.selectedPiece.goBackToPosition()

        # destination tile has opponent piece
        else:
            if self.selectedPiece.isValidAttack(newTile):
                self.capturePiece(self.board.getPieceAtTile(newTile))
                self.selectedPiece.move(newTile)
                self.isWhitesTurn = not self.isWhitesTurn
            else:
                self.selectedPiece.goBackToPosition()

        self.selectedPiece = None

    def capturePiece(self, capturedPiece):
        if capturedPiece in self.activePieces:
            self.activePieces.remove(capturedPiece)
        if capturedPiece not in self.capturedPieces:
            self.capturedPieces.add(capturedPiece)

    # def captureViaEnPassant(self, attackingPiece, tile):
    #     direction = -1 if attackingPiece.getIsWhite() else 1
    #     newTile = (tile[COL_INDEX], tile[ROW_INDEX] + (1 * direction))
    #     print(f"checking for en passant enemy pawn at tile {newTile[COL_INDEX]},{newTile[ROW_INDEX]}")
    #     if not isTileInRange(newTile):
    #         return False
    #     if not self.board.isTileOccupied(newTile):
    #         return False
    #     pieceAtRisk = self.board.getPieceAtTile(newTile)
    #     if pieceAtRisk.getIsWhite() == attackingPiece.getIsWhite():
    #         return False
    #     if not pieceAtRisk.isOpenToEnPassant():
    #         return False
    #     print(f"Successful en passant at tile {tile[COL_INDEX]},{tile[ROW_INDEX]}")
    #     self.capturePiece(pieceAtRisk)
    #     self.selectedPiece.move(newTile)
    #     self.isWhitesTurn = not self.isWhitesTurn





