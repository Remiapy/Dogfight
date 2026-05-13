import pygame
import math

class Missile:
    def __init__(self, x, y, angle, speed, lifetime=3000):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def get_target_angle(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        return math.degrees(math.atan2(dx, -dy))

    def angle_to_target(self, target_x, target_y):
        target_angle = self.get_target_angle(target_x, target_y)
        diff = (target_angle - self.angle) % 360 - 180
        return diff

    def move(self, screen_width, screen_height):
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed
        self.x %= screen_width
        self.y %= screen_height

    def update(self, screen_width, screen_height):
        if self.is_expired():
            self.alive = False
            return
        self.move(screen_width, screen_height)