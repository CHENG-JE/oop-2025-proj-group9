import pygame
import sys, os
import random
# 確保可以從父目錄導入模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from weapon import Arrow

# === 常數區 ===
# ... (常數區不變，省略)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_SPEED = 7
ATTACK_COOLDOWN = 30
INVINCIBLE_DURATION = 120
GRAVITY = 2.2
JUMP_SPEED = -33.3
GROUND_Y = 500
LEFT_BOUNDARY = 50
RIGHT_BOUNDARY = 750


# === 全域物件 ===
# ... (不變，省略)
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
effect_group = pygame.sprite.Group()


# === 背景圖片 ===
lev3_map = pygame.image.load("assets/background/level3.jpeg")
lev3_bg = pygame.transform.scale(lev3_map, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Platform(pygame.sprite.Sprite):
    # ... (Platform 類別不變，省略)
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/enemy/monster.png")
        self.image = pygame.transform.scale(self.image, (200, 200)) # 假設怪物大小為 200x200
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        
        # === 改正 1：新增 max_health 屬性 ===
        self.max_health = 1000
        self.health = self.max_health
        
        self.direction = 1
        self.speed = 2
        self.vy = 0

    def update(self, platforms):
        # ... (update 方法不變，省略)
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
            if self.rect.right > RIGHT_BOUNDARY or self.rect.left < LEFT_BOUNDARY:
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)


def init_level3(player):
    # ... (init_level3 方法不變，省略)
    player.current_map = "level3"
    
    platform_group.empty()
    platform_group.add(Platform(0, GROUND_Y, SCREEN_WIDTH, 20))

    player.rect.midbottom = (250, GROUND_Y)
    
    enemy_group.empty()
    projectile_group.empty()
    enemy = Enemy(550, GROUND_Y)
    enemy_group.add(enemy)
    
    player.vy = 0
    player.on_ground = False
    player.facing_right = True
    player.attack_cooldown = 0
    player.invincible_timer = 0


def handle_game_over(screen, player, win):
    # ... (handle_game_over 方法不變，省略)
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

# === 改正 2：修改 update_level3 函式 ===
def update_level3(player, screen):
    # (前面邏輯不變，省略)
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
        arrow = Arrow(player.rect.centerx, player.rect.centery, direction)
        projectile_group.add(arrow)
        player.attack_cooldown = ATTACK_COOLDOWN

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
    
    # --- 繪圖區 ---
    platform_group.draw(screen)
    enemy_group.draw(screen)
    projectile_group.draw(screen)
    player.draw(screen)
    
    font = pygame.font.SysFont(None, 28)
    enemy_text = font.render(f"Enemies left: {len(enemy_group)}", True, (255, 255, 0))
    screen.blit(enemy_text, (SCREEN_WIDTH - 150, 20))

    # --- 新增：繪製怪物血條 ---
    # 只有在場上有怪物時才繪製血條
    if enemy_group:
        # 獲取唯一的怪物實例
        monster = enemy_group.sprites()[0]
        
        # 血條位置和尺寸
        bar_x = 250
        bar_y = 80
        bar_width = 450
        bar_height = 20
        
        # 計算血量百分比和當前血條寬度
        health_percent = monster.health / monster.max_health
        current_bar_width = bar_width * health_percent
        
        # 繪製血條背景 (紅色)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # 繪製當前血量 (綠色)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))
        
        # --- 新增：繪製怪物血條標題 ---
        try:
            font_path = "assets/fonts/Cinzel-Regular.ttf"
            # === 改正 1：放大字體大小 ===
            # 原來大小是 22，放大 1.3 倍 (22 * 1.3 ≈ 29)
            title_font = pygame.font.Font(font_path, 29)
        except FileNotFoundError:
            print(f"警告：找不到字體檔案 {font_path}，將使用預設字體。")
            # 同步放大備用字體
            title_font = pygame.font.SysFont(None, 30)
            
        title_font.bold = True
        title_font.italic = True
            
        title_text = "Primordial bathysmal vishap"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        
        title_rect = title_surface.get_rect()
        # === 改正 2：上移 Y 座標 ===
        # 將 y 座標減 5，讓文字向上移動 5 像素
        title_rect.bottomleft = (bar_x, bar_y - 5) 
        screen.blit(title_surface, title_rect)