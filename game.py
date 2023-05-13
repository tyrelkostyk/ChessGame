import pygame
from piece import Piece, Pawn, Rook, Knight, Bishop, King, Queen
from typing import Optional
from common import *


class Game:

    def __init__(self):
        # create active game pieces
        self.activePieces = pygame.sprite.Group()

        ## white pieces
        # rooks
        whiteRookOne = Rook(True, 1)
        self.activePieces.add(whiteRookOne)
        whiteRookTwo = Rook(True, 2)
        self.activePieces.add(whiteRookTwo)
        # knights
        whiteKnightOne = Knight(True, 1)
        self.activePieces.add(whiteKnightOne)
        whiteKnightTwo = Knight(True, 2)
        self.activePieces.add(whiteKnightTwo)
        # bishops
        whiteBishopOne = Bishop(True, 1)
        self.activePieces.add(whiteBishopOne)
        whiteBishopTwo = Bishop(True, 2)
        self.activePieces.add(whiteBishopTwo)
        # king & queen
        whiteKing = King(True)
        self.activePieces.add(whiteKing)
        whiteQueen = Queen(True)
        self.activePieces.add(whiteQueen)
        # pawns
        whitePawnOne = Pawn(True, 1)
        self.activePieces.add(whitePawnOne)
        whitePawnTwo = Pawn(True, 2)
        self.activePieces.add(whitePawnTwo)
        whitePawnThree = Pawn(True, 3)
        self.activePieces.add(whitePawnThree)
        whitePawnFour = Pawn(True, 4)
        self.activePieces.add(whitePawnFour)
        whitePawnFive = Pawn(True, 5)
        self.activePieces.add(whitePawnFive)
        whitePawnSix = Pawn(True, 6)
        self.activePieces.add(whitePawnSix)
        whitePawnSeven = Pawn(True, 7)
        self.activePieces.add(whitePawnSeven)
        whitePawnEight = Pawn(True, 8)
        self.activePieces.add(whitePawnEight)

        # black pieces
        # rooks
        blackRookOne = Rook(False, 1)
        self.activePieces.add(blackRookOne)
        blackRookTwo = Rook(False, 2)
        self.activePieces.add(blackRookTwo)
        # knights
        blackKnightOne = Knight(False, 1)
        self.activePieces.add(blackKnightOne)
        blackKnightTwo = Knight(False, 2)
        self.activePieces.add(blackKnightTwo)
        # bishops
        blackBishopOne = Bishop(False, 1)
        self.activePieces.add(blackBishopOne)
        blackBishopTwo = Bishop(False, 2)
        self.activePieces.add(blackBishopTwo)
        # king & queen
        blackKing = King(False)
        self.activePieces.add(blackKing)
        blackQueen = Queen(False)
        self.activePieces.add(blackQueen)
        # pawns
        blackPawnOne = Pawn(False, 1)
        self.activePieces.add(blackPawnOne)
        blackPawnTwo = Pawn(False, 2)
        self.activePieces.add(blackPawnTwo)
        blackPawnThree = Pawn(False, 3)
        self.activePieces.add(blackPawnThree)
        blackPawnFour = Pawn(False, 4)
        self.activePieces.add(blackPawnFour)
        blackPawnFive = Pawn(False, 5)
        self.activePieces.add(blackPawnFive)
        blackPawnSix = Pawn(False, 6)
        self.activePieces.add(blackPawnSix)
        blackPawnSeven = Pawn(False, 7)
        self.activePieces.add(blackPawnSeven)
        blackPawnEight = Pawn(False, 8)
        self.activePieces.add(blackPawnEight)

        # create captured game pieces
        self.capturedPieces = pygame.sprite.Group()

        # can have 1 active piece selected (grabbed) at a time
        self.selectedPiece: Optional[Piece] = None

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


