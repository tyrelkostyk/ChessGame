import pygame
from piece import *
from common import *

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

selectedPiece = None
mouseOffset = (0, 1)

carryOn = True
while carryOn:
    ## event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # left mouse button
            if event.button == 1:
                for piece in pieces:
                    if piece.rect.collidepoint(event.pos):
                        selectedPiece = piece
                        mouseOffset = (event.pos[0] - piece.rect.x, event.pos[1] - piece.rect.y)
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            # left mouse button
            if event.button == 1:
                if selectedPiece:
                    # snap piece to selected tile
                    x = (selectedPiece.rect.x + TILE_WIDTH // 2) // TILE_WIDTH
                    y = (selectedPiece.rect.y + TILE_WIDTH // 2) // TILE_WIDTH
                    selectedPiece.rect.x = x * TILE_WIDTH + BORDER_WIDTH
                    selectedPiece.rect.y = y * TILE_WIDTH + BORDER_WIDTH
                selectedPiece = None
        elif event.type == pygame.MOUSEMOTION:
            if selectedPiece:
                selectedPiece.rect.x = event.pos[0] - mouseOffset[0]
                selectedPiece.rect.y = event.pos[1] - mouseOffset[1]

    ## game logic

    # update pieces
    pieces.update()

    ## drawing code

    # draw chessboard
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            square = pygame.Rect(col * TILE_WIDTH, row * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_BROWN, square)
            else:
                pygame.draw.rect(screen, DARK_BROWN, square)

    # draw pieces
    pieces.draw(screen)

    # update screen
    pygame.display.flip()

    # set clock rate
    clock.tick(60)

pygame.quit()
