import pygame

class HealthBar:
    def __init__(self, max_hp, width=60, height=8, offset_y=40):
        self.max_hp = max_hp
        self.hp = max_hp
        self.width = width
        self.height = height
        self.offset_y = offset_y  # pixels above the sprite center

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)

    @property
    def is_dead(self):
        return self.hp <= 0

    def draw(self, screen, x, y):
        bar_x = int(x - self.width / 2)
        bar_y = int(y - self.offset_y)
        ratio = self.hp / self.max_hp

        # Background
        pygame.draw.rect(screen, (180, 0, 0), (bar_x, bar_y, self.width, self.height))
        # Health remaining
        pygame.draw.rect(screen, (0, 220, 0), (bar_x, bar_y, int(self.width * ratio), self.height))
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.width, self.height), 1)