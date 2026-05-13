import pygame
import math
from resources import *
from bullet import Bullet
from health_bar import HealthBar

class Enemy:
    def __init__(self, screen_width, screen_height, x=None, y=None):
        self.original_image = enemy_img
        self.angle = 0
        self.turn_speed = 1.7
        self.speed = 1
        self.max_speed = 6
        self.acceleration = 0.06
        self.x = x if x is not None else screen_width / 4
        self.y = y if y is not None else screen_height / 4
        self.shoot_cooldown = 800
        self.last_shot = 0
        self.fire_angle = 15
        self.health = HealthBar(max_hp=100)
        self.alive = True
        self.speed_death_timer = 0
        self.speed_death_delay = 3000

    def update(self, player_x, player_y, screen_width, screen_height, bullets):
        if not self.alive:
            return

        dx = player_x - self.x
        dy = player_y - self.y
        target_angle = math.degrees(math.atan2(dx, -dy))
        angle_diff = (target_angle - self.angle + 180) % 360 - 180

        if angle_diff > 0:
            self.angle += min(self.turn_speed, angle_diff)
        elif angle_diff < 0:
            self.angle += max(-self.turn_speed, angle_diff)

        if abs(angle_diff) < 90:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            self.speed = max(self.speed - self.acceleration * 0.05, 0)

        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed

        self.x %= screen_width
        self.y %= screen_height

        now = pygame.time.get_ticks()
        if abs(angle_diff) < self.fire_angle and now - self.last_shot > self.shoot_cooldown:
            bullets.append(Bullet(self.x, self.y, self.angle, color=(255, 50, 50)))
            self.last_shot = now

        if self.speed == 0:
            self.speed_death_timer += pygame.time.get_ticks()
            if self.speed_death_timer >= self.speed_death_delay:
                self.alive = False
        else:
            self.speed_death_timer = 3

        if self.health.is_dead:
            self.alive = False

    def draw(self, screen):
        if not self.alive:
            return
        rotated = pygame.transform.rotate(self.original_image, -self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)
        self.health.draw(screen, self.x, self.y)