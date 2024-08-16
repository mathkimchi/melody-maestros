import pygame


class Collider:
    """Pygame rect only works with ints, which screws physics"""

    def __init__(self, x, y, width, height) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def right(self) -> float:
        return self.x + self.width

    def left(self) -> float:
        return self.x

    def bottom(self) -> float:
        return self.y + self.width

    def top(self) -> float:
        return self.y


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
    y_overlap = min(collider.bottom, other_collider.bottom) - max(
        collider.top, other_collider.top
    )

    # smaller overlap is collision dimension
    if x_overlap < y_overlap:
        # horizontal collision
        return pygame.Vector2(other_collider.centerx - collider.centerx, 0)
    else:
        # vertical collision
        return pygame.Vector2(0, other_collider.centery - collider.centery)
