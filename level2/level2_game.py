import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import random
from level2.basic_fighter import BasicEnemyFighter, Item
from weapon import Laser
#from basic_fighter import BasicEnemyFighter
#from basic_fighter import Item


# === 常數區 ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHOOT_COOLDOWN = 15
ENEMY_SPAWN_RATE = 100  # 平均每 100 frame 出現一台敵機
DROP_CHANCE = 0.5

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
    player.current_map = "level2"
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    player.shoot_timer = 0
    player.kills = 0
    enemy_group.empty()
    laser_group.empty()
    all_items.empty()

# === 更新 level2 每幀邏輯 ===
def update_level2(player, screen):
    # --- 畫背景 ---
    screen.fill((0, 0, 0))  # 或繪製 level2 的背景圖，如 screen.blit(level2_bg, (0, 0))
    screen.blit(lev2_bg, (0, 0))

    # --- 玩家鍵盤輸入與更新 ---
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update()

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

    # --- 生成敵機 --
    if player.kills <= 10:
        spawn_rate = ENEMY_SPAWN_RATE
    elif player.kills <=20:
        spawn_rate = ENEMY_SPAWN_RATE * 2
    else :
        spawn_rate = ENEMY_SPAWN_RATE * 1

    if random.randint(1, spawn_rate) == 1:
        x = random.randint(50, SCREEN_WIDTH - 50)
        if 20 >= player.kills > 10:
            from level2.fast_fighter import FastEnemy
            enemy = FastEnemy((x, -40))
            enemy.health = 50
        elif player.kills > 20:
            from level2.spaceship_fighter import SpaceEnemy
            enemy = SpaceEnemy((x, -40))
            enemy.health = 200
        else:
            enemy = BasicEnemyFighter((x, -40))
            enemy.health = 100
        enemy_group.add(enemy)

    # --- 更新所有物件 ---
    laser_group.update()
    enemy_group.update()

    # --- 敵機隨機射擊（帶冷卻限制） ---
    for enemy in enemy_group:
        if not hasattr(enemy, 'shoot_timer'):
            enemy.shoot_timer = 0
        enemy.shoot_timer += 1
        if enemy.shoot_timer >= 60 and random.randint(1, 90) == 1:
            if 20 > player.kills >=10: 
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 5, (255,255,255,180), 5, 30, 20)
            elif player.kills >=20:
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 1.5, (255,255,255,180), 5, 30, 5)
            else:
                laser = Laser(enemy.rect.centerx, enemy.rect.bottom, "down", 2, (255,255,255,180), 5, 30, 10)
            enemy_lasers.add(laser)
            enemy.shoot_timer = 0
    enemy_lasers.update()
    all_items.update()

    # --- 敵機出界移除 ---
    for enemy in enemy_group:
        if enemy.rect.top > SCREEN_HEIGHT:
            enemy.kill()

    # --- 敵機到達指定位置造成傷害 ---
    for enemy in enemy_group:
        if enemy.rect.centery >= 600:
            if player.kills >= 20:
                player.blood -= 3 
            elif player.kills >= 10:
                player.blood -= 10
            elif player.kills > 0:
                player.blood -= 5
            enemy.kill()
            if player.blood <= 0:
                print("Player defeated")
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 48)
                line1 = font.render(f"You were defeated. Total kills: {player.kills}", True, (255, 0, 0))
                line2 = font.render("Press L to leave!", True, (255, 0, 0))

                # 顯示兩行文字，第二行往下偏移約 50 px
                screen.blit(line1, (SCREEN_WIDTH // 2 - line1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
                screen.blit(line2, (SCREEN_WIDTH // 2 - line2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            player.reset_image()
                            player.current_map = "game_map"
                            player.rect.center = (460, 170)
                            player.resize_image((100, 100))
                            player.blood = 100
                            player.exp = 0
                            player.kills = 0
                            waiting = False
                            return

    # --- 繪製所有物件 ---
    player.draw(screen)
    laser_group.draw(screen)
    enemy_group.draw(screen)
    enemy_lasers.draw(screen)
    all_items.draw(screen)

    # --- 子彈與敵機碰撞處理 ---
    for laser in laser_group:
        hits = pygame.sprite.spritecollide(laser, enemy_group, False)
        if hits:
            laser.kill()
            enemy = hits[0]
            # enemy.take_damage(laser.damage)  # 暫時註解，直接減血
            enemy.health -= laser.damage  # 直接減血，避免 take_damage() 做出額外操作
            if enemy.health <= 0:
                enemy.kill()
                player.kills += 1
                if player.kills % 10 == 0:
                    player.blood = min(player.blood + 20, 100)
                if random.random() < DROP_CHANCE:
                    # 確保 Item 類別已正確導入，若未導入請加上 import
                    item = Item(enemy.rect.center)
                    all_items.add(item)
                    # 檢測寶物顏色
                    color = item.image.get_at((0, 0))[:3]
                    if color == (255, 255, 0):
                        print("掉落黃色寶物")
                    elif color == (255, 0, 0):
                        print("掉落紅色寶物")
                    else:
                        print("掉落未知顏色寶物:", color)

    # --- 玩家被敵機子彈打中時的碰撞判斷與扣血 ---
    hits = pygame.sprite.spritecollide(player, enemy_lasers, True) or pygame.sprite.spritecollide(player, enemy_group, True)
    for hit in hits:
        player.blood -= 10
        if player.blood <= 0:
            print("Player defeated")
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 48)
            line1 = font.render(f"You were defeated. Total kills: {player.kills}", True, (255, 0, 0))
            line2 = font.render("Press L to leave!", True, (255, 0, 0))

            # 顯示兩行文字，第二行往下偏移約 50 px
            screen.blit(line1, (SCREEN_WIDTH // 2 - line1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(line2, (SCREEN_WIDTH // 2 - line2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        player.reset_image()
                        player.current_map = "game_map"
                        player.rect.center = (460, 170)  # 設定指定位置
                        player.resize_image((100, 100))  # 根據需要重新縮放圖片
                        player.blood = 100
                        player.exp = 0
                        player.kills = 0
                        waiting = False
                        return
    
    if player.kills == 40 :
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        line1 = font.render(f"Victory! Total kills: {player.kills}", True, (255, 0, 0))
        line2 = font.render("Press L to leave!", True, (255, 0, 0))

        # 顯示兩行文字，第二行往下偏移約 50 px
        screen.blit(line1, (SCREEN_WIDTH // 2 - line1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(line2, (SCREEN_WIDTH // 2 - line2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    player.reset_image()
                    player.current_map = "game_map"
                    player.rect.center = (460, 170)  # 設定指定位置
                    player.resize_image((100, 100))  # 根據需要重新縮放圖片
                    player.blood = player.blood
                    player.exp += 100
                    player.money += 1000
                    player.kills = 0
                    waiting = False
                    return


    # --- 撿寶物處理 ---
    pickups = pygame.sprite.spritecollide(player, all_items, True)
    for item in pickups:
        if item.image.get_at((0, 0))[:3] == (255, 255, 0):  # 黃色：加經驗值
            player.exp += 10
        elif item.image.get_at((0, 0))[:3] == (255, 0, 0):  # 紅色：回血
            player.blood = min(player.blood + 20, 100)


    font = pygame.font.SysFont(None, 28)
    kill_text = font.render(f"Kills: {player.kills}", True, (255, 255, 0))
    screen.blit(kill_text, (SCREEN_WIDTH - 120, 20))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    from player import Player  # 假設 player.py 中定義 Player 類
    player = Player("assets/player/fighter.png", (400, 500), (100, 100))
    init_level2(player)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_level2(player, screen)
        pygame.display.flip()
        clock.tick(60)