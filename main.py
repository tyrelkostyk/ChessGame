import pygame
from piece import Piece, Pawn, Rook, Knight, Bishop, King, Queen
from common import *

from typing import Optional

### Game Setup & Init
pygame.init()

# define screen
size = (WINDOW_WIDTH, WINDOW_WIDTH)
screen = pygame.display.set_mode(size)

# clock used to control how fast the game screen updates
clock = pygame.time.Clock()

# create game pieces
pieces = pygame.sprite.Group()

## white pieces
# rooks
whiteRookOne = Rook(True, 1)
pieces.add(whiteRookOne)
whiteRookTwo = Rook(True, 2)
pieces.add(whiteRookTwo)
# knights
whiteKnightOne = Knight(True, 1)
pieces.add(whiteKnightOne)
whiteKnightTwo = Knight(True, 2)
pieces.add(whiteKnightTwo)
# bishops
whiteBishopOne = Bishop(True, 1)
pieces.add(whiteBishopOne)
whiteBishopTwo = Bishop(True, 2)
pieces.add(whiteBishopTwo)
# king & queen
whiteKing = King(True)
pieces.add(whiteKing)
whiteQueen = Queen(True)
pieces.add(whiteQueen)
# pawns
whitePawnOne = Pawn(True, 1)
pieces.add(whitePawnOne)
whitePawnTwo = Pawn(True, 2)
pieces.add(whitePawnTwo)
whitePawnThree = Pawn(True, 3)
pieces.add(whitePawnThree)
whitePawnFour = Pawn(True, 4)
pieces.add(whitePawnFour)
whitePawnFive = Pawn(True, 5)
pieces.add(whitePawnFive)
whitePawnSix = Pawn(True, 6)
pieces.add(whitePawnSix)
whitePawnSeven = Pawn(True, 7)
pieces.add(whitePawnSeven)
whitePawnEight = Pawn(True, 8)
pieces.add(whitePawnEight)

# black pieces
# rooks
blackRookOne = Rook(False, 1)
pieces.add(blackRookOne)
blackRookTwo = Rook(False, 2)
pieces.add(blackRookTwo)
# knights
blackKnightOne = Knight(False, 1)
pieces.add(blackKnightOne)
blackKnightTwo = Knight(False, 2)
pieces.add(blackKnightTwo)
# bishops
blackBishopOne = Bishop(False, 1)
pieces.add(blackBishopOne)
blackBishopTwo = Bishop(False, 2)
pieces.add(blackBishopTwo)
# king & queen
blackKing = King(False)
pieces.add(blackKing)
blackQueen = Queen(False)
pieces.add(blackQueen)
# pawns
blackPawnOne = Pawn(False, 1)
pieces.add(blackPawnOne)
blackPawnTwo = Pawn(False, 2)
pieces.add(blackPawnTwo)
blackPawnThree = Pawn(False, 3)
pieces.add(blackPawnThree)
blackPawnFour = Pawn(False, 4)
pieces.add(blackPawnFour)
blackPawnFive = Pawn(False, 5)
pieces.add(blackPawnFive)
blackPawnSix = Pawn(False, 6)
pieces.add(blackPawnSix)
blackPawnSeven = Pawn(False, 7)
pieces.add(blackPawnSeven)
blackPawnEight = Pawn(False, 8)
pieces.add(blackPawnEight)

### main game loop

selectedPiece: Optional[Piece] = None   # the selected (grabbed) piece
mousePieceOffset = (0, 1)               # offset between the cursor and piece

carryOn = True
while carryOn:
    ## event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_MOUSE_BUTTON:
                for piece in pieces:
                    if piece.detectCollision(event.pos):
                        selectedPiece = piece
                        pieceCord = piece.getCurrentCords()
                        mousePieceOffset = (event.pos[0] - pieceCord[0], event.pos[1] - pieceCord[1])
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT_MOUSE_BUTTON:
                if selectedPiece:
                    selectedPiece.snapToTile(cordsToTile(event.pos[0], event.pos[1]))
                selectedPiece = None
        elif event.type == pygame.MOUSEMOTION:
            if selectedPiece:
                newPieceXCord = event.pos[0] - mousePieceOffset[0]
                newPieceYCord = event.pos[1] - mousePieceOffset[1]
                selectedPiece.setCords((newPieceXCord, newPieceYCord))

    ## game logic

    # update pieces
    pieces.update()

    ## drawing code

    # draw chessboard
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            square = pygame.Rect(col * TILE_WIDTH, row * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_TILE_COLOUR, square)
            else:
                pygame.draw.rect(screen, DARK_TILE_COLOUR, square)

    # draw pieces
    pieces.draw(screen)

    # update screen
    pygame.display.flip()

    # set clock rate
    clock.tick(60)

pygame.quit()
