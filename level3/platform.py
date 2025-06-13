# level3/platform.py
import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        # 讓平台隱形，只做碰撞用
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(x=x, y=y)