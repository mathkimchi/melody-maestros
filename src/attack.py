import pygame


class Attack:
    def __init__(self, owner, damage: float, duration: float, direction: int, offset: int = 50) -> None:
        self.owner = owner  # fighter but can't annotate bc circular
        self.damage = damage
        self.direction = direction
        self.duration = duration
        self.time_left = duration
        self.offset = offset
        
        self.collider: pygame.Rect = pygame.Rect(
            self.owner.collider.left() + direction * offset,
            self.owner.collider.top(),
            self.owner.collider.width,
            self.owner.collider.height,
        )
        # seconds

    def tick(self, delta_time) -> bool:
        """
        Returns whether or not the attack should persist to the next tick
        """
        self.time_left -= delta_time

        return self.time_left > 0

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface=surface, color=(255, 255, 0), rect=self.collider)