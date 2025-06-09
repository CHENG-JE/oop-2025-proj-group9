# laser.py
import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="up", speed=10, color=(255, 0, 0, 180), width=5, height=30, damage=50):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # 如果飛出畫面就自動刪除
        if (self.rect.right < 0 or self.rect.left > 800 or 
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()