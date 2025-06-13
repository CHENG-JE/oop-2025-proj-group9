# level1/droplet.py
import pygame
import math

class Droplet(pygame.sprite.Sprite):
    def __init__(self, start_pos, cell_size):
        super().__init__()
        # 繼承主玩家的屬性
        self.max_blood = 100
        self.blood = 100
        self.exp = 0
        self.money = 0
        
        # 視覺圖像 (可以旋轉)
        self.original_image = pygame.image.load("assets/player/droplet.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (34, 17))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
        
        # === 新增：物理碰撞框 (Hitbox) ===
        # Hitbox 的尺寸是固定的，比視覺圖像略小，且不會旋轉
        hitbox_size = (16, 16) 
        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = self.rect.center

        # 位置與移動 (使用向量來處理精確位置)
        self.pos = pygame.math.Vector2(start_pos)
        self.speed = 3

    def update(self, keys, walls):
        # 處理輸入並獲取移動向量
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y = -1
        if keys[pygame.K_s]: move_vector.y = 1
        if keys[pygame.K_a]: move_vector.x = -1
        if keys[pygame.K_d]: move_vector.x = 1

        if move_vector.length_squared() > 0:
            move_vector.normalize_ip()

            # --- 只旋轉視覺圖像 ---
            angle = move_vector.angle_to(pygame.math.Vector2(0, -1))
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.hitbox.center) # 視覺圖像的中心永遠對齊 Hitbox 的中心
            
            # --- 移動與碰撞改為基於 Hitbox ---
            self.move_and_collide(move_vector, walls)

    def move_and_collide(self, move_vector, walls):
        # --- 使用 Hitbox 進行所有移動和碰撞計算 ---
        
        # X 軸移動
        self.pos.x += move_vector.x * self.speed
        self.hitbox.centerx = round(self.pos.x)
        # X 軸碰撞
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if move_vector.x > 0: # 向右移動
                    self.hitbox.right = wall.rect.left
                elif move_vector.x < 0: # 向左移動
                    self.hitbox.left = wall.rect.right
                self.pos.x = self.hitbox.centerx # 碰撞後，校正浮點數位置

        # Y 軸移動
        self.pos.y += move_vector.y * self.speed
        self.hitbox.centery = round(self.pos.y)
        # Y 軸碰撞
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if move_vector.y > 0: # 向下移動
                    self.hitbox.bottom = wall.rect.top
                elif move_vector.y < 0: # 向上移動
                    self.hitbox.top = wall.rect.bottom
                self.pos.y = self.hitbox.centery
        
        # --- 最後，讓視覺圖像的中心跟隨 Hitbox 的中心 ---
        self.rect.center = self.hitbox.center
            
    def take_damage(self, amount):
        self.blood = max(0, self.blood - amount)
        
    def draw_ui(self, screen):
        font = pygame.font.SysFont(None, 28)
        money_text = font.render(f"Money: ${self.money}", True, (255, 255, 0))
        hp_text = font.render(f"HP: {int(self.blood)}/{self.max_blood}", True, (0, 255, 0))
        exp_text = font.render(f"EXP: {self.exp}", True, (0, 255, 255))
        screen.blit(money_text, (20, 20))
        screen.blit(hp_text, (20, 45))
        screen.blit(exp_text, (20, 70))