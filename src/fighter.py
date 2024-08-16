import pygame
from attack import Attack
from collider import Collider, get_collision_direction


class Fighter:
    def __init__(self, gs) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        # TODO: use in-game scale different from pixel scale
        self.velocity: pygame.Vector2 = pygame.Vector2()
        self.collider = Collider(0.0, 0.0, 50.0, 100.0)

        self.attacks: list[Attack] = []

        self.horizontal_walk = 0.0

    def tick(self, delta_time) -> None:
        # apply walk
        self.velocity.x += self.horizontal_walk
        self.horizontal_walk = 0.0

        should_gravity = True

        # collisions
        # platform collision
        for platform in self.gs.platforms:
            if self.collider.get_rect().colliderect(platform.collider):
                collision_direction = get_collision_direction(
                    self.collider.get_rect(), platform.collider
                )
                if collision_direction.x > 0:
                    # horizontal collision, platform is to the right, need to move player to the left st player right = other left
                    # player x + player width = other x
                    self.collider.x = platform.collider.x - self.collider.width
                    self.velocity.x = 0
                elif collision_direction.x < 0:
                    # horizontal collision, platform is to the left, need to move player to the right st player left = other right
                    self.collider.x = platform.collider.right
                    self.velocity.x = 0
                elif (
                    collision_direction.y > 0
                    or collision_direction.magnitude_squared == 0
                ):
                    # if just touching, then assume it is this case
                    # vertical collision, platform has greater y, platform is below (+y -> below)
                    self.collider.y = platform.collider.top - self.collider.height
                    self.velocity.y = 0
                    should_gravity = False

        # apply gravity
        if should_gravity:
            self.velocity += delta_time * pygame.Vector2(0, 10.0)

        # clamp velocity just to be safe
        if self.velocity.magnitude_squared() > 0.001:
            # clamp breaks when 0 vec
            self.velocity.clamp_magnitude_ip(200.0)

        # apply horizontal friction
        self.velocity.x *= 0.9
        if abs(self.velocity.x) < 0.001:
            self.velocity.x = 0

        # apply velocity
        self.collider.get_rect().move_ip(delta_time * self.velocity)

        # update "children"
        # update attacks and remove those who are finished
        self.attacks = [attack for attack in self.attacks if attack.tick(delta_time)]

        # dbg
        print(f"{delta_time=}")
        print(f"{should_gravity=}")
        print(f"{self.velocity=}")
        print(f"{self.collider=}")

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface=surface, color=(255, 0, 0), rect=self.collider.get_rect()
        )

        # draw "children"
        for attack in self.attacks:
            attack.draw(surface=surface)

    def move_left(self) -> None:
        self.horizontal_walk -= 100

    def move_right(self) -> None:
        self.horizontal_walk += 100

    def jump(self) -> None:
        pass

    def fast_attack(self) -> None:
        self.attacks.append(Attack(self))

    def strong_attack(self) -> None:
        pass

    def block(self) -> None:
        pass
