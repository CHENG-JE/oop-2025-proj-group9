# level3/archer.py
import pygame
from weapon import Arrow
import ui

class Archer(pygame.sprite.Sprite):
    def __init__(self, pos, boundaries):
        super().__init__()
        # 從 player.py 複製過來的屬性
        self.max_blood = 100
        self.blood = 100
        self.exp = 0
        self.money = 0 # 假設從0開始或從主玩家傳入

        # 角色外觀與位置
        self.image = pygame.image.load("assets/player/archer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.original_image_right = self.image
        self.original_image_left = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom=pos)

        # 物理與狀態
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.invincible_timer = 0
        self.attack_cooldown = 0
        
        # 常數
        self.gravity = 0.87
        self.jump_speed = -20.8
        self.move_speed = 7
        self.left_boundary, self.right_boundary = boundaries

    def update(self, keys, platforms, projectile_group):
        # 更新計時器
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 處理物理
        self.apply_gravity_and_collision(platforms)
        
        # 處理輸入
        self.handle_input(keys, projectile_group)

    def apply_gravity_and_collision(self, platforms):
        self.vy += self.gravity
        self.rect.y += self.vy
        
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                self.on_ground = True
                break

    def handle_input(self, keys, projectile_group):
        # 左右移動
        if keys[pygame.K_a] and self.rect.left > self.left_boundary:
            self.rect.x -= self.move_speed
            if self.facing_right:
                self.facing_right = False
                self.image = self.original_image_left
        if keys[pygame.K_d] and self.rect.right < self.right_boundary:
            self.rect.x += self.move_speed
            if not self.facing_right:
                self.facing_right = True
                self.image = self.original_image_right
        
        # 跳躍
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = self.jump_speed
            
        # 攻擊
        if keys[pygame.K_j] and self.attack_cooldown == 0:
            direction = "right" if self.facing_right else "left"
            arrow = Arrow(self.rect.centerx, self.rect.centery, direction, damage=20)
            projectile_group.add(arrow)
            self.attack_cooldown = 30

    def take_damage(self, amount):
        if self.invincible_timer == 0:
            self.blood = max(0, self.blood - amount) # 使用 max() 確保血量不低於 0
            self.invincible_timer = INVINCIBLE_DURATION # INVINCIBLE_DURATION 在 level3_game 中定義，這裡假設為 120
            
    def draw(self, screen):
        # 如果處於無敵狀態，加上半透明效果
        if self.invincible_timer > 0 and self.invincible_timer % 10 < 5: # 閃爍效果
            pass # 不繪製，造成閃爍
        else:
            screen.blit(self.image, self.rect)

        # === 改正：呼叫 ui 模組來繪製狀態 ===
        ui.draw_player_stats(screen, self)