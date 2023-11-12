import pygame
from typing import Optional, cast

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

        # keep track of check (only valid for the current player)
        self.isKingInCheck = False

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

    def getBoard(self):
        return self.board

    # def selectPiece(self, mousePosition):
    def selectPiece(self, tile):
        if self.selectedPiece is not None:
            return False
        for piece in self.getActivePieces():
            if piece.detectTileCollision(tile):
                if not piece.getIsWhite() == self.isWhitesTurn:
                    return False
                self.selectedPiece = piece
                self.selectedPiece.calculateNewValidMoves()
                return True
        return False

    def dragPiece(self, newCoordinatePosition):
        if self.selectedPiece:
            self.selectedPiece.setCords(newCoordinatePosition)

    def placePiece(self, newTile):
        if self.selectedPiece is None:
            return
        if not isTileInRange(newTile):
            self.selectedPiece.goBackToPosition()
            self.selectedPiece = None
            return

        # TODO: implement checks for checkmate

        successfulMove = False

        # destination tile is empty
        if not self.board.isTileOccupied(newTile):
            # TODO: implement piece revival

            # capture via en passant
            if self.selectedPiece.isValidAttack(newTile) and self.selectedPiece.getCharacterName() == 'pawn':
                # pawns moving to an open space may be able to capture an enemy pawn via En Passant
                self.selectedPiece = cast(Pawn, self.selectedPiece)
                enPassantVictimTile = (newTile[COL_INDEX], newTile[ROW_INDEX] - self.selectedPiece.getDirection())
                # is the tile behind a pawn?
                if self.board.isTileOccupied(enPassantVictimTile) and self.board.getPieceAtTile(enPassantVictimTile).getCharacterName() == 'pawn':
                    victimPawn = cast(Pawn, self.board.getPieceAtTile(enPassantVictimTile))
                    # did the victim pawn enter En Passant risk last turn?
                    if victimPawn.isOpenToEnPassant():
                        self.movePiece(newTile, self.board.getPieceAtTile(enPassantVictimTile))
                        successfulMove = True

            if not successfulMove and self.selectedPiece.isValidMove(newTile) and self.movePiece(newTile):
                successfulMove = True

        # destination tile has friendly piece
        elif self.board.getPieceAtTile(newTile).getIsWhite() == self.selectedPiece.isWhite:
            # TODO: implement castling
            pass

        # destination tile has opponent piece
        elif self.selectedPiece.isValidAttack(newTile) and self.movePiece(newTile, self.board.getPieceAtTile(newTile)):
            successfulMove = True

        if successfulMove:
            self.completeTurn()
            incrementTurnNumber()
        else:
            self.cancelMove()

    def capturePiece(self, capturedPiece):
        if capturedPiece in self.activePieces:
            self.activePieces.remove(capturedPiece)
        if capturedPiece not in self.capturedPieces:
            self.capturedPieces.add(capturedPiece)

    def restorePiece(self, capturedPiece, newTile=None):
        if capturedPiece in self.capturedPieces:
            self.capturedPieces.remove(capturedPiece)
        if capturedPiece not in self.activePieces:
            self.activePieces.add(capturedPiece)
            position = capturedPiece.getPosition() if newTile is None else newTile
            capturedPiece.move(position)

    def movePiece(self, newTile, existingPiece=None):
        if self.selectedPiece is None:
            return False
        # captured piece (if necessary)
        if existingPiece is not None:
            self.capturePiece(existingPiece)
        # record original piece position
        startingPosition = self.selectedPiece.getPosition()
        # determine if the moving player was previously in check
        inCheck = self.isCurrentPlayerInCheck()
        # move piece
        self.selectedPiece.move(newTile)
        # if previously in check, evaluate check resolution
        if inCheck and self.isCurrentPlayerInCheck():
            # restore capture piece
            if existingPiece is not None:
                self.restorePiece(existingPiece)
            # place selected piece back to its original position
            self.selectedPiece.move(startingPosition)
            return False
        # successfully moved the piece
        return True

    def cancelMove(self):
        self.selectedPiece.goBackToPosition()
        self.selectedPiece = None

    def completeTurn(self):
        self.isWhitesTurn = not self.isWhitesTurn
        self.selectedPiece = None

    def isCurrentPlayerInCheck(self):
        self.isKingInCheck = False
        for piece in self.activePieces:
            # only evaluate opponent pieces
            if piece.getIsWhite() == self.isWhitesTurn:
                continue
            piece.calculateNewValidMoves()
            if piece.hasKingChecked():
                self.isKingInCheck = True
                break
        return self.isKingInCheck

