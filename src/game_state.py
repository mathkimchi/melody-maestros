import pygame
from fighter import Fighter


class GameState:
    def __init__(self) -> None:
        self.player = Fighter()

    def tick(self) -> None:
        """
        Performs just the logic (changes the data) for a single tick.
        In other words, does not display.
        """

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] == True:
            self.player.move_left()
        if pressed_keys[pygame.K_RIGHT] == True:
            self.player.move_right()

    def draw(self, surface: pygame.Surface) -> None:
        """Does NOT update surface"""
        # draw the player as a rectangle
        pygame.draw.rect(surface=surface, color=(255, 0, 0), rect=self.player.collider)
