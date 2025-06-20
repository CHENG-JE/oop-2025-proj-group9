# level2/level2_game.py (修正版)
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import random
from level2.basic_fighter import BasicEnemyFighter, Item
from weapon import Laser
import win_or_lose
import ui

# === 常數區 ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHOOT_COOLDOWN = 15
ENEMY_SPAWN_RATE = 100
DROP_CHANCE = 0.4


# === 顯示遊戲標題畫面 ===
def show_game_title(screen):
    font = pygame.font.SysFont("arial", 50)
    text_surface = font.render("BATTLE FIGHTER BLITZ!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # 等待3秒

# === 全域物件 ===
enemy_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
all_items = pygame.sprite.Group()

# 背景圖片
lev2_map = pygame.image.load("assets/background/level2.png")
lev2_bg = pygame.transform.scale(lev2_map, (SCREEN_WIDTH, SCREEN_HEIGHT))

# === 初始化 level2 ===
def init_level2(player):
    
    show_game_title(pygame.display.get_surface())
    # === 修正：重設玩家在 Level 2 的初始位置 ===
    player.rect.center = (400, 500)

    player.shoot_timer = 0
    player.kills = 0
    enemy_group.empty()
    laser_group.empty()
    enemy_lasers.empty()
    all_items.empty()

# === 更新 level2 每幀邏輯 ===
def update_level2(player, screen, keys): # 接收 keys 參數
    # --- 畫背景 ---
    screen.blit(lev2_bg, (0, 0))

    # --- 自動射擊 ---
    player.shoot_timer += 1
    if player.shoot_timer >= SHOOT_COOLDOWN:
        player.shoot_timer = 0
        if 200 > getattr(player, 'exp', 0) >= 100:
            laser = Laser(player.rect.centerx, player.rect.top, "up", speed=12, color=(0, 255, 255, 200), width=10, height=30, damage=70)
        elif getattr(player, 'exp', 0) >= 200:
            laser = Laser(player.rect.centerx, player.rect.top, "up", speed=15, color=(0, 255, 0, 200), width=10, height=30, damage=100)
        else:
            laser = Laser(player.rect.centerx, player.rect.top, "up")
        laser_group.add(laser)

    # --- 生成敵機 ---
    spawn_rate = ENEMY_SPAWN_RATE
    if 10 < player.kills <= 20:
        spawn_rate = ENEMY_SPAWN_RATE * 2
    
    if random.randint(1, spawn_rate) == 1:
        x = random.randint(50, SCREEN_WIDTH - 50)
        if 20 >= player.kills > 10:
            from level2.fast_fighter import FastEnemy
            enemy = FastEnemy((x, -40))
        elif player.kills > 20:
            from level2.spaceship_fighter import SpaceEnemy
            enemy = SpaceEnemy((x, -40))
        else:
            enemy = BasicEnemyFighter((x, -40))
        enemy_group.add(enemy)

    # --- 更新所有物件 ---
    laser_group.update()
    enemy_group.update()
    enemy_lasers.update()
    all_items.update()

    # --- 敵機隨機射擊 ---
    for enemy in enemy_group:
        if not hasattr(enemy, 'shoot_timer'):
            enemy.shoot_timer = 0
        enemy.shoot_timer += 1
        if enemy.shoot_timer >= 40 and random.randint(1, 90) == 1:
            if 20 > player.kills >=10:
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 8, (255,255,255,180), 5, 30, 20)
            elif player.kills >=20:
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 1.5, (255,255,255,180), 5, 30, 5)
            else:
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 4, (255,255,255,180), 5, 30, 10)
            enemy_lasers.add(laser)
            enemy.shoot_timer = 0
    
    # --- 敵機出界與穿過防線扣血 ---
    for enemy in list(enemy_group):
        if enemy.rect.top > SCREEN_HEIGHT:
            if player.kills >= 20: player.blood -= 3
            elif player.kills >= 10: player.blood -= 10
            elif player.kills > 0: player.blood -= 5
            enemy.kill()
            if player.blood <= 0:
                win_or_lose.display(screen, player, False, "level2")
                return "game_over"

    # --- 子彈與敵機碰撞處理 ---
    for laser in laser_group:
        hits = pygame.sprite.spritecollide(laser, enemy_group, False)
        if hits:
            laser.kill()
            for enemy in hits:
                enemy.health -= laser.damage
                if enemy.health <= 0:
                    enemy.kill()
                    player.kills += 1
                    if player.kills % 10 == 0:
                        player.blood = min(player.blood + 20, player.max_blood)
                    if random.random() < DROP_CHANCE:
                        all_items.add(Item(enemy.rect.center))
    
    # --- 玩家被敵機子彈打中時的碰撞判斷與扣血 (恢復原始設計) ---
    hits = pygame.sprite.spritecollide(player, enemy_lasers, True) or pygame.sprite.spritecollide(player, enemy_group, True)
    for hit in hits:
        player.blood -= 10 # 直接扣血，沒有無敵
        if player.blood <= 0:
            win_or_lose.display(screen, player, False, "level2")
            return "game_over"
            
    # --- 玩家勝利判斷 ---
    if player.kills >= 40:
        win_or_lose.display(screen, player, True, "level2")
        return "game_over"

    # --- 撿寶物處理 (恢復原始設計) ---
    pickups = pygame.sprite.spritecollide(player, all_items, True)
    for item in pickups:
        if item.image.get_at((0, 0))[:3] == (255, 255, 0):  # 黃色：加經驗值
            player.exp += 10
        elif item.image.get_at((0, 0))[:3] == (255, 0, 0):
            player.blood = min(player.blood + 20, player.max_blood)
            
    # --- 繪製所有物件 ---
    player.draw(screen)
    laser_group.draw(screen)
    enemy_group.draw(screen)
    enemy_lasers.draw(screen)
    all_items.draw(screen)
    
    # --- 繪製UI ---
    ui.draw_player_stats(screen, player)
    ui.draw_level_hud(screen, "level2", kills=player.kills)
    
    return None