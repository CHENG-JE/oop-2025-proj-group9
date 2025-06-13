# level1/wall.py
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/items/wall.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((cell_size, cell_size))
            self.image.fill((100, 100, 100)) # 如果圖片找不到，用灰色方塊代替
            
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(x, y))