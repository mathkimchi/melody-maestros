import pygame
from .collider import Collider
import os
import dataclasses

class Attack:
    def __init__(self, owner_collider, damage: float, duration: float, direction: int, offset: int = 15, isRanged: bool = False, velocity: int = 0) -> None:
        self.owner_collider = owner_collider  # fighter but can't annotate bc circular
        self.damage = damage
        self.direction = direction
        self.duration = duration
        self.time_left = duration
        self.offset = offset
        self.velocity = velocity
        self.isRanged = isRanged
        
        if not self.isRanged:
            self.collider: pygame.Rect = pygame.Rect(
                self.owner_collider.left() + direction * offset,
                self.owner_collider.top(),
                self.owner_collider.width,
                self.owner_collider.height,
            )
        else:
            self.collider : pygame.Rect = pygame.Rect(
                (self.owner_collider.left() if direction == -1 else self.owner_collider.right()), 
                self.owner_collider.top() + self.owner_collider.height/2 - 20,
                20,
                20,
            )
            
            image_path = "assets/note.png"
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))



    def tick(self, delta_time) -> bool:
        movement = self.velocity * self.direction * delta_time
        self.collider.move_ip(movement, 0)
        
        self.time_left -= delta_time

        return self.time_left > 0

    def draw(self, surface: pygame.Surface) -> None:
        if self.isRanged:
            surface.blit(self.image, self.collider)
    
    def toJsonObj(self) -> dict:
        return {
            "owner_collider": dataclasses.asdict(self.owner_collider),
            "damage": self.damage,
            "direction": self.direction,
            "duration": self.duration,
            "time_left": self.time_left,
            "offset": self.offset,
            "velocity": self.velocity,
            "isRanged": self.isRanged,
            "collider": dataclasses.asdict(self.collider),
        }
