# fast_enemy.py
import pygame
from level2.basic_fighter import BasicEnemyFighter

class SpaceEnemy(BasicEnemyFighter):
    def __init__(self, position):
        super().__init__(position, speed=1, hp=200, attack_power=5)
        self.image = pygame.image.load("assets/enemy/fighter3.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)