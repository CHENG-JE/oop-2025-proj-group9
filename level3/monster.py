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

        # === 狀態機與計時器 ===
        self.state = 'idle'
        self.attack_cooldown = 120 # 攻擊之間的冷卻
        self.shockwave_lifetime = 60 # 震波在畫面上持續的時間 (1秒)
        self.target_pos = None

        # 常數
        self.gravity = 2.2
        self.move_speed = 10 
        self.left_boundary, self.right_boundary = boundaries

    def update(self, platforms, player, monster_projectile_group, monster_effect_group):
        # Y軸物理模擬
        self.vy += self.gravity
        self.rect.y += self.vy
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                break
        
        # === 最終版 AI 狀態機 ===
        if self.state == 'idle':
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                # 決定攻擊模式
                if random.random() < 0.8: # 80% 機率光波
                    # --- 光波攻擊 ---
                    beam = MonsterBeam(self.rect.center, player.rect.center)
                    monster_projectile_group.add(beam)
                    self.attack_cooldown = 42 # 攻擊後冷卻 0.7 秒
                else: # 20% 機率震地
                    # --- 震地攻擊 ---
                    self.state = 'shockwave_stage1'
        
        elif self.state == 'shockwave_stage1':
            # 階段一：在原地放出第一個震波
            wave = Shockwave(self.rect.midbottom, self.rect.width, damage=30, stage=1)
            monster_effect_group.add(wave)
            
            # 記錄下當前玩家的X座標，作為移動目標
            self.target_pos = (player.rect.centerx, self.rect.midbottom[1])
            
            # 立刻進入移動狀態
            self.state = 'moving_to_target'

        elif self.state == 'moving_to_target':
            if self.target_pos:
                dx = self.target_pos[0] - self.rect.centerx
                # 判斷是否已到達目的地
                if abs(dx) < self.move_speed:
                    self.rect.centerx = self.target_pos[0]
                    self.state = 'shockwave_stage2' # 到達後進入最終階段
                else:
                    # 繼續朝目標移動
                    direction = 1 if dx > 0 else -1
                    self.rect.x += self.move_speed * direction
                    # 確保不出邊界
                    if self.rect.left < self.left_boundary: self.rect.left = self.left_boundary
                    if self.rect.right > self.right_boundary: self.rect.right = self.right_boundary
        
        elif self.state == 'shockwave_stage2':
            # 階段三：在移動後的位置放出第二個震波
            wave = Shockwave(self.rect.midbottom, self.rect.width, damage=50, stage=2)
            monster_effect_group.add(wave)
            
            # 整套攻擊結束，返回閒置狀態並進入冷卻
            self.state = 'idle'
            self.attack_cooldown = 180 # 震地攻擊的總冷卻時間為3秒

            
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