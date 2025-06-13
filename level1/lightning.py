# level1/lightning.py
import pygame

class Lightning(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/items/lightning.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0, 180), (30, 30), 30)

        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=center_pos)
        self.lifetime = 60 # 持續 1 秒 (60 幀)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()