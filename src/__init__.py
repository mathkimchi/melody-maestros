"""
This is the file that actually runs Melody Maestros.
"""

import sys
import pygame
import game_state

if __name__ == "__main__":  # if this is the file being run
    # initialization stuff
    pygame.init()
    gs = game_state.GameState()
    screen = pygame.display.set_mode((540, 540))

    while True:
        for event in pygame.event.get():
            # exit handle
            if event.type == pygame.QUIT:
                sys.exit()

        # reset display
        screen.fill((0, 0, 0))

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] == True:
            # player wants to move left
            gs.player_rect.move_ip(-1, 0)
        if pressed_keys[pygame.K_RIGHT] == True:
            # player wants to move right
            gs.player_rect.move_ip(+1, 0)
            print(f"{gs.player_rect=}")

        # draw the player as a rectangle
        pygame.draw.rect(surface=screen, color=(255, 0, 0), rect=gs.player_rect)

        # NOTE changes don't show until this is called
        pygame.display.update()
