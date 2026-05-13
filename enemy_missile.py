import pygame
import math
from missile import Missile
from resources import *

class EnemyMissile(Missile):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle + 180, speed=6, lifetime=3000)
        self.turn_speed = 3
        self.tracking_angle = 45
        self.tracking = False
        self.original_image = missile_img

    def update(self, player_x, player_y, screen_width, screen_height):
        if self.is_expired():
            self.alive = False
            return

        diff = self.angle_to_target(player_x, player_y)

        # Start tracking once player enters the forward cone
        if abs(diff) < self.tracking_angle:
            self.tracking = True

        if self.tracking:
            if diff > 0:
                self.angle += min(self.turn_speed, diff)
            elif diff < 0:
                self.angle += max(-self.turn_speed, diff)

        self.move(screen_width, screen_height)

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.original_image, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)