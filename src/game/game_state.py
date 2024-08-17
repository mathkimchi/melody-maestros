from sys import platform
import pygame
from .fighters.violinist import Violinist
from .fighter import Fighter
from .platform_entity import Platform
from .collider import Collider
from .attack import Attack


class GameState:
    """Represents all the data relating to a game."""

    def __init__(self) -> None:
        self.players: dict[int, Fighter] = {}
        self.platforms = [

        Platform(self, Collider(0.0, 550.0, 1200.0, 50.0)),

        # Central elevated platform
        Platform(self, Collider(400.0, 350.0, 400.0, 20.0)),

        # Two small floating platforms on either side
        Platform(self, Collider(100.0, 250.0, 200.0, 20.0)),
        Platform(self, Collider(900.0, 250.0, 200.0, 20.0)),
    ]


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
        def from_json_obj(obj: dict, gs, id) -> Fighter:
            if obj["type"] == str(Violinist):
                return Violinist(
                    gs,
                    player_id=id,
                    health=obj["health"],
                    direction=obj["direction"],
                    move_input=obj["move_input"],
                    velocity=pygame.Vector2(obj["velocity"]),
                    collider=Collider(**obj["collider"]),
                    attacks=[
                        self.parse_attack_dict(attack) for attack in obj["attacks"]
                    ],
                )
            else:
                raise

        self.players = {
            id: from_json_obj(player_dict, self, id)
            for id, player_dict in new["players"].items()
        }
        self.platforms = [
            Platform(self, Collider(**platform)) for platform in new["platforms"]
        ]

    def parse_attack_dict(self, obj: dict) -> Attack:
        return Attack(
            owner_collider=Collider(
                obj["owner_collider"]["x"],
                obj["owner_collider"]["y"],
                obj["owner_collider"]["width"],
                obj["owner_collider"]["height"],
            ),
            damage=obj["damage"],
            duration=obj["time_left"],
            direction=obj["direction"],
            offset=obj["offset"],
            velocity=obj["velocity"],
            isRanged=obj["isRanged"],
            collider=Collider(
                obj["collider"]["x"],
                obj["collider"]["y"],
                obj["collider"]["width"],
                obj["collider"]["height"],
            ),
        )
