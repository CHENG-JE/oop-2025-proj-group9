# level3/monster.py
import pygame
import random
import math
from weapon import MonsterBeam, Shockwave

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, boundaries):
        super().__init__()
        self.image = pygame.image.load("assets/enemy/monster.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.image, (200, 200))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(midbottom=pos)
        self.max_health = 1000
        self.health = self.max_health
        self.vy = 0
        self.state = 'idle'
        self.attack_timer = 120
        self.shockwave_timer = 0
        self.target_pos = None
        self.gravity = 2.2
        self.move_speed = 10 # 600 pixels/sec @ 60 FPS
        self.left_boundary, self.right_boundary = boundaries

    def update(self, platforms, player, monster_projectile_group, monster_effect_group):
        # Y軸物理模擬
        self.vy += self.gravity
        self.rect.y += self.vy
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0: self.rect.bottom = platform.rect.top; self.vy = 0; break
        
        # 狀態機 AI
        if self.state == 'idle':
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                if random.random() < 0.8: # 光波攻擊
                    beam = MonsterBeam(self.rect.center, player.rect.center)
                    monster_projectile_group.add(beam)
                    self.attack_timer = 42 # 0.7秒後再一發
                else: # 震地攻擊
                    self.state = 'shockwave_stage1'
                    wave = Shockwave(self.rect.midbottom, self.rect.width, damage=30, stage=1)
                    monster_effect_group.add(wave)
                    self.shockwave_timer = 60 # 震波持續1秒
        
        elif self.state == 'shockwave_stage1':
            self.shockwave_timer -= 1
            if self.shockwave_timer <= 0:
                self.state = 'idle'
                self.attack_timer = 120

        elif self.state == 'moving_to_target':
            if self.target_pos:
                dx = self.target_pos[0] - self.rect.centerx
                if abs(dx) < self.move_speed:
                    self.rect.centerx = self.target_pos[0]
                    self.state = 'shockwave_stage2'
                    wave = Shockwave(self.rect.midbottom, self.rect.width, damage=50, stage=2)
                    monster_effect_group.add(wave)
                    self.shockwave_timer = 60
                else:
                    direction = 1 if dx > 0 else -1
                    self.rect.x += self.move_speed * direction
                    if self.rect.left < self.left_boundary: self.rect.left = self.left_boundary
                    if self.rect.right > self.right_boundary: self.rect.right = self.right_boundary
        
        elif self.state == 'shockwave_stage2':
            self.shockwave_timer -= 1
            if self.shockwave_timer <= 0:
                self.state = 'idle'
                self.attack_timer = 120
            
    def draw_health_bar(self, screen):
        bar_x, bar_y, bar_width, bar_height = 250, 80, 450, 20
        health_percent = max(0, self.health / self.max_health)
        current_bar_width = bar_width * health_percent
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))
        try:
            font_path = "assets/fonts/Cinzel-Regular.ttf"
            title_font = pygame.font.Font(font_path, 29)
        except FileNotFoundError:
            title_font = pygame.font.SysFont(None, 30)
        title_font.bold = True; title_font.italic = True
        title_text = "Primordial bathysmal vishap"; title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(bottomleft=(bar_x, bar_y - 5)); screen.blit(title_surface, title_rect)