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
    clock = pygame.time.Clock()

    # NOTE if frame rate too high, then there are rounding errors because dt is integer & too small
    MAX_FRAME_RATE = 30

    while True:
        for event in pygame.event.get():
            # exit handle
            if event.type == pygame.QUIT:
                sys.exit()

        # ---
        # Display

        # reset display
        screen.fill((255, 255, 255))

        gs.draw(surface=screen)

        # NOTE changes don't show until this is called
        pygame.display.update()

        # ---

        # in seconds
        delta_time = clock.tick(MAX_FRAME_RATE) / 1000.0

        gs.tick(delta_time)
