# weapon.py (最終修正版)
import pygame
import math

class Projectile(pygame.sprite.Sprite):
    """
    所有武器（投射物）的基礎類別
    """
    def __init__(self, image, center_pos, damage=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.damage = damage

    def update(self):
        # 共通的邊界檢查，如果投射物飛出畫面，則自動銷毀
        if self.rect.bottom < 0 or self.rect.top > 600 or \
           self.rect.right < 0 or self.rect.left > 800:
            self.kill()


class Laser(Projectile):
    """
    玩家和基本敵機發射的雷射光束。
    """
    def __init__(self, x, y, direction="up", speed=10, color=(255, 0, 0, 180), width=5, height=30, damage=50):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(image, color, (0, 0, width, height))
        super().__init__(image, center_pos=(x, y), damage=damage)
        self.direction = direction
        self.speed = speed

    def update(self):
        if self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed
        super().update()


class Arrow(Projectile):
    """
    Level 3 玩家發射的弓箭。
    """
    def __init__(self, x, y, direction, speed=15, damage=20):
        image = pygame.image.load("assets/weapon/arrow.png").convert_alpha()
        image = pygame.transform.scale(image, (100, 100))
        if direction == "left":
            image = pygame.transform.flip(image, True, False)
        super().__init__(image, center_pos=(x, y), damage=damage)
        self.direction = direction
        self.speed = speed

    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        super().update()


class MonsterBeam(Projectile):
    """
    Level 3 BOSS 發射的追蹤光束，傷害固定為 50。
    """
    def __init__(self, start_pos, target_pos):
        # 準備光束圖片和角度
        try:
            original_image = pygame.image.load("assets/weapon/beam.gif").convert_alpha()
        except pygame.error:
            original_image = pygame.Surface((50, 20), pygame.SRCALPHA)
            original_image.fill((255, 100, 255))
        
        original_image = pygame.transform.scale(original_image, (50, 20))
        
        angle_rad = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        angle_deg = math.degrees(angle_rad)
        image = pygame.transform.rotate(original_image, 180 - angle_deg)
        
        # === 修正：呼叫父類別時，將 damage 寫死為 50 ===
        super().__init__(image, center_pos=start_pos, damage=50)

        # MonsterBeam 特有的移動屬性
        speed = 10.5
        self.vx = math.cos(angle_rad) * speed
        self.vy = math.sin(angle_rad) * speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        super().update()


class Shockwave(Projectile):
    """
    Level 3 BOSS 發射的震盪波。
    """
    def __init__(self, center_pos, width, damage, stage, lifetime=60):
        # 準備震盪波圖片
        try:
            image = pygame.image.load("assets/weapon/shockwave.png").convert_alpha()
        except pygame.error:
            image = pygame.Surface((width, 30))
            image.fill((100, 100, 255))
        
        original_aspect_ratio = image.get_height() / image.get_width()
        new_height = int(width * original_aspect_ratio)
        image = pygame.transform.scale(image, (width, new_height))
        
        super().__init__(image, center_pos=center_pos, damage=damage)
        
        self.lifetime = lifetime
        self.stage = stage
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()