import pygame
from .fighters.violinist import Violinist
from .platform_entity import Platform


class GameState:
    """Represents all the data relating to a game."""

    def __init__(self) -> None:
        self.players = {0: Violinist(self)}
        self.platforms = [Platform(self)]

    def tick(self, delta_time) -> None:
        """
        Performs just the logic (changes the data) for a single tick.
        In other words, does not display.
        """

        # update "children"
        for player in self.players.values():
            player.tick(delta_time)
        for platform in self.platforms:
            platform.tick(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Does NOT update surface"""

        # draw "children"
        # draw the player as a rectangle
        for player in self.players.values():
            player.draw(surface=surface)
        for platform in self.platforms:
            platform.draw(surface=surface)
