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
        if self.selectedPiece.isValidMove(newTile):
            self.selectedPiece.move(newTile)
        else:
            self.selectedPiece.goBackToPosition()
        self.selectedPiece = None


