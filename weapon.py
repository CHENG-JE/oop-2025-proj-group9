# weapon.py
import pygame
import math

class Laser(pygame.sprite.Sprite):
    # ... (Laser 類別不變)
    def __init__(self, x, y, direction="up", speed=10, color=(255, 0, 0, 180), width=5, height=30, damage=50):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage
    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed
        if (self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

class Arrow(pygame.sprite.Sprite):
    # ... (Arrow 類別不變)
    def __init__(self, x, y, direction, speed=15, damage=20):
        super().__init__()
        self.image = pygame.image.load("assets/weapon/arrow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.direction = direction
        self.speed = speed
        self.damage = damage
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()

class MonsterBeam(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/weapon/beam.gif").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((30, 10))
            self.image.fill((255, 100, 255))
            
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect(center=start_pos)
        
        angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        arrow_speed = 15
        self.speed = arrow_speed * 0.5
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 讓這個類別更獨立，不依賴外部的 screen 變數
        if (self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, center_pos, width):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/weapon/shockwave.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((width, 30))
            self.image.fill((100, 100, 255))
        
        self.image = pygame.transform.scale(self.image, (width, self.image.get_height()))
        self.rect = self.image.get_rect(center=center_pos)
        self.lifetime = 30
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()