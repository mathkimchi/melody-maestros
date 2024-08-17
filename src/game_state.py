import pygame
from fighters.violinist import Violinist
from fighter import Fighter
from platform_entity import Platform


class GameState:
    def __init__(self) -> None:
        self.player = Violinist(self)
        self.platforms = [Platform(self)]

    def tick(self, delta_time) -> None:
        """
        Performs just the logic (changes the data) for a single tick.
        In other words, does not display.
        """

        # handle inputs
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] == True:
            self.player.move_left()
        elif pressed_keys[pygame.K_RIGHT] == True:
            self.player.move_right()
        else:
            self.player.stop()
        if pressed_keys[pygame.K_UP] == True:
            self.player.jump()
        if pressed_keys[pygame.K_LSHIFT] == True:
            self.player.fast_attack()
        if pressed_keys[pygame.K_z] == True:
            self.player.ranged_attack()

        # update "children"
        self.player.tick(delta_time)
        for platform in self.platforms:
            platform.tick(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Does NOT update surface"""

        # draw "children"
        # draw the player as a rectangle
        self.player.draw(surface=surface)
        for platform in self.platforms:
            platform.draw(surface=surface)
