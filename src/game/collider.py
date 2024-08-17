import pygame
import dataclasses


@dataclasses.dataclass
class Collider:
    """Pygame rect only works with ints, which screws physics"""

    x: float
    y: float
    width: float
    height: float

    def __init__(self, x, y, width, height) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def left(self) -> float:
        return self.x

    def right(self) -> float:
        return self.x + self.width

    def top(self) -> float:
        return self.y

    def bottom(self) -> float:
        return self.y + self.height

    def centerx(self) -> float:
        return self.x + self.width / 2

    def centery(self) -> float:
        return self.y + self.height / 2

    def move_ip(self, move_by: pygame.Vector2):
        self.x += move_by.x
        self.y += move_by.y

    def colliderect(self, other: "Collider", count_touching:bool = False) -> bool:
        if count_touching:
            return (
                self.x <= other.x + other.width
                and self.x + self.width >= other.x
                and self.y <= other.y + other.height
                and self.y + self.height >= other.y
            )
        else:
            return (
                self.x < other.x + other.width
                and self.x + self.width > other.x
                and self.y < other.y + other.height
                and self.y + self.height > other.y
            )


# def collider_from_rect(rect: pygame.Rect) -> Collider:
#     return Collider(rect.x, rect.y, rect.width, rect.height)


def get_collision_direction(
    collider: Collider, other_collider: Collider
) -> pygame.Vector2:
    """
    Just a helper function
    breaks when an object is inside another object in the collision direction
    """

    # overlaps should be non-negative
    x_overlap = min(collider.right(), other_collider.right()) - max(
        collider.left(), other_collider.left()
    )
    y_overlap = min(collider.bottom(), other_collider.bottom()) - max(
        collider.top(), other_collider.top()
    )

    # smaller overlap is collision dimension
    if x_overlap < y_overlap:
        # horizontal collision
        return pygame.Vector2(other_collider.centerx() - collider.centerx(), 0)
    else:
        # vertical collision
        return pygame.Vector2(0, other_collider.centery() - collider.centery())
