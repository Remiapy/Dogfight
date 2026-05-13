import pygame
import math
from resources import *
from health_bar import HealthBar

class Plane:
    def __init__(self, screen_width, screen_height):
        self.original_image = plane_img
        self.angle = 0
        self.turn_speed = 3
        self.speed = 4
        self.max_speed = 8
        self.acceleration = 0.06
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.health = HealthBar(max_hp=150)
        self.alive = True
        self.speed_death_timer = 3
        self.speed_death_delay = 3000
        self.bullet_damage = 10
        self.fire_cooldown = 150

    def apply_upgrade(self, upgrade):
        name = upgrade["name"]
        if name == "TWR upgrade":
            self.acceleration += 0.02
        elif name == "Rapid Fire":
            self.fire_cooldown = max(50, self.fire_cooldown - 30)
        elif name == "Plating":
            self.health.max_hp += 25
            self.health.hp += 25
        elif name == "Better canards":
            self.turn_speed += 1
        elif name == "Extra millimeter":
            self.bullet_damage += 10

    def update(self, keys, screen_width, screen_height):
        if not self.alive:
            return

        effective_turn = self.turn_speed * (self.speed / self.max_speed)

        if keys[pygame.K_LEFT]:
            self.angle -= effective_turn
        if keys[pygame.K_RIGHT]:
            self.angle += effective_turn

        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            self.speed = max(self.speed - 0.025, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.speed = max(self.speed - effective_turn * 0.03, 0)

        if keys[pygame.K_SPACE]:
            self.speed = min(self.speed - self.bullet_damage * 0.002, self.max_speed)

        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed

        self.x %= screen_width
        self.y %= screen_height

        if self.speed <= 0:
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