# level2/fast_fighter.py (修正版)
import pygame
from level2.basic_fighter import BasicEnemyFighter

class FastEnemy(BasicEnemyFighter):
    def __init__(self, position):
        # === 修正：將 hp=50 改為 health=50 ===
        super().__init__(position, speed=5, health=50, attack_power=20)
        self.image = pygame.image.load("assets/enemy/fighter2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)