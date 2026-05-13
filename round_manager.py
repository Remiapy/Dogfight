from enemy import Enemy

class RoundManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.round_num = 0
        self.enemies = []

    def start_round(self):
        self.round_num += 1
        self.enemies = []
        import math
        for i in range(self.round_num):
            # Space enemies around the edge
            angle = (360 / self.round_num) * i
            rad = math.radians(angle)
            x = self.screen_width // 2 + math.cos(rad) * 300
            y = self.screen_height // 2 + math.sin(rad) * 200
            x = max(50, min(self.screen_width - 50, x))
            y = max(50, min(self.screen_height - 50, y))
            self.enemies.append(Enemy(self.screen_width, self.screen_height, x, y))

    @property
    def all_dead(self):
        return all(not e.alive for e in self.enemies)