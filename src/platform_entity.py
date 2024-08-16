import pygame


class Platform:
    def __init__(self, gs) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        self.collider = pygame.Rect(0.0, 300.0, 300.0, 30.0)

    def tick(self, delta_time) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface=surface, color=(200, 200, 200), rect=self.collider)
