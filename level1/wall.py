# level1/wall.py
import pygame

class BaseWall(pygame.sprite.Sprite):
    """牆壁的基礎類別，用於載入圖片"""
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/items/wall.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((1, 1)) # 備用
            self.image.fill((100, 100, 100))

class HorizontalWall(BaseWall):
    """水平的牆壁"""
    def __init__(self, x, y, cell_size):
        super().__init__()
        # 設定尺寸為 (18, 3)
        self.image = pygame.transform.scale(self.image, (18, 3))
        # 將牆壁放在格線的中央
        self.rect = self.image.get_rect(topleft=(x + (cell_size - 18) / 2, y - 1))

class VerticalWall(BaseWall):
    """垂直的牆壁"""
    def __init__(self, x, y, cell_size):
        super().__init__()
        # 先縮放再旋轉
        scaled_image = pygame.transform.scale(self.image, (18, 3))
        self.image = pygame.transform.rotate(scaled_image, 90) # 旋轉90度
        # 將牆壁放在格線的中央
        self.rect = self.image.get_rect(topleft=(x - 1, y + (cell_size - 18) / 2))