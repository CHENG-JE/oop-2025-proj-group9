# basic_enemy_fighter.py
import pygame
import random

class BasicEnemyFighter(pygame.sprite.Sprite):
    def __init__(self, position, speed=3, hp=30, attack_power=5):
        super().__init__()
        self.image = pygame.image.load("assets/enemy/fighter1.png")
        self.image = pygame.transform.scale(self.image, (100, 100))  # ← 需指定回 self.image
        # self.image.fill((255, 100, 100))  # ← 如果你要圖片而不是純色方塊，應註解這行
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.hp = hp
        self.attack_power = attack_power

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.drop_item()
            self.kill()

    def drop_item(self):
        i = random.random()
        print(f"隨機值: {i}")
        if i < 0.3:  # 30% 機率掉黃色寶物
            item = Item(self.rect.center, color=(255, 255, 0))
            all_items.add(item)
            print("掉落：黃色寶物")
        elif 0.3 <= i < 0.45:  # 15% 機率掉紅色寶物
            red_item = Item(self.rect.center, color=(255, 0, 0))
            all_items.add(red_item)
            print("掉落：紅色寶物")
        else:
            print("無掉落")

# item.py
class Item(pygame.sprite.Sprite):
    def __init__(self, position, color=(255, 255, 0)):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)  # 可設定顏色的寶物
        self.rect = self.image.get_rect(center=position)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()