import pygame

UPGRADES = [
    {"name": "TWR upgrade",      "desc": "Increase acceleration by 0.02"},
    {"name": "Rapid Fire",       "desc": "Reduce fire cooldown by 30ms"},
    {"name": "Plating",           "desc": "Increase max HP by 25"},
    {"name": "Better canards",          "desc": "Increase turn speed by 1"},
    {"name": "Extra millimeter",     "desc": "Bullets deal 10 more damage"},
]

class UpgradeScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.SysFont(None, 60)
        self.font_option = pygame.font.SysFont(None, 42)
        self.font_desc = pygame.font.SysFont(None, 22)
        self.options = []
        self.rects = []

    def new_round(self, round_num):
        import random
        # Pick 3 random upgrades
        self.options = random.sample(UPGRADES, 3)
        self.rects = []
        card_w, card_h = 200, 120
        gap = 60
        total_w = 3 * card_w + 2 * gap
        start_x = (self.screen_width - total_w) // 2
        y = self.screen_height // 2 - card_h // 2
        for i in range(3):
            x = start_x + i * (card_w + gap)
            self.rects.append(pygame.Rect(x, y, card_w, card_h))

    def draw(self, screen, round_num):
        # Dim background
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font_title.render(f"Round {round_num} — Choose an Upgrade", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.screen_width // 2, self.screen_height // 3 - 60)))

        mouse = pygame.mouse.get_pos()
        for i, (rect, upgrade) in enumerate(zip(self.rects, self.options)):
            hovered = rect.collidepoint(mouse)
            color = (80, 120, 200) if hovered else (40, 60, 120)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)

            name = self.font_option.render(upgrade["name"], True, (255, 255, 255))
            desc = self.font_desc.render(upgrade["desc"], True, (200, 200, 200))
            screen.blit(name, name.get_rect(center=(rect.centerx, rect.centery - 18)))
            screen.blit(desc, desc.get_rect(center=(rect.centerx, rect.centery + 18)))

    def handle_click(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return self.options[i]
        return None