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
            if self.isOpponentCheckmated():
                print(f"{'White' if self.isWhitesTurn else 'Black'} Wins!!!")
                # TODO: end game, increment score, etc.

            self.whereIsOpposingPlayerInCheck()
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
        pieceToBeCaptured = existingPiece
        if pieceToBeCaptured is None:
            pieceToBeCaptured = self.board.getPieceAtTile(newTile)
        if pieceToBeCaptured is not None:
            self.capturePiece(pieceToBeCaptured)
        # record original piece position
        startingPosition = self.selectedPiece.getPosition()
        # move piece
        self.selectedPiece.move(newTile)
        # can't make a move that results in check
        if self.isPlayerInCheck(self.isWhitesTurn):
            # restore capture piece
            if pieceToBeCaptured is not None:
                self.restorePiece(pieceToBeCaptured)
            # place selected piece back to its original position
            self.selectedPiece.move(startingPosition)
            return False
        # successfully moved the piece
        return True

    def simulatePieceMovement(self, piece, newTile):
        if piece is None:
            return False
        # captured piece (if necessary)
        existingPiece = self.board.getPieceAtTile(newTile)
        if existingPiece is not None:
            self.capturePiece(existingPiece)
        # record original piece position
        startingPosition = piece.getPosition()
        # move piece
        piece.move(newTile)
        # evaluate if this player is still in check after the move
        escapedCheck = not self.isPlayerInCheck(piece.getIsWhite())
        # restore capture piece
        if existingPiece is not None:
            self.restorePiece(existingPiece)
        # place selected piece back to its original position
        piece.move(startingPosition)
        # successfully moved the piece
        return escapedCheck

    def cancelMove(self):
        self.selectedPiece.goBackToPosition()
        self.selectedPiece = None

    def completeTurn(self):
        self.isWhitesTurn = not self.isWhitesTurn
        self.selectedPiece = None

    def isPlayerInCheck(self, isPlayerWhite):
        isPlayerInCheck = False
        for piece in self.activePieces:
            # only evaluate opponent pieces
            if piece.getIsWhite() == isPlayerWhite:
                continue
            piece.calculateNewValidMoves()
            if piece.hasKingChecked():
                isPlayerInCheck = True
                break
        return isPlayerInCheck

    def whereIsOpposingPlayerInCheck(self):
        for piece in self.activePieces:
            # only evaluate friendly pieces
            if not piece.getIsWhite() == self.isWhitesTurn:
                continue
            piece.calculateNewValidMoves()
            if piece.hasKingChecked():
                print(f"{'Black' if piece.isWhite else 'White'} King is in Check by {piece.getCharacterName()} at {piece.getPositionColumn()}, {piece.getPositionRow()}")

    '''
    Check to see if opponent is in checkmate; if so, current player wins
    '''
    def isOpponentCheckmated(self):
        # first, opponent must be in check
        if not self.isPlayerInCheck(not self.isWhitesTurn):
            return False
        # simulate all the possible moves the opponent can make; if not get them out of check, it's checkmate
        opponentPieces = [piece for piece in self.activePieces if piece.getIsWhite() != self.isWhitesTurn]
        for piece in opponentPieces:
            piece.calculateNewValidMoves()
            for validMove in piece.validMoves:
                if self.simulatePieceMovement(piece, validMove):
                    return False
            for validAttack in piece.validAttacks:
                if self.simulatePieceMovement(piece, validAttack):
                    return False
        return True

