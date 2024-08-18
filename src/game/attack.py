import pygame
from .collider import Collider
import os
import dataclasses


class Attack:
    def __init__(
        self,
        owner_collider: Collider,
        damage: float,
        duration: float,
        direction: int,
        offset: int = 15,
        isRanged: bool = False,
        velocity: int = 0,
        collider: Collider | None = None,
    ) -> None:
        self.owner_collider = owner_collider  # fighter but can't annotate bc circular
        self.damage = damage
        self.direction = direction
        self.duration = duration
        self.time_left = duration
        self.offset = offset
        self.velocity = velocity
        self.isRanged = isRanged

        if not self.isRanged:
            self.collider: Collider = Collider(
                self.owner_collider.left() + direction * offset,
                self.owner_collider.top(),
                self.owner_collider.width,
                self.owner_collider.height,
            )
        else:
            if collider is None:
                self.collider: Collider = Collider(
                    (
                        self.owner_collider.left()
                        if direction == -1
                        else self.owner_collider.right()
                    ),
                    self.owner_collider.top() + self.owner_collider.height / 2 - 20,
                    20,
                    20,
                )
            else:
                self.collider = collider

            image_path = "assets/note.png"
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))

    def tick(self, delta_time) -> bool:
        movement = self.velocity * self.direction * delta_time
        self.collider.move_ip(pygame.Vector2(movement, 0))

        self.time_left -= delta_time

        return self.time_left > 0

    def draw(self, surface: pygame.Surface) -> None:
        # if not self.isRanged:
            # pygame.draw.rect(
            #     surface=surface, color=(255, 0, 0), rect=self.collider.get_rect()
            # )

        if self.isRanged:
            pos = (self.collider.x, self.collider.y)
            if 0 <= pos[0] < surface.get_width() and 0 <= pos[1] < surface.get_height():
                surface.blit(self.image, pos)

    def toJsonObj(self) -> dict:
        return {
            "owner_collider": dataclasses.asdict(self.owner_collider),
            "collider": dataclasses.asdict(self.collider),
            "damage": self.damage,
            "direction": self.direction,
            "duration": self.duration,
            "time_left": self.time_left,
            "offset": self.offset,
            "velocity": self.velocity,
            "isRanged": self.isRanged,
            "collider": dataclasses.asdict(self.collider),
        }
