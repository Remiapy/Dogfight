import pygame
import math
import random

class StartScreen:
    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height
        self.font_title  = pygame.font.SysFont("Courier New", 64, bold=True)
        self.font_sub    = pygame.font.SysFont("Courier New", 20, bold=True)
        self.font_small  = pygame.font.SysFont("Courier New", 14)
        self.green       = (0, 255, 100)
        self.dim_green   = (0, 140, 60)
        self.dark_green  = (0, 40, 20)
        self.amber       = (255, 180, 0)

        # Button
        bw, bh = 220, 50
        self.btn_rect = pygame.Rect(
            screen_width  // 2 - bw // 2,
            screen_height // 2 + 60,
            bw, bh
        )

        # Randomised radar blips
        self.blips = [
            (random.randint(50, screen_width - 50),
             random.randint(50, screen_height - 50),
             random.random() * 2 * math.pi)
            for _ in range(12)
        ]
        self.spawn_time = pygame.time.get_ticks()

    def handle_click(self, pos):
        return self.btn_rect.collidepoint(pos)

    def draw(self, screen):
        now  = pygame.time.get_ticks()
        t    = (now - self.spawn_time) / 1000.0
        cx   = self.sw // 2
        cy   = self.sh // 2

        screen.fill((0, 0, 0))

        # Scrolling scanlines
        for row in range(0, self.sh, 4):
            offset = int(t * 30) % 4
            s = pygame.Surface((self.sw, 1), pygame.SRCALPHA)
            s.fill((0, 255, 100, 12))
            screen.blit(s, (0, (row + offset) % self.sh))

        # Radar circle background
        for r in range(200, 0, -40):
            alpha = 20 + r // 10
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 255, 100, alpha), (r, r), r, 1)
            screen.blit(s, (cx - r, cy - r))

        # Rotating radar sweep
        sweep_angle = (t * 60) % 360
        for i in range(30):
            a = math.radians(sweep_angle - i * 3)
            fade = int(80 * (1 - i / 30))
            end_x = cx + math.cos(a) * 200
            end_y = cy + math.sin(a) * 200
            s = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
            pygame.draw.line(s, (0, 255, 100, fade), (cx, cy), (int(end_x), int(end_y)), 2)
            screen.blit(s, (0, 0))

        # Radar blips that appear as sweep passes
        for bx, by, _ in self.blips:
            bangle = math.degrees(math.atan2(by - cy, bx - cx)) % 360
            diff   = (sweep_angle - bangle) % 360
            if diff < 60:
                alpha = int(255 * (1 - diff / 60))
                s = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(s, (0, 255, 100, alpha), (4, 4), 3)
                screen.blit(s, (bx - 4, by - 4))

        # Cross hairs
        pygame.draw.line(screen, (0, 80, 40), (cx, 0),       (cx, self.sh),  1)
        pygame.draw.line(screen, (0, 80, 40), (0,  cy),      (self.sw, cy),  1)

        # Title
        title = self.font_title.render("VECTOR LEAD", True, self.green)
        shadow = self.font_title.render("VECTOR LEAD", True, self.dark_green)
        screen.blit(shadow, title.get_rect(center=(cx + 2, self.sh // 2 - 80 + 2)))
        screen.blit(title,  title.get_rect(center=(cx,     self.sh // 2 - 80)))

        sub = self.font_sub.render("AERIAL COMBAT SYSTEM  v1.0", True, self.dim_green)
        screen.blit(sub, sub.get_rect(center=(cx, self.sh // 2 - 30)))

        # Divider
        pygame.draw.line(screen, self.dim_green,
            (cx - 160, self.sh // 2),
            (cx + 160, self.sh // 2), 1)

        # Start button
        mouse   = pygame.mouse.get_pos()
        hovered = self.btn_rect.collidepoint(mouse)
        color   = self.green if hovered else self.dim_green
        pygame.draw.rect(screen, (0, 30, 15),   self.btn_rect, border_radius=4)
        pygame.draw.rect(screen, color,          self.btn_rect, 1, border_radius=4)

        # Corner accents on button
        r = self.btn_rect
        pygame.draw.line(screen, self.green, (r.x, r.y + 6),         (r.x + 6, r.y),         1)
        pygame.draw.line(screen, self.green, (r.right - 6, r.bottom), (r.right, r.bottom - 6), 1)

        label = self.font_sub.render("[ LAUNCH MISSION ]", True, color)
        screen.blit(label, label.get_rect(center=self.btn_rect.center))

        # Blinking bottom status
        if int(t * 2) % 2 == 0:
            status = self.font_small.render(
                "CONTROLS:  ARROW KEYS — MOVE     SPACE — FIRE     ESC — ABORT",
                True, self.dim_green)
            screen.blit(status, status.get_rect(center=(cx, self.sh - 30)))