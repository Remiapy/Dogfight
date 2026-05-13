import pygame
import math
import ctypes
from resources import *
from plane import Plane
from bullet import Bullet
from round_manager import RoundManager
from upgrade import UpgradeScreen
from hud import HUD

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
screen.set_alpha(None)

colorkey = (0, 0, 0)
screen.set_colorkey(colorkey)

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowLongW(hwnd, -20,
    ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, 0x1)

font = pygame.font.SysFont("Courier New", 72)
font_small = pygame.font.SysFont("Courier New", 36)

hud = HUD(screen_width, screen_height)

# Game states
STATE_PLAYING   = "playing"
STATE_UPGRADE   = "upgrade"
STATE_DEAD      = "dead"

def new_game():
    global plane, round_manager, player_bullets, enemy_bullets
    global player_shoot_cooldown, last_player_shot, state
    plane = Plane(screen_width, screen_height)
    round_manager = RoundManager(screen_width, screen_height)
    player_bullets = []
    enemy_bullets = []
    last_player_shot = 0
    state = STATE_PLAYING
    round_manager.start_round()

upgrade_screen = UpgradeScreen(screen_width, screen_height)
new_game()

clock = pygame.time.Clock()

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and state == STATE_DEAD:
                new_game()
        if event.type == pygame.MOUSEBUTTONDOWN and state == STATE_UPGRADE:
            chosen = upgrade_screen.handle_click(event.pos)
            if chosen:
                plane.apply_upgrade(chosen)
                # Restore some health between rounds
                plane.health.hp = min(plane.health.hp + 150, plane.health.max_hp)
                round_manager.start_round()
                player_bullets.clear()
                enemy_bullets.clear()
                state = STATE_PLAYING

    keys = pygame.key.get_pressed()

    if state == STATE_PLAYING:
        if not plane.alive:
            state = STATE_DEAD
        elif round_manager.all_dead:
            upgrade_screen.new_round(round_manager.round_num + 1)
            state = STATE_UPGRADE
        else:
            # Player shoot
            if keys[pygame.K_SPACE] and now - last_player_shot > plane.fire_cooldown:
                player_bullets.append(Bullet(plane.x, plane.y, plane.angle, color=(255, 255, 0)))
                last_player_shot = now

            plane.update(keys, screen_width, screen_height)

            for enemy in round_manager.enemies:
                enemy.update(plane.x, plane.y, screen_width, screen_height, enemy_bullets)

            # Player bullets hit enemies
            for b in player_bullets:
                b.update(screen_width, screen_height)
                for enemy in round_manager.enemies:
                    if not enemy.alive:
                        continue
                    dx = b.x - enemy.x
                    dy = b.y - enemy.y
                    if math.sqrt(dx*dx + dy*dy) < 30:
                        enemy.health.take_damage(plane.bullet_damage)
                        b.alive = False
                        break

            # Enemy bullets hit player
            for b in enemy_bullets:
                b.update(screen_width, screen_height)
                dx = b.x - plane.x
                dy = b.y - plane.y
                if math.sqrt(dx*dx + dy*dy) < 30:
                    plane.health.take_damage(10)
                    b.alive = False

            player_bullets = [b for b in player_bullets if b.alive]
            enemy_bullets  = [b for b in enemy_bullets  if b.alive]

    # Draw
    screen.fill(colorkey)
    plane.draw(screen)
    for enemy in round_manager.enemies:
        enemy.draw(screen)
    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)

    # HUD — round number
    if state == STATE_PLAYING:
        r_text = font_small.render(f"Round {round_manager.round_num}", True, (255, 255, 255))
        screen.blit(r_text, (10, 10))

    if state == STATE_UPGRADE:
        upgrade_screen.draw(screen, round_manager.round_num + 1)

    if state == STATE_DEAD:
        t = font.render("YOU DIED  —  R to restart", True, (255, 50, 50))
        screen.blit(t, t.get_rect(center=(screen_width // 2, screen_height // 2)))

    if state == STATE_PLAYING or state == STATE_UPGRADE:
        hud.draw(screen, plane, round_manager, round_manager.round_num)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()