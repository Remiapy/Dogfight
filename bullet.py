import pygame
import math

class Bullet:
    def __init__(self, x, y, angle, speed=15, lifetime=1500, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.color = color
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True
        self.radius = 4

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def update(self, screen_width, screen_height):
        if self.is_expired():
            self.alive = False
            return
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed

        # Disappear when offscreen instead of wrapping
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)