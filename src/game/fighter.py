import pygame
from .attack import Attack
from .collider import Collider, get_collision_direction
from abc import ABC, abstractmethod
from .player_actions import PlayerActionSet
import dataclasses

JUMP_STRENGTH = -400
MOVE_SPEED = 1500
AIR_CONTROL = 0.4

GROUND_FRICTION = 0.8
AIR_FRICTION = 0.95


class Fighter(ABC):
    def __init__(
        self, gs, player_id: int, direction=1, move_input=0, velocity=None, collider=None, attacks=None
    ) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        # TODO: use in-game scale different from pixel scale

        # set defaults for arguments that are None
        if velocity == None:
            velocity = pygame.Vector2()
        if collider == None:
            collider = Collider(0.0, 0.0, 50.0, 100.0)
        if attacks == None:
            attacks = []

        self.player_id = player_id
        self.direction = direction  # -1 is left, 1 is right
        self.move_input = move_input
        self.velocity: pygame.Vector2 = velocity
        self.collider = collider

        self.attacks: list[Attack] = attacks

        self.is_grounded = False

    def tick(self, delta_time) -> None:
        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1

        if self.is_grounded:
            self.velocity.x += self.move_input * MOVE_SPEED * delta_time
        else:
            self.velocity.x += self.move_input * MOVE_SPEED * AIR_CONTROL * delta_time

        self.is_grounded = False

        # collisions
        # platform collision
        for platform in self.gs.platforms:
            other_collider: Collider = platform.collider
            if self.collider.colliderect(other_collider, count_touching=True):
                collision_direction = get_collision_direction(
                    self.collider, other_collider
                )
                if collision_direction.x > 0:
                    # horizontal collision, platform is to the right, need to move player to the left st player right = other left
                    # player x + player width = other x
                    self.collider.x = other_collider.x - self.collider.width
                    self.velocity.x = 0
                elif collision_direction.x < 0:
                    # horizontal collision, platform is to the left, need to move player to the right st player left = other right
                    self.collider.x = other_collider.right()
                    self.velocity.x = 0
                elif (
                    collision_direction.y > 0
                    or collision_direction.magnitude_squared == 0
                ):
                    # if just touching, then assume it is this case
                    # vertical collision, platform has greater y, platform is below (+y -> below)
                    self.collider.y = other_collider.top() - self.collider.height
                    self.velocity.y = 0
                    self.is_grounded = True

        # other players collision
        for (other_player_id, other_fighter) in self.gs.player_id.items():
            if self.player_id == other_player_id:
                continue
            
            other_collider = other_fighter.collider
            if self.collider.colliderect(other_collider):
                collision_direction = get_collision_direction(self.collider, other_collider)

                if collision_direction.x > 0:
                    # horizontal collision, other is to the right, need to move player to the left st player right = other left
                    # player x + player width = other x
                    self.collider.x = other_collider.x - self.collider.width
                    self.velocity.x = min(self.velocity.x, 0)
                elif collision_direction.x < 0:
                    # horizontal collision, other is to the left, need to move player to the right st player left = other right
                    self.collider.x = other_collider.right()
                    self.velocity.x = max(self.velocity.x, 0)
                elif collision_direction.y > 0:
                    # vertical collision, other has greater y, other is below (+y -> below)
                    self.collider.y = other_collider.top() - self.collider.height
                    self.velocity.y = 0


        # apply friction
        if self.is_grounded:
            self.velocity.x *= GROUND_FRICTION
        else:
            self.velocity.x *= AIR_FRICTION

        # clamp velocity just to be safe
        if self.velocity.magnitude_squared() > 0.001:
            # clamp breaks when 0 vec
            self.velocity.clamp_magnitude_ip(1000.0)

        # apply velocity
        self.collider.move_ip(delta_time * self.velocity)

        # apply gravity
        if not self.is_grounded:
            self.velocity += delta_time * pygame.Vector2(0, 800.0)

        # update "children"
        # update attacks and remove those who are finished
        self.attacks = [attack for attack in self.attacks if attack.tick(delta_time)]

        # debug
        # print(f"{delta_time=}")
        # print(f"{self.is_grounded=}")
        # print(f"{self.velocity=}")
        # print(f"{self.collider=}")

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface=surface, color=(255, 0, 0), rect=self.collider.get_rect()
        )

        triangle_base = 20
        triangle_height = 10
        if self.direction == 1:
            points = [
                (self.collider.right(), self.collider.centery()),
                (
                    self.collider.right() - triangle_height,
                    self.collider.centery() - triangle_base // 2,
                ),
                (
                    self.collider.right() - triangle_height,
                    self.collider.centery() + triangle_base // 2,
                ),
            ]
        else:
            points = [
                (self.collider.left(), self.collider.centery()),
                (
                    self.collider.left() + triangle_height,
                    self.collider.centery() - triangle_base // 2,
                ),
                (
                    self.collider.left() + triangle_height,
                    self.collider.centery() + triangle_base // 2,
                ),
            ]
        pygame.draw.polygon(surface, (0, 255, 0), points)  # Green triangle

        # draw "children"
        for attack in self.attacks:
            attack.draw(surface=surface)

    def process_action_set(self, action_set: PlayerActionSet):
        self.move_input = action_set.walk_direction

        if action_set.jump:
            self.jump()

        if action_set.attack == 1:
            self.do_fast_attack()
        elif action_set.attack == 2:
            self.do_fast_attack()

    def jump(self) -> None:
        if self.is_grounded:
            # print("Jumped!")
            self.velocity.y = JUMP_STRENGTH
            self.collider.y -= 0.001 # get it off ground
            self.is_grounded = False

    def do_fast_attack(self):
        self.attacks.append(self.generate_fast_attack())

    def do_strong_attack(self):
        self.attacks.append(self.generate_strong_attack())

    @abstractmethod
    def generate_fast_attack(self) -> Attack:
        pass

    @abstractmethod
    def generate_strong_attack(self) -> Attack:
        pass

    def toJsonObj(self) -> dict[str, object]:
        return {
            "type": str(type(self)),
            "player_id": self.player_id,
            "direction": self.direction,
            "move_input": self.move_input,
            "velocity": (self.velocity.x, self.velocity.y),
            "collider": dataclasses.asdict(self.collider),
            "attacks": self.attacks,
            "is_grounded": self.is_grounded,
        }
