from ..fighter import Fighter
from ..attack import Attack
import pygame


class Violinist(Fighter):
    def __init__(self, gs):
        super().__init__(gs)

    def tick(self, delta_time):
        super().tick(delta_time)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

    def fast_attack(self):
        self.attacks.append(
            Attack(self, damage=10, duration=0.1, direction=self.direction)
        )

    def strong_attack(self):
        self.attacks.append(
            Attack(self, damage=20, duration=0.1, direction=self.direction)
        )
