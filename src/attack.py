import pygame
from collider import Collider


class Attack:
    def __init__(self, owner, damage: float, duration: float, direction: int, offset: int = 15, isRanged: bool = False, velocity: int = 0) -> None:
        self.owner = owner  # fighter but can't annotate bc circular
        self.damage = damage
        self.direction = direction
        self.duration = duration
        self.time_left = duration
        self.offset = offset
        self.velocity = velocity
        self.isRanged = isRanged
        
        if not self.isRanged:
            self.collider: pygame.Rect = pygame.Rect(
                self.owner.collider.left() + direction * offset,
                self.owner.collider.top(),
                self.owner.collider.width,
                self.owner.collider.height,
            )
        else:
            self.collider : pygame.Rect = pygame.Rect(
                (self.owner.collider.left() if direction == -1 else self.owner.collider.right()), 
                self.owner.collider.top() + self.owner.collider.height/2 - 10,
                10,
                10,
            )

    def tick(self, delta_time) -> bool:
        movement = self.velocity * self.direction * delta_time
        self.collider.move_ip(movement, 0)
        
        self.time_left -= delta_time

        return self.time_left > 0

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface=surface, color=(255, 255, 0), rect=self.collider)