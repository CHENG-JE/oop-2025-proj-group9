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
        
        # 圖像與旋轉
        self.original_image = pygame.image.load("assets/player/droplet.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (cell_size, cell_size))
        self.image = self.original_image
        
        # 位置與移動
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos) # 使用向量來處理精確位置
        self.speed = 3 # 180 像素/秒

    def update(self, keys, walls):
        # 處理輸入並獲取移動向量
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y = -1
        if keys[pygame.K_s]: move_vector.y = 1
        if keys[pygame.K_a]: move_vector.x = -1
        if keys[pygame.K_d]: move_vector.x = 1

        # 如果有移動，才進行旋轉和位置更新
        if move_vector.length_squared() > 0:
            move_vector.normalize_ip() # 將向量長度設為1，確保斜向移動不會比較快

            # 旋轉圖像
            # atan2 的參數是 (y, x)，回傳弧度。我們轉換為角度
            # Pygame 的角度是逆時針為正，且 0 度朝右。我們的圖朝上，所以要減 90 度
            angle = move_vector.angle_to(pygame.math.Vector2(0, -1))
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # 移動並處理碰撞
            self.move_and_collide(move_vector, walls)

    def move_and_collide(self, move_vector, walls):
        # 分別處理 X 和 Y 軸的移動與碰撞
        # X 軸
        self.pos.x += move_vector.x * self.speed
        self.rect.centerx = round(self.pos.x)
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if move_vector.x > 0: # 向右移動
                self.rect.right = wall.rect.left
            elif move_vector.x < 0: # 向左移動
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.centerx

        # Y 軸
        self.pos.y += move_vector.y * self.speed
        self.rect.centery = round(self.pos.y)
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if move_vector.y > 0: # 向下移動
                self.rect.bottom = wall.rect.top
            elif move_vector.y < 0: # 向上移動
                self.rect.top = wall.rect.bottom
            self.pos.y = self.rect.centery
            
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