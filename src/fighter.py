import pygame


class Fighter:
    def __init__(self) -> None:
        self.collider = pygame.Rect(0, 0, 50, 100)

    def move_left(self) -> None:
        self.collider.move_ip(-1, 0)

    def move_right(self) -> None:
        self.collider.move_ip(+1, 0)
