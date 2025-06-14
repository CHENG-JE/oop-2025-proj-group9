# level3/monster.py
import pygame
import random
import math
from weapon import MonsterBeam, Shockwave

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, boundaries):
        super().__init__()
        original_image_loaded = pygame.image.load("assets/enemy/monster.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image_loaded, (200, 200))
        self.image_left = scaled_image
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect(midbottom=pos)
        self.max_health = 1000
        self.health = self.max_health
        self.vy = 0
        self.state = 'idle'
        self.attack_cooldown = 120
        self.target_pos = None
        self.gravity = 2.2
        self.move_speed = 15
        self.left_boundary, self.right_boundary = boundaries
        self.jump_gravity = 0.68
        self.jump_speed = -18.5


    def update(self, platforms, player, monster_projectile_group, monster_effect_group):
        if self.state not in ['jumping_up', 'falling_down']:
            self.vy += self.gravity
            self.rect.y += self.vy
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.vy > 0:
                    self.rect.bottom = platform.rect.top; self.vy = 0; break
        
        # 狀態機 AI
        if self.state == 'idle':
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                if random.random() < 0.8:
                    beam = MonsterBeam(self.rect.center, player.rect.center)
                    monster_projectile_group.add(beam)
                    self.attack_cooldown = 42
                else:
                    self.state = 'moving_to_target'

        elif self.state == 'moving_to_target':
            self.target_pos = (player.rect.centerx, self.rect.midbottom[1]) # 目標位置為玩家的水平位置
            if self.target_pos:
                dx = self.target_pos[0] - self.rect.centerx
                direction = 1 if dx > 0 else -1
                is_stuck_at_wall = ((self.rect.left <= self.left_boundary and direction == -1) or (self.rect.right >= self.right_boundary and direction == 1))
                if abs(dx) < self.move_speed or is_stuck_at_wall:
                    self.state = 'jumping_up'; self.vy = self.jump_speed
                else:
                    self.rect.x += self.move_speed * direction
                    if self.rect.left < self.left_boundary: self.rect.left = self.left_boundary
                    if self.rect.right > self.right_boundary: self.rect.right = self.right_boundary
        
        elif self.state == 'jumping_up':
            self.vy += self.jump_gravity; self.rect.y += self.vy
            if self.vy >= 0: self.state = 'falling_down'

        elif self.state == 'falling_down':
            self.vy += self.gravity; self.rect.y += self.vy
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.vy > 0:
                    self.rect.bottom = platform.rect.top; self.vy = 0
                    self.state = 'shockwave_stage2'; break

        elif self.state == 'shockwave_stage2':
            wave = Shockwave(self.rect.midbottom, self.rect.width, damage=80, stage=2, lifetime=60)
            monster_effect_group.add(wave)
            self.state = 'idle'
            self.attack_cooldown = 30 #震地後搖0.5秒
        
        # 轉向判斷 (不變)
        if self.state in ['idle', 'moving_to_target']:
            if player.rect.centerx > self.rect.centerx: self.image = self.image_right
            else: self.image = self.image_left
            
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