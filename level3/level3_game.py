import pygame
import sys, os
import win_or_lose
import ui

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .platform import Platform
from .monster import Monster

def show_game_title(screen):
    font = pygame.font.SysFont("arial", 64)
    text_surface = font.render("LEVEL 3 - BATTLE OF THE MONSTER", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(5000)

# === 常數區 ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_Y = 500
BOUNDARIES = (50, 750)
INVINCIBLE_DURATION = 120

# === 全域物件 (Sprite Groups) ===
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_projectile_group = pygame.sprite.Group()
monster_projectile_group = pygame.sprite.Group()
monster_effect_group = pygame.sprite.Group()

# === 場景物件 ===
monster = None
lev3_bg = pygame.transform.scale(pygame.image.load("assets/background/level3.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def init_level3(main_player):
    show_game_title(pygame.display.get_surface())
    # 清空所有群組
    for group in [platform_group, enemy_group, player_projectile_group, monster_projectile_group, monster_effect_group]:
        group.empty()

    # 建立平台
    ground = Platform(0, GROUND_Y, SCREEN_WIDTH, 20)
    platform_group.add(ground)
    
    # 建立怪物
    global monster
    monster = Monster(pos=(550, GROUND_Y), boundaries=BOUNDARIES)
    enemy_group.add(monster)

def update_level3(screen, main_player, keys):
    # --- 遊戲結束判斷 ---
    if main_player.blood <= 0:
        win_or_lose.display(screen, main_player, False, "level3")
        return "game_over"
    if not enemy_group:
        win_or_lose.display(screen, main_player, True, "level3")
        return "game_over"
    
    # --- 更新物件 ---
    main_player.update(platforms=platform_group) # 傳入平台給玩家判斷重力
    main_player.handle_input(keys, projectile_group=player_projectile_group) # 傳入子彈群組給玩家發射
    
    if monster:
        monster.update(platform_group, main_player, monster_projectile_group, monster_effect_group)
    
    player_projectile_group.update()
    monster_projectile_group.update()
    monster_effect_group.update()

    # --- 碰撞檢測 ---
    # 玩家箭矢 vs 敵人
    hits = pygame.sprite.groupcollide(player_projectile_group, enemy_group, True, False)
    for projectile, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.health -= projectile.damage
            if enemy.health <= 0:
                enemy.kill()
                main_player.exp += 25

    # 玩家 vs 怪物攻擊
    if main_player.invincible_timer == 0:
        if pygame.sprite.spritecollide(main_player, monster_projectile_group, True):
            main_player.take_damage(50)
            main_player.invincible_timer = INVINCIBLE_DURATION
        
        wave_hits = pygame.sprite.spritecollide(main_player, monster_effect_group, True)
        if wave_hits:
            main_player.take_damage(wave_hits[0].damage)
            main_player.invincible_timer = INVINCIBLE_DURATION

    # --- 繪製所有內容 ---
    screen.blit(lev3_bg, (0, 0))
    
    enemy_group.draw(screen)
    player_projectile_group.draw(screen)
    monster_projectile_group.draw(screen)
    monster_effect_group.draw(screen)
    main_player.draw(screen) # === 修正：直接畫 main_player ===
    
    if monster: 
        monster.draw_health_bar(screen)
    
    # === 修正：繪製UI ===
    ui.draw_player_stats(screen, main_player)
    ui.draw_level_hud(screen, "level3", enemies_left=len(enemy_group))
    
    return None