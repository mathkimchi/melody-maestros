import pygame
from attack import Attack


class Fighter:
    def __init__(self, gs) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        # TODO: use in-game scale different from pixel scale
        self.velocity = pygame.Vector2()
        self.collider = pygame.Rect(0, 0, 50, 100)

        self.attacks: list[Attack] = []

    def tick(self, delta_time) -> None:
        self.collider.move_ip(self.velocity * delta_time)

        self.velocity = pygame.Vector2()

        # collisions

        # ground collision

        # update "children"
        # update attacks and remove those who are finished
        self.attacks = [attack for attack in self.attacks if attack.tick(delta_time)]

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface=surface, color=(255, 0, 0), rect=self.collider)

        # draw "children"
        for attack in self.attacks:
            attack.draw(surface=surface)

    def move_left(self) -> None:
        self.velocity.x = -100

    def move_right(self) -> None:
        self.velocity.x = +100

    def jump(self) -> None:
        pass

    def fast_attack(self) -> None:
        self.attacks.append(Attack(self))

    def strong_attack(self) -> None:
        pass

    def block(self) -> None:
        pass
