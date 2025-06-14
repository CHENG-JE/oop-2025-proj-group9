# level3/level3_game.py
import pygame
import sys, os
import win_or_lose

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from level3.platform import Platform
from level3.archer import Archer
from level3.monster import Monster

# === 常數區 ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_Y = 500
BOUNDARIES = (50, 750) # (左邊界, 右邊界)
INVINCIBLE_DURATION = 120

# === 全域物件 (Sprite Groups) ===
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_projectile_group = pygame.sprite.Group()
monster_projectile_group = pygame.sprite.Group()
monster_effect_group = pygame.sprite.Group()

# === 場景物件 ===
archer = None
monster = None
lev3_bg = pygame.transform.scale(pygame.image.load("assets/background/level3.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def init_level3(main_player):
    # 清空所有群組
    for group in [all_sprites, platform_group, player_group, enemy_group, player_projectile_group, monster_projectile_group, monster_effect_group]:
        group.empty()

    # 建立平台
    ground = Platform(0, GROUND_Y, SCREEN_WIDTH, 20)
    platform_group.add(ground)
    all_sprites.add(ground)

    # 建立玩家角色
    global archer
    archer = Archer(pos=(250, GROUND_Y), boundaries=BOUNDARIES)
    # 繼承主遊戲的狀態
    archer.money = main_player.money
    archer.exp = main_player.exp
    archer.max_blood = main_player.max_blood
    archer.blood = main_player.blood
    player_group.add(archer)
    all_sprites.add(archer)
    
    # 建立怪物
    global monster
    monster = Monster(pos=(550, GROUND_Y), boundaries=BOUNDARIES)
    enemy_group.add(monster)
    all_sprites.add(monster)

def update_level3(screen, main_player):
    # === 改正：結束時呼叫 win_or_lose.handle_game_over ===
    if archer.blood <= 0:
        win_or_lose.display(screen, main_player, False, "level3")
        return "game_over"
    if not enemy_group:
        win_or_lose.display(screen, main_player, True, "level3")
        return "game_over"
    
    # 更新物件
    keys = pygame.key.get_pressed()
    archer.update(keys, platform_group, player_projectile_group)
    if monster: # 確保 monster 存在才更新
        monster.update(platform_group, archer, monster_projectile_group, monster_effect_group)
    player_projectile_group.update()
    monster_projectile_group.update()
    monster_effect_group.update()

    # 碰撞檢測
    # 1. 玩家箭矢 vs 敵人 (不變)
    hits = pygame.sprite.groupcollide(player_projectile_group, enemy_group, True, False)
    for projectile, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.health -= projectile.damage
            if enemy.health <= 0: enemy.kill(); archer.exp += 25

    # 2. 玩家 vs 怪物攻擊 (無敵幀判斷)
    if archer.invincible_timer == 0:
        # 2a. vs 光波
        beam_hits = pygame.sprite.spritecollide(archer, monster_projectile_group, True)
        if beam_hits:
            archer.blood -= 50
            archer.invincible_timer = INVINCIBLE_DURATION
        
        # 2b. vs 震盪波 (現在只負責扣血)
        wave_hits = pygame.sprite.spritecollide(archer, monster_effect_group, True)
        if wave_hits:
            # 只需從震盪波物件本身獲取傷害值並扣血即可
            archer.blood -= wave_hits[0].damage
            archer.invincible_timer = INVINCIBLE_DURATION

    # --- 繪製所有內容 ---
    screen.blit(lev3_bg, (0, 0))
    # 正確的繪圖方式
    for p in player_group: p.draw(screen) # 呼叫自訂的 draw 方法
    enemy_group.draw(screen)
    player_projectile_group.draw(screen) # 現在箭矢會被畫出來
    monster_projectile_group.draw(screen)
    monster_effect_group.draw(screen)
    
    if monster: monster.draw_health_bar(screen)

    return None