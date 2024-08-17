import pygame
from .collider import Collider
import dataclasses


@dataclasses.dataclass
class Platform:
    """Immovable and collidable parts of the map."""

    collider: Collider

    def __init__(self, gs, collider) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        self.collider = collider

    def tick(self, delta_time) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface=surface,
            color=(200, 200, 200),
            rect=self.collider.get_rect(),
        )

    def toJsonObj(self) -> dict[str, object]:
        return dataclasses.asdict(self.collider)
