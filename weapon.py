import pygame

class Laser:#雷射槍
    def __init__(self, x, y, direction="right", speed=10, color=(255, 0, 0, 180), width=30, height=5, damage=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
        self.damage = damage
        self.alive = True  # 超出邊界就設為 False
        
    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # 檢查是否出界，超出就標記為消失
        if self.x < -self.width or self.x > 800 or self.y < -self.height or self.y > 600:
            self.alive = False

    def draw(self, screen):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.width, self.height))
        screen.blit(surf, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)