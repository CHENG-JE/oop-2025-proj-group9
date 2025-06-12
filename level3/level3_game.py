import pygame
import sys, os
import random
# 確保可以從父目錄導入模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from weapon import Arrow

# === 常數區 ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_SPEED = 7
ATTACK_COOLDOWN = 30
INVINCIBLE_DURATION = 120

# --- 基於物理計算得出的新常數 ---
# 為了達到 0.5 秒跳躍時間和 200 像素跳躍高度，我們需要：
# 重力加速度 a ≈ 6400 pixels/sec²
# 初始跳躍速度 v₀ ≈ -1600 pixels/sec
# 換算成 60 FPS 遊戲迴圈中的值：
GRAVITY = 1.8  # (6400 / 60 / 60)
JUMP_SPEED = -27 # (-1600 / 60)

# --- 新增的環境常數 ---
GROUND_Y = 500  # 地平線的Y座標
LEFT_BOUNDARY = 50   # 左邊界
RIGHT_BOUNDARY = 750 # 右邊界


# === 全域物件 ===
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
effect_group = pygame.sprite.Group()

# === 背景圖片 ===
lev3_map = pygame.image.load("assets/background/level3.jpeg")
lev3_bg = pygame.transform.scale(lev3_map, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        # 讓平台隱形
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/enemy/monster.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y) # 使用 midbottom 精確定位
        self.health = 100
        self.direction = 1
        self.speed = 2
        self.vy = 0

    def update(self, platforms):
        self.vy += GRAVITY
        self.rect.y += self.vy

        on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                on_ground = True
                break
        
        if on_ground:
            self.rect.x += self.speed * self.direction
            # === 改用新的邊界進行判斷 ===
            if self.rect.right > RIGHT_BOUNDARY or self.rect.left < LEFT_BOUNDARY:
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)


def init_level3(player):
    player.current_map = "level3"
    
    # === 更改平台設定：只有一個地平線 ===
    platform_group.empty()
    platform_group.add(Platform(0, GROUND_Y, SCREEN_WIDTH, 20)) # 在 y=500 建立一個寬屏平台

    # === 更改角色和敵人的初始位置 ===
    player.rect.midbottom = (250, GROUND_Y) # 角色初始位置 (250, 500)
    
    enemy_group.empty()
    projectile_group.empty()
    enemy = Enemy(550, GROUND_Y) # 怪物初始位置 (550, 500)
    enemy_group.add(enemy)
    
    # 重置玩家狀態
    player.vy = 0
    player.on_ground = False
    player.facing_right = True
    player.attack_cooldown = 0
    player.invincible_timer = 0


def handle_game_over(screen, player, win):
    # (此函式內容不變，省略以節省篇幅)
    # ...
    font = pygame.font.SysFont(None, 60)
    if win:
        text1 = font.render("You Win!", True, (0, 255, 0))
        text2_str = "You got $300 & 50 EXP"
        player.money += 300
        player.exp = min(player.exp + 50, 1000)
    else:
        text1 = font.render("You Lose!", True, (255, 0, 0))
        text2_str = "You lose $50"
        player.money = max(0, player.money - 50)

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
    
    player.reset_image()
    player.current_map = "game_map"
    player.rect.center = (420, 180)
    player.resize_image((100, 100))
    player.blood = player.max_blood

def update_level3(player, screen):
    # (此函式大部分內容不變，僅修改移動邊界，此處省略部分以節省篇幅)
    # ...
    if player.blood <= 0:
        handle_game_over(screen, player, win=False)
        return
    if not enemy_group:
        handle_game_over(screen, player, win=True)
        return

    screen.blit(lev3_bg, (0, 0))
    
    player.update()
    enemy_group.update(platform_group)
    projectile_group.update()

    player.vy += GRAVITY
    player.rect.y += player.vy
    
    player.on_ground = False
    for platform in platform_group:
        if player.rect.colliderect(platform.rect):
            if player.vy > 0:
                player.rect.bottom = platform.rect.top
                player.vy = 0
                player.on_ground = True
            elif player.vy < 0:
                player.rect.top = platform.rect.bottom
                player.vy = 0
    
    keys = pygame.key.get_pressed()
    original_facing = player.facing_right

    # === 更改玩家的移動邊界 ===
    if keys[pygame.K_a] and player.rect.left > LEFT_BOUNDARY:
        player.rect.x -= MOVE_SPEED
        player.facing_right = False
    if keys[pygame.K_d] and player.rect.right < RIGHT_BOUNDARY:
        player.rect.x += MOVE_SPEED
        player.facing_right = True
    
    if original_facing != player.facing_right:
        player.image = pygame.transform.flip(player.image, True, False)

    if keys[pygame.K_SPACE] and player.on_ground:
        player.vy = JUMP_SPEED
    
    if keys[pygame.K_j] and player.attack_cooldown == 0:
        direction = "right" if player.facing_right else "left"
        arrow = Arrow(player.rect.centerx, player.rect.centery, direction, speed=15, damage=40)
        projectile_group.add(arrow)
        player.attack_cooldown = ATTACK_COOLDOWN # ATTACK_COOLDOWN 的值是 30

    hits = pygame.sprite.groupcollide(projectile_group, enemy_group, True, False)
    for projectile, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.health -= projectile.damage
            if enemy.health <= 0:
                enemy.kill()
                player.exp = min(player.exp + 25, 1000)

    if player.invincible_timer == 0:
        hits = pygame.sprite.spritecollide(player, enemy_group, False)
        if hits:
            player.blood -= 20
            player.invincible_timer = INVINCIBLE_DURATION

    platform_group.draw(screen)
    enemy_group.draw(screen)
    projectile_group.draw(screen)
    player.draw(screen)
    
    font = pygame.font.SysFont(None, 28)
    enemy_text = font.render(f"Enemies left: {len(enemy_group)}", True, (255, 255, 0))
    screen.blit(enemy_text, (SCREEN_WIDTH - 150, 20))