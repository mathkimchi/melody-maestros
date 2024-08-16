import pygame
from attack import Attack
from collider import Collider, get_collision_direction


class Fighter:
    def __init__(self, gs) -> None:
        self.gs = gs  # NOTE: can not type hint game state bc circular import
        # TODO: use in-game scale different from pixel scale
        
        self.direction = 1 # -1 is left, 1 is right
        self.move_input = 0
        self.velocity: pygame.Vector2 = pygame.Vector2()
        self.collider = Collider(0.0, 0.0, 50.0, 100.0)

        self.attacks: list[Attack] = []

        self.jump_strength = -400
        self.is_grounded = False
        self.move_speed = 1500
        self.air_control = 0.4
        
        self.ground_friction = 0.8
        self.air_friction = 0.95
        
        self.ground_offset = 1 # used to stop jittering

    def tick(self, delta_time) -> None:
        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1
            
        if self.is_grounded:
            self.velocity.x += self.move_input * self.move_speed * delta_time
        else:
            self.velocity.x += self.move_input * self.move_speed * self.air_control * delta_time

        self.is_grounded = False

        # collisions
        # platform collision
        for platform in self.gs.platforms:
            other_collider: Collider = platform.collider
            if self.collider.colliderect(other_collider):
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

        # apply friction
        if self.is_grounded:
            self.velocity.x *= self.ground_friction
        else:
            self.velocity.x *= self.air_friction

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

        # dbg
        # print(f"{delta_time=}")
        print(f"{self.is_grounded=}")
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
                (self.collider.right() - triangle_height, self.collider.centery() - triangle_base // 2),
                (self.collider.right() - triangle_height, self.collider.centery() + triangle_base // 2)
            ]
        else: 
            points = [
                (self.collider.left(), self.collider.centery()),
                (self.collider.left() + triangle_height, self.collider.centery() - triangle_base // 2),
                (self.collider.left() + triangle_height, self.collider.centery() + triangle_base // 2)
            ]
        pygame.draw.polygon(surface, (0, 255, 0), points)  # Green triangle

        # draw "children"
        for attack in self.attacks:
            attack.draw(surface=surface)

    def move_left(self) -> None:
        self.move_input = -1

    def move_right(self) -> None:
        self.move_input = 1
    
    def stop(self) -> None:
        self.move_input = 0

    def jump(self) -> None:
        if self.is_grounded:
            self.velocity.y = self.jump_strength
            self.is_grounded = False