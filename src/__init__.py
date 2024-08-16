"""
This is the file that actually runs Melody Maestros.
"""

import sys
import pygame
from game_state import GameState

if __name__ == "__main__":  # if this is the file being run
    # initialization stuff
    pygame.init()
    gs = GameState()
    screen = pygame.display.set_mode((540, 540))

    while True:
        for event in pygame.event.get():
            # exit handle
            if event.type == pygame.QUIT:
                sys.exit()

        # ---
        # Display

        # reset display
        screen.fill((0, 0, 0))

        gs.draw(surface=screen)

        # NOTE changes don't show until this is called
        pygame.display.update()

        # ---

        gs.tick()
