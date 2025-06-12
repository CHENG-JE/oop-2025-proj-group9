import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="up", speed=10, color=(255, 0, 0, 180), width=5, height=30, damage=50):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # 如果飛出畫面就自動刪除
        if (self.rect.right < 0 or self.rect.left > 800 or 
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=15, damage=40):
        super().__init__()
        # 載入圖片
        self.image = pygame.image.load("assets/weapon/arrow.png").convert_alpha()
        # 調整圖片大小
        self.image = pygame.transform.scale(self.image, (40, 10))
        
        self.direction = direction
        self.speed = speed
        self.damage = damage
        
        # 根據方向翻轉圖片
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False) # True 代表水平翻轉, False 代表不垂直翻轉
        
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # 移動邏輯和 Laser 一樣
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        
        # 如果飛出畫面就自動刪除
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()