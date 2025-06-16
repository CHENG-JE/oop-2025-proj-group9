# level2/spaceship_fighter.py (修正版)
import pygame
from level2.basic_fighter import BasicEnemyFighter

class SpaceEnemy(BasicEnemyFighter):
    def __init__(self, position):
        # === 修正：將 hp=200 改為 health=200 ===
        super().__init__(position, speed=1, health=200, attack_power=5)
        self.image = pygame.image.load("assets/enemy/fighter3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)