from ..fighter import Fighter
from ..attack import Attack
import pygame
import os

class Violinist(Fighter):
    def __init__(self, gs, **kwargs):
        super().__init__(gs, **kwargs)
        self.idle_frames = []
        self.fast_attack_frames = []
        self.ranged_attack_frames = []
        self.current_frame = 0
        self.animation_time = 0
        self.idle_speed = 0.3  
        self.fast_attack_speed = 0.1 
        self.ranged_attack_speed = 0.1
        self.current_animation = 'idle'
        self.attack_duration = 0.5 
        self.attack_timer = 0
        
        self.idle_image_path = os.path.join('assets', 'violinist/violinist-idle.png')
        self.fast_attack_image_path = os.path.join('assets', 'violinist/violinist-attack.png')
        self.ranged_attack_image_path = os.path.join('assets', 'violinist/violinist-ranged.png')
        
        self.sprites_loaded = False

    def load_sprite_sheets(self):
        self.idle_frames = self.load_frames(self.idle_image_path)
        self.fast_attack_frames = self.load_frames(self.fast_attack_image_path)
        self.ranged_attack_frames = self.load_frames(self.ranged_attack_image_path)
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
        
        if self.current_animation in ['attack', 'ranged_attack']:
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_duration:
                self.current_animation = 'idle'
                self.attack_timer = 0
                self.current_frame = 0
            else:
                frames = self.fast_attack_frames if self.current_animation == 'attack' else self.ranged_attack_frames
                speed = self.fast_attack_speed if self.current_animation == 'attack' else self.ranged_attack_speed
                if self.animation_time >= speed and frames:
                    self.current_frame = (self.current_frame + 1) % len(frames)
                    self.animation_time = 0
        elif self.animation_time >= self.idle_speed and self.idle_frames:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.animation_time = 0

    def draw(self, surface: pygame.Surface):
        if not self.sprites_loaded:
            self.load_sprite_sheets()

        if self.current_animation == 'idle' and self.idle_frames:
            current_frame = self.idle_frames[self.current_frame % len(self.idle_frames)]
        elif self.current_animation == 'attack' and self.fast_attack_frames:
            current_frame = self.fast_attack_frames[self.current_frame % len(self.fast_attack_frames)]
        elif self.current_animation == 'ranged_attack' and self.ranged_attack_frames:
            current_frame = self.ranged_attack_frames[self.current_frame % len(self.ranged_attack_frames)]
        else:
            # Fallback to first idle frame if no valid frame is found
            current_frame = self.idle_frames[0] if self.idle_frames else None

        if current_frame:
            if self.direction == 1:  # Facing right
                surface.blit(current_frame, (self.collider.x, self.collider.y))
            else:  # Facing left
                flipped_frame = pygame.transform.flip(current_frame, True, False)
                surface.blit(flipped_frame, (self.collider.x, self.collider.y))

        health_bar_width = 50 
        health_bar_height = 5 
        health_bar_y_offset = 10
        
        pygame.draw.rect(surface, (0, 255, 0), (self.collider.x, self.collider.y - health_bar_y_offset, health_bar_width, health_bar_height))
        
        current_health_length = int((self.health / 100) * health_bar_width)
        pygame.draw.rect(surface, (0, 255, 0), (self.collider.x, self.collider.y - health_bar_y_offset, current_health_length, health_bar_height))
        
        

        for attack in self.attacks:
            attack.draw(surface)

    def fast_attack(self):
        self.attacks.append(Attack(self.collider, damage=10, duration=0.1, direction=self.direction))
        self.current_animation = 'attack'
        self.current_frame = 0
        self.attack_timer = 0

    def ranged_attack(self):
        self.attacks.append(Attack(self.collider, damage=5, duration=2, direction=self.direction, isRanged=True, velocity=200))
        self.current_animation = 'ranged_attack'
        self.current_frame = 0
        self.attack_timer = 0
