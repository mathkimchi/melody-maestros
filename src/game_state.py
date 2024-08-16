import pygame
from fighter import Fighter


class GameState:
    def __init__(self) -> None:
        self.player = Fighter(self)

    def tick(self, delta_time) -> None:
        """
        Performs just the logic (changes the data) for a single tick.
        In other words, does not display.
        """

        # handle inputs
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] == True:
            self.player.move_left()
        if pressed_keys[pygame.K_RIGHT] == True:
            self.player.move_right()
        if pressed_keys[pygame.K_LSHIFT] == True:
            self.player.fast_attack()

        # update "children"
        self.player.tick(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Does NOT update surface"""

        # draw "children"
        # draw the player as a rectangle
        self.player.draw(surface=surface)
