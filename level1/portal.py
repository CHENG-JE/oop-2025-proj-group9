# level1/portal.py
import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/items/portal.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((cell_size, cell_size))
            self.image.fill((0, 255, 255)) # 如果圖片找不到，用青色方塊代替

        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=(x, y))