from sys import platform
import pygame
from .fighters.violinist import Violinist
from .fighter import Fighter
from .platform_entity import Platform
from .collider import Collider


class GameState:
    """Represents all the data relating to a game."""

    def __init__(self) -> None:
        self.players: dict[int, Fighter] = {}
        self.platforms = [Platform(self, Collider(0.0, 300.0, 300.0, 30.0))]

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

        # print(f"-------------")
        # print(f"{self.__dict__=}")
        # print(f"{self.players[0].__dict__=}")
        # print(f"{self.players[0].toJsonObj()=}")
        # print(f"{self.toJsonObj()=}")

    def draw(self, surface: pygame.Surface) -> None:
        """Does NOT update surface"""

        # draw "children"
        # draw the player as a rectangle
        for player in self.players.values():
            player.draw(surface=surface)
        for platform in self.platforms:
            platform.draw(surface=surface)

    def toJsonObj(self) -> dict[str, object]:
        return {
            "players": {id: player.toJsonObj() for id, player in self.players.items()},
            "platforms": [platform.toJsonObj() for platform in self.platforms],
        }

    def parse_json_in_place(self, new: dict):
        # put here bc stupid circular import rules
        def from_json_obj(obj: dict, gs) -> Fighter:
            if obj["type"] == str(Violinist):
                return Violinist(
                    gs,
                    player_id=obj["player_id"],
                    direction=obj["direction"],
                    move_input=obj["move_input"],
                    velocity=pygame.Vector2(obj["velocity"]),
                    collider=Collider(**obj["collider"]),
                    attacks=obj["attacks"],
                )
            else:
                raise

        self.players = {
            id: from_json_obj(player_dict, self)
            for id, player_dict in new["players"].items()
        }
        self.platforms = [
            Platform(self, Collider(**platform)) for platform in new["platforms"]
        ]
