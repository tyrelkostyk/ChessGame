import pygame

from game import Game
from common import *

### Game Setup & Init
pygame.init()

# define screen
size = (WINDOW_WIDTH, WINDOW_WIDTH)
screen = pygame.display.set_mode(size)

# clock used to control how fast the game screen updates
clock = pygame.time.Clock()

# game manager
game = Game()

### main game loop

mousePieceOffset = (0, 1)   # offset between the cursor and piece's top left corner

carryOn = True
while carryOn:
    ## event loop & game logic
    for event in pygame.event.get():

        # exit the game
        if event.type == pygame.QUIT:
            carryOn = False

        # pick up a piece (if one is present under the cursor)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_MOUSE_BUTTON:
                if game.selectPiece(event.pos):
                    # calculate offset between cursor and piece's top-left corner position
                    pieceCord = game.getSelectedPiece().getCurrentCords()
                    mousePieceOffset = (event.pos[0] - pieceCord[0], event.pos[1] - pieceCord[1])

        # place a piece down (if the proposed move is valid)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT_MOUSE_BUTTON:
                game.placePiece(event.pos)

        # move a held piece around the board
        elif event.type == pygame.MOUSEMOTION:
            if game.getSelectedPiece():
                newPieceXCord = event.pos[0] - mousePieceOffset[0]
                newPieceYCord = event.pos[1] - mousePieceOffset[1]
                game.dragPiece((newPieceXCord, newPieceYCord))

    # update active piece locations
    game.getActivePieces().update()

    # draw chessboard
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            square = pygame.Rect(col * TILE_WIDTH, row * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_TILE_COLOUR, square)
            else:
                pygame.draw.rect(screen, DARK_TILE_COLOUR, square)

    # draw active pieces
    game.getActivePieces().draw(screen)

    # update screen
    pygame.display.flip()

    # set clock rate
    clock.tick(60)

pygame.quit()
