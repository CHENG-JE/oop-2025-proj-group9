# level3/level3_game.py
import pygame
import sys, os

# 確保可以從父目錄導入模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 從新檔案中導入類別
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
    archer.max_blood = main_player.max_blood
    archer.blood = main_player.blood
    player_group.add(archer)
    all_sprites.add(archer)
    
    # 建立怪物
    global monster
    monster = Monster(pos=(550, GROUND_Y), boundaries=BOUNDARIES)
    enemy_group.add(monster)
    all_sprites.add(monster)

def handle_game_over(screen, main_player, win):
    # (此函式邏輯不變，但注意它現在接收主玩家 main_player)
    font = pygame.font.SysFont(None, 60)
    if win:
        text1 = font.render("You Win!", True, (0, 255, 0))
        text2_str = "You got $300 & 50 EXP"
        main_player.money += 300
        main_player.exp = min(main_player.exp + 50, 1000)
    else:
        text1 = font.render("You Lose!", True, (255, 0, 0))
        text2_str = "You lose $50"
        main_player.money = max(0, main_player.money - 50)

    # ... (後續等待畫面邏輯不變)
    text2 = pygame.font.SysFont(None, 40).render(text2_str, True, (255, 255, 255))
    text3 = pygame.font.SysFont(None, 30).render("Press any key to return to map...", True, (255, 255, 255))
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2 - 60))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2))
    screen.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, SCREEN_HEIGHT//2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
    
    main_player.reset_image()
    main_player.current_map = "game_map"
    main_player.rect.center = (420, 180)
    main_player.resize_image((100, 100))
    main_player.blood = archer.blood # 返回時繼承血量

def update_level3(screen, main_player):
    # 遊戲結束判斷
    if archer.blood <= 0:
        handle_game_over(screen, main_player, win=False)
        return
    if not enemy_group:
        handle_game_over(screen, main_player, win=True)
        return

    # 更新物件
    keys = pygame.key.get_pressed()
    archer.update(keys, platform_group, player_projectile_group)
    monster.update(platform_group, archer, monster_projectile_group, monster_effect_group)
    monster_projectile_group.update()
    monster_effect_group.update()

    # 碰撞檢測
    # 1. 玩家的箭矢 vs 敵人
    hits = pygame.sprite.groupcollide(player_projectile_group, enemy_group, True, False)
    for projectile, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.health -= projectile.damage
            if enemy.health <= 0:
                enemy.kill()
                archer.exp += 25

    # 2. 玩家 vs 怪物攻擊 (無敵幀判斷)
    if archer.invincible_timer == 0:
        # 2a. 玩家 vs 光波
        beam_hits = pygame.sprite.spritecollide(archer, monster_projectile_group, True)
        if beam_hits:
            archer.blood -= 50
            archer.invincible_timer = INVINCIBLE_DURATION
        
        # 2b. 玩家 vs 震盪波
        wave_hits = pygame.sprite.spritecollide(archer, monster_effect_group, False)
        if wave_hits:
            wave = wave_hits[0]
            if hasattr(wave, 'damage') and wave.damage == 80:
                archer.blood -= 80
            else:
                archer.blood -= 50
                if monster:
                    monster.target_pos = archer.rect.center
                    monster.state = 'moving_to_target'
            archer.invincible_timer = INVINCIBLE_DURATION
            wave.kill()

    # 繪製所有內容
    screen.blit(lev3_bg, (0, 0))
    player_group.draw(screen)
    enemy_group.draw(screen)
    player_projectile_group.draw(screen)
    monster_projectile_group.draw(screen)
    monster_effect_group.draw(screen)
    
    # 繪製UI
    if monster:
        monster.draw_health_bar(screen)
    # (可以再增加繪製玩家血條的UI)