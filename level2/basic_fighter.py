# level2/basic_fighter.py (修正版)
import pygame
import random

# 我們將 Item 也移到這裡，因為它和掉落物邏輯緊密相關
class Item(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # 只有經驗值道具
        self.item_type = 'exp'
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # 只使用黃色：經驗值
        self.rect = self.image.get_rect(center=position)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


class BasicEnemyFighter(pygame.sprite.Sprite):
    def __init__(self, position, speed=3, health=100, attack_power=10): # === 修正: hp -> health ===
        super().__init__()
        self.image = pygame.image.load("assets/enemy/fighter1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.health = health  # === 修正: self.hp -> self.health ===
        self.attack_power = attack_power
        self.shoot_timer = 0 # 每個敵人都應該有自己的射擊計時器

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage # === 修正: self.hp -> self.health ===
        if self.health <= 0: # === 修正: self.hp -> self.health ===
            self.kill() # kill() 會自動將 Sprite 從所有 Group 中移除

    # drop_item 邏輯已經整合進 level2_game.py，這裡可以移除以簡化基礎類別