from fighter import Fighter
from attack import Attack
import pygame
import os

class Violinist(Fighter):
    def __init__(self, gs):
        super().__init__(gs)
        self.idle_frames = []
        self.fast_attack_frames = []
        self.current_frame = 0
        self.animation_time = 0
        self.idle_speed = 0.3  # Seconds per frame for idle animation
        self.fast_attack_speed = 0.1  # Seconds per frame for attack animation
        self.current_animation = 'idle'
        self.attack_duration = 0.5  # Total duration of attack animation
        self.attack_timer = 0
        
        self.idle_image_path = os.path.join('assets', 'violinist/violinist-idle.png')
        self.fast_attack_image_path = os.path.join('assets', 'violinist/violinist-attack.png')
        
        self.sprites_loaded = False

    def load_sprite_sheets(self):
        self.idle_frames = self.load_frames(self.idle_image_path)
        self.fast_attack_frames = self.load_frames(self.fast_attack_image_path)
        self.sprites_loaded = True

    def load_frames(self, path):
        frames = []
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sprite_sheet.get_width()
        frame_width = 64
        frame_height = 64
        
        for i in range(sheet_width // frame_width):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (int(self.collider.width), int(self.collider.height)))
            frames.append(scaled_frame)
        return frames

    def tick(self, delta_time):
        super().tick(delta_time)
        
        if not self.sprites_loaded:
            return

        self.animation_time += delta_time
        
        if self.current_animation == 'attack':
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_duration:
                self.current_animation = 'idle'
                self.attack_timer = 0
                self.current_frame = 0
            elif self.animation_time >= self.fast_attack_speed:
                self.current_frame = (self.current_frame + 1) % len(self.fast_attack_frames)
                self.animation_time = 0
        elif self.animation_time >= self.idle_speed:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.animation_time = 0

    def draw(self, surface: pygame.Surface):
        if not self.sprites_loaded:
            self.load_sprite_sheets()

        if self.current_animation == 'idle':
            current_frame = self.idle_frames[self.current_frame]
        else:
            current_frame = self.fast_attack_frames[self.current_frame]

        if self.direction == 1:  # Facing right
            surface.blit(current_frame, (self.collider.x, self.collider.y))
        else:  # Facing left
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            surface.blit(flipped_frame, (self.collider.x, self.collider.y))

        # Used to draw attack hitbox        
        for attack in self.attacks:
            attack.draw(surface)

    def fast_attack(self):
        self.attacks.append(Attack(self, damage=10, duration=0.1, direction=self.direction))
        self.current_animation = 'attack'
        self.current_frame = 0
        self.attack_timer = 0
        
    def ranged_attack(self):
        self.attacks.append(Attack(self, damage = 5, duration = 2, direction = self.direction, isRanged=True, velocity = 200))
        
