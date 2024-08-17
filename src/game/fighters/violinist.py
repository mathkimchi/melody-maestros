from ..fighter import Fighter
from ..attack import Attack
import pygame


class Violinist(Fighter):
    def __init__(self, gs, **kwargs):
        super().__init__(gs, **kwargs)

    def tick(self, delta_time):
        super().tick(delta_time)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

    def generate_fast_attack(self) -> Attack:
        return Attack(self, damage=10, duration=0.1, direction=self.direction)

    def generate_strong_attack(self) -> Attack:
        return Attack(self, damage=20, duration=0.1, direction=self.direction)
