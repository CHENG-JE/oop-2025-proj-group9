# level1/portal.py
import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/items/portal.png").convert_alpha()
        except pygame.error:
            # 將備用圖片也改成 30x30
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 255)) 

        # === 改正：將尺寸從 cell_size 改為固定的 (30, 30) ===
        self.image = pygame.transform.scale(self.image, (30, 30))
            
        # self.rect 會根據上面縮放後的 image 自動調整大小
        self.rect = self.image.get_rect(topleft=(x, y))