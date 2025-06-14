# weapon.py
import pygame
import math

class Laser(pygame.sprite.Sprite):
    # ... (Laser 類別不變)
    def __init__(self, x, y, direction="up", speed=10, color=(255, 0, 0, 180), width=5, height=30, damage=50):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage
    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed
        if (self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

class Arrow(pygame.sprite.Sprite):
    # ... (Arrow 類別不變)
    def __init__(self, x, y, direction, speed=15, damage=20):
        super().__init__()
        self.image = pygame.image.load("assets/weapon/arrow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.direction = direction
        self.speed = speed
        self.damage = damage
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()

class MonsterBeam(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        
        # 1. 載入原始圖片並儲存，以備旋轉使用
        try:
            self.original_image = pygame.image.load("assets/weapon/beam.gif").convert_alpha()
        except pygame.error:
            self.original_image = pygame.Surface((50, 20), pygame.SRCALPHA)
            self.original_image.fill((255, 100, 255))
        
        self.original_image = pygame.transform.scale(self.original_image, (50, 20))
        
        # 2. 計算射擊角度
        # math.atan2 會回傳從 start_pos 指向 target_pos 的向量與X軸正向的夾角(弧度)
        angle_rad = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        # 將弧度轉換為角度
        angle_deg = math.degrees(angle_rad)
        
        # 3. 旋轉圖片以對準目標
        # Pygame 的 rotate 是逆時針旋轉。我們的圖預設朝左(180度)，所以需要公式 `180 - angle` 來校正
        self.image = pygame.transform.rotate(self.original_image, 180 - angle_deg)
        
        self.rect = self.image.get_rect(center=start_pos)
        
        # 4. 根據角度計算移動向量 (恢復追蹤彈邏輯)
        arrow_speed = 15
        speed = arrow_speed * 0.7
        self.vx = math.cos(angle_rad) * speed
        self.vy = math.sin(angle_rad) * speed

    def update(self):
        # 根據計算好的向量移動
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # 飛出畫面就自動刪除
        if not (0 <= self.rect.centerx <= 800 and 0 <= self.rect.centery <= 600):
            self.kill()
        
        angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        arrow_speed = 15
        self.speed = arrow_speed * 0.5
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 讓這個類別更獨立，不依賴外部的 screen 變數
        if (self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

class Shockwave(pygame.sprite.Sprite):
    # === 改正：__init__ 方法新增 lifetime 參數 ===
    def __init__(self, center_pos, width, damage, stage, lifetime=60): # 預設持續 1 秒
        super().__init__()
        try:
            self.image = pygame.image.load("assets/weapon/shockwave.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((width, 30)); self.image.fill((100, 100, 255))
        
        original_aspect_ratio = self.image.get_height() / self.image.get_width()
        new_height = int(width * original_aspect_ratio)
        self.image = pygame.transform.scale(self.image, (width, new_height))
        
        self.rect = self.image.get_rect(center=center_pos)
        self.lifetime = lifetime # 使用傳入的持續時間
        
        self.damage = damage
        self.stage = stage
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()