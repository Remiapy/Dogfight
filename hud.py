import pygame
import math
import random

class HUD:
    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height
        self.font_large = pygame.font.SysFont("Courier New", 22, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_tiny  = pygame.font.SysFont("Courier New", 11)
        self.green      = (0, 255, 100)
        self.dim_green  = (0, 140, 60)
        self.dark_green = (0, 60, 30)
        self.amber      = (255, 180, 0)
        self.red        = (255, 50, 50)
        self.glitch_timer = 0

    def _color_for_hp(self, ratio):
        if ratio > 0.5:
            return self.green
        elif ratio > 0.25:
            return self.amber
        else:
            return self.red

    def _draw_bar(self, screen, x, y, w, h, ratio, color):
        pygame.draw.rect(screen, self.dark_green, (x, y, w, h))
        pygame.draw.rect(screen, color, (x, y, int(w * ratio), h))
        pygame.draw.rect(screen, self.dim_green, (x, y, w, h), 1)
        # Tick marks
        for i in range(1, 4):
            tx = x + int(w * i / 4)
            pygame.draw.line(screen, self.dim_green, (tx, y), (tx, y + h), 1)

    def _draw_compass(self, screen, cx, cy, angle):
        r = 22
        pygame.draw.circle(screen, self.dark_green, (cx, cy), r)
        pygame.draw.circle(screen, self.dim_green, (cx, cy), r, 1)
        # Cardinal ticks
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            inner = r - (5 if deg % 90 == 0 else 3)
            x1 = cx + math.sin(rad) * inner
            y1 = cy - math.cos(rad) * inner
            x2 = cx + math.sin(rad) * r
            y2 = cy - math.cos(rad) * r
            pygame.draw.line(screen, self.dim_green, (int(x1), int(y1)), (int(x2), int(y2)), 1)
        # Heading needle
        rad = math.radians(angle)
        nx = cx + math.sin(rad) * (r - 5)
        ny = cy - math.cos(rad) * (r - 5)
        pygame.draw.line(screen, self.green, (cx, cy), (int(nx), int(ny)), 2)
        # Center dot
        pygame.draw.circle(screen, self.green, (cx, cy), 2)

    def _scanline(self, screen, x, y, w, h):
        for row in range(y, y + h, 4):
            s = pygame.Surface((w, 1), pygame.SRCALPHA)
            s.fill((0, 0, 0, 40))
            screen.blit(s, (x, row))

    def draw(self, screen, plane, round_manager, round_num):
        now = pygame.time.get_ticks()
        pad = 10
        w, h = 220, 210
        x = pad
        y = self.sh - h - pad

        # Panel background
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 20, 10, 190))
        screen.blit(panel, (x, y))

        # Outer border with corner cuts
        pts = [
            (x + 10, y),
            (x + w,  y),
            (x + w,  y + h - 10),
            (x + w - 10, y + h),
            (x,      y + h),
            (x,      y + 10),
        ]
        pygame.draw.polygon(screen, self.dim_green, pts, 1)

        # Corner accents
        pygame.draw.line(screen, self.green, (x, y + 10), (x + 10, y), 1)
        pygame.draw.line(screen, self.green, (x + w - 10, y + h), (x + w, y + h - 10), 1)

        # Scanlines
        self._scanline(screen, x, y, w, h)

        lx = x + 12
        cy = y + 14

        # Header
        header = self.font_small.render("[ PILOT SYSTEMS ]", True, self.green)
        screen.blit(header, (lx, cy))
        pygame.draw.line(screen, self.dim_green, (lx, cy + 16), (x + w - 12, cy + 16), 1)
        cy += 22

        # HP bar
        hp_ratio = plane.health.hp / plane.health.max_hp
        hp_color = self._color_for_hp(hp_ratio)
        label = self.font_small.render(f"HULL  {plane.health.hp:>3}/{plane.health.max_hp}", True, hp_color)
        screen.blit(label, (lx, cy))
        cy += 16
        self._draw_bar(screen, lx, cy, w - 24, 10, hp_ratio, hp_color)
        cy += 16

        # Speed bar
        spd_ratio = plane.speed / plane.max_speed
        spd_label = self.font_small.render(f"SPD   {plane.speed:>4.1f}/{plane.max_speed:.1f}", True, self.green)
        screen.blit(spd_label, (lx, cy))
        cy += 16
        self._draw_bar(screen, lx, cy, w - 24, 10, spd_ratio, self.green)
        cy += 16

        # Divider
        pygame.draw.line(screen, self.dim_green, (lx, cy), (x + w - 12, cy), 1)
        cy += 6

        # Compass + stats side by side
        compass_cx = lx + 22
        compass_cy = cy + 22
        self._draw_compass(screen, compass_cx, compass_cy, plane.angle)

        sx = lx + 54
        heading = plane.angle % 360
        self.font_small.render(f"HDG", True, self.dim_green)
        screen.blit(self.font_small.render(f"HDG  {heading:>5.1f}°", True, self.green), (sx, cy))
        screen.blit(self.font_small.render(f"RND  {round_num:>5}", True, self.green), (sx, cy + 14))
        enemies_left = sum(1 for e in round_manager.enemies if e.alive)
        screen.blit(self.font_small.render(f"TGT  {enemies_left:>5}", True,
            self.amber if enemies_left > 0 else self.green), (sx, cy + 28))
        screen.blit(self.font_small.render(f"DMG  {plane.bullet_damage:>5}", True, self.green), (sx, cy + 42))
        cy += 54

        # Divider
        pygame.draw.line(screen, self.dim_green, (lx, cy), (x + w - 12, cy), 1)
        cy += 6

        # Fire cooldown indicator
        fire_label = self.font_small.render(f"FIRE RATE", True, self.dim_green)
        screen.blit(fire_label, (lx, cy))
        fire_ratio = 1 - (plane.fire_cooldown / 500)
        self._draw_bar(screen, lx, cy + 14, w - 24, 8, fire_ratio, self.green)

        # Glitch flicker on low HP
        if hp_ratio < 0.25 and random.random() < 0.05:
            glitch = pygame.Surface((w, 2), pygame.SRCALPHA)
            glitch.fill((0, 255, 100, 60))
            screen.blit(glitch, (x, y + random.randint(0, h)))