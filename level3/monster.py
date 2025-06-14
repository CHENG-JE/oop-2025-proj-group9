# level3/monster.py
import pygame
import random
import math
from weapon import MonsterBeam, Shockwave

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, boundaries):
        super().__init__()
        
        # === 改正 1：修正圖片方向邏輯 ===
        original_image_loaded = pygame.image.load("assets/enemy/monster.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image_loaded, (200, 200))
        
        # 假設你的原圖 monster.png 是朝左的
        self.image_left = scaled_image
        # 將朝左的圖水平翻轉，得到朝右的圖
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        
        # 初始時，怪物在右邊，應該朝左看
        self.image = self.image_left
        
        self.rect = self.image.get_rect(midbottom=pos)
        
        self.max_health = 1000
        self.health = self.max_health
        self.vy = 0

        # 狀態機與計時器
        self.state = 'idle'
        self.attack_cooldown = 120
        self.target_pos = None

        # 物理常數
        self.gravity = 2.2      # 正常(下落)重力
        self.move_speed = 15 
        self.left_boundary, self.right_boundary = boundaries
        
        # 非對稱跳躍用的物理常數
        self.jump_gravity = 0.68  # 上升時的慢速重力
        self.jump_speed = -18.5 # 上升時的初始速度

    def update(self, platforms, player, monster_projectile_group, monster_effect_group):
        # Y軸物理模擬 (在非跳躍狀態下)
        if self.state not in ['jumping_up', 'falling_down']:
            self.vy += self.gravity
            self.rect.y += self.vy
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.vy > 0:
                    self.rect.bottom = platform.rect.top; self.vy = 0; break
        
        # === 改正 2：恢復完整的跳躍攻擊流程 ===
        if self.state == 'idle':
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                if random.random() < 0.8:
                    beam = MonsterBeam(self.rect.center, player.rect.center)
                    monster_projectile_group.add(beam)
                    self.attack_cooldown = 42
                else:
                    self.state = 'shockwave_stage1'
        
        elif self.state == 'shockwave_stage1':
            wave = Shockwave(self.rect.midbottom, self.rect.width, damage=30, stage=1, lifetime=42)
            monster_effect_group.add(wave)
            self.target_pos = (player.rect.centerx, self.rect.midbottom[1])
            self.state = 'moving_to_target'

        elif self.state == 'moving_to_target':
            if self.target_pos:
                dx = self.target_pos[0] - self.rect.centerx
                direction = 1 if dx > 0 else -1
                is_stuck_at_wall = ((self.rect.left <= self.left_boundary and direction == -1) or (self.rect.right >= self.right_boundary and direction == 1))
                
                # 到達目的地後，進入跳躍，而不是直接攻擊
                if abs(dx) < self.move_speed or is_stuck_at_wall:
                    self.state = 'jumping_up' # <--- 進入上升跳躍狀態
                    self.vy = self.jump_speed   # <--- 設定起跳速度
                else:
                    self.rect.x += self.move_speed * direction
                    if self.rect.left < self.left_boundary: self.rect.left = self.left_boundary
                    if self.rect.right > self.right_boundary: self.rect.right = self.right_boundary
        
        # --- 新增回來的跳躍狀態 ---
        elif self.state == 'jumping_up':
            self.vy += self.jump_gravity # 使用上升的慢速重力
            self.rect.y += self.vy
            if self.vy >= 0: # 到達頂點
                self.state = 'falling_down'

        elif self.state == 'falling_down':
            self.vy += self.gravity # 使用下落的快速重力
            self.rect.y += self.vy
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.vy > 0:
                    self.rect.bottom = platform.rect.top; self.vy = 0
                    self.state = 'shockwave_stage2' # 落地後才進入最終攻擊
                    break
        # --- 跳躍狀態結束 ---

        elif self.state == 'shockwave_stage2':
            wave = Shockwave(self.rect.midbottom, self.rect.width, damage=50, stage=2, lifetime=60)
            monster_effect_group.add(wave)
            self.state = 'idle'
            self.attack_cooldown = 180
        
        # 轉向判斷
        if self.state in ['idle', 'moving_to_target']:
            if self.rect.centerx < player.rect.centerx:
                self.image = self.image_right
            else:
                self.image = self.image_left
            
    def draw_health_bar(self, screen):
        # (此函式不變)
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