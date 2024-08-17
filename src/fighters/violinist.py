from fighter import Fighter
from attack import Attack
import pygame

class Violinist(Fighter):
    def __init__(self, gs):
        super().__init__(gs)
        self.load_idle_animation()
        self.current_frame = 0
        self.animation_speed = 0.1
    
    def load_idle_animation(self):
        try:
            # Load the GIF
            self.idle_frames = []
            idle_gif = pygame.image.load("path/to/your/idle_animation.gif")
            
            # Extract frames from the GIF
            frame_count = idle_gif.get_frames_count()
            for i in range(frame_count):
                frame_surface = idle_gif.get_frame_surface(i)
                # Scale the frame to match the collider size if necessary
                scaled_frame = pygame.transform.scale(frame_surface, (int(self.collider.width), int(self.collider.height)))
                self.idle_frames.append(scaled_frame)
        except pygame.error as e:
            print(f"Error loading idle animation: {e}")
            # Fallback to a simple surface if loading fails
            self.idle_frames = [pygame.Surface((int(self.collider.width), int(self.collider.height)))]
            self.idle_frames[0].fill((255, 0, 0))  # Red rectangle as fallback

    def tick(self, delta_time):
        super().tick(delta_time)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

    def fast_attack(self):
        self.attacks.append(Attack(self, damage=10, duration = 0.1, direction=self.direction))

    def strong_attack(self):
        self.attacks.append(Attack(self))
