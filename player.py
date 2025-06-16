# player.py (修正版)
import pygame
import ui
import math

class Player:
    def __init__(self, image_path, position, size=(150, 150)):
        # --- 核心屬性 ---
        self.original_image_path = image_path
        self.image_size = size
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=position)
        
        # --- 遊戲狀態 ---
        self.current_map = "lobby"
        self.money = 500
        self.max_blood = 100
        self.blood = 100
        self.exp = 0

        # --- 行為與狀態控制 ---
        self.facing_right = True
        self.attack_cooldown = 0
        self.invincible_timer = 0
        self.shoot_timer = 0
        self.kills = 0
        self.map_initialized = {"lobby": False, "game_map": False}

        # --- 各關卡專用物理屬性 ---
        self.original_droplet_image = None
        self.pos_vector = pygame.math.Vector2(position)
        self.hitbox = pygame.Rect(0, 0, 16, 16)
        self.vy = 0
        self.on_ground = False
        self.gravity = 0.4
        self.jump_speed = -14
        self.move_speed = 7
        self.original_image_right = self.image
        self.original_image_left = pygame.transform.flip(self.image, True, False)
        
        # --- 地圖碰撞與觸發 ---
        self.blocked_areas = {
            "lobby": [pygame.Rect(0, 0, 775, 270), pygame.Rect(230, 286, 144, 20), pygame.Rect(680, 325, 90, 55), pygame.Rect(70, 315, 110, 55)],
            "game_map": [pygame.Rect(280,485,600,200), pygame.Rect(280,375,70,200), pygame.Rect(570,435,600,200), pygame.Rect(630,405,600,200), pygame.Rect(260,265,40,30), pygame.Rect(290,195,50,30)],
        }
        self.trigger_areas = [
                {"rect": pygame.Rect(60, 405, 110, 50), "message": "Do you want to buy something?", "pos": (20, 150), "target": "shop"},
                {"rect": pygame.Rect(490, 315, 150, 50), "message": "Play the game NOW!", "pos": (440, 40), "target": "game_map"},
                {"rect": pygame.Rect(655, 425, 200, 50), "message": "Exit Game?", "pos": (635, 320), "target": "exit"}
            ]
        self.current_trigger_info = None

    def set_level_mode(self, level_name, boundaries=(50, 750)):
        self.current_map = level_name
        
        if level_name == "level1":
            # === 修正：確保 self.original_droplet_image 是縮小後的版本 ===
            loaded_image = pygame.image.load("assets/player/droplet.png").convert_alpha()
            self.original_droplet_image = pygame.transform.scale(loaded_image, (34, 17))
            self.image = self.original_droplet_image.copy() # 使用副本作為當前圖像
            
            self.rect = self.image.get_rect(center=(400, 300))
            self.pos_vector = pygame.math.Vector2(self.rect.center)
            self.hitbox.center = self.rect.center
            self.image_size = (34, 17)
        
        elif level_name == "level2":
            self.image = pygame.image.load("assets/player/fighter.png").convert_alpha()
            self.image_size = (100, 100)
            self.resize_image(self.image_size)
            self.rect.center = (400, 500)

        elif level_name == "level3":
            archer_img = pygame.image.load("assets/player/archer.png").convert_alpha()
            self.image_size = (120, 120)
            self.original_image_right = pygame.transform.scale(archer_img, self.image_size)
            self.original_image_left = pygame.transform.flip(self.original_image_right, True, False)
            self.image = self.original_image_right
            self.rect = self.image.get_rect(midbottom=(250, 500))
            self.left_boundary, self.right_boundary = boundaries
            self.vy = 0
            self.on_ground = False

        else: # Lobby / Game Map
            self.image_size = (150, 150)
            self.reset_image()

    def update(self, **kwargs):
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        if self.invincible_timer > 0: self.invincible_timer -= 1
        
        if self.current_map == "level3":
            self._update_physics_level3(kwargs.get('platforms', []))

    def handle_input(self, keys, **kwargs):
        print("Player Position:", self.rect.center)
        
        if self.current_map == "level1":
            self._handle_input_level1(keys, kwargs.get('walls', []))
        elif self.current_map == "level2":
            self._handle_input_level2(keys)
        elif self.current_map == "level3":
            self._handle_input_level3(keys, kwargs.get('projectile_group'))
        else:
            self._handle_input_lobby(keys)

    def draw(self, screen):
        if self.current_map == 'level3' and self.invincible_timer > 0 and self.invincible_timer % 10 < 5:
            pass
        else:
            screen.blit(self.image, self.rect)

        if self.current_map == "lobby" and self.current_trigger_info:
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.current_trigger_info["message"], True, (220, 220, 220))
            screen.blit(text, self.current_trigger_info["pos"])

    def _handle_input_level1(self, keys, walls):
        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: move_vector.y = -1
        if keys[pygame.K_s]: move_vector.y = 1
        if keys[pygame.K_a]: move_vector.x = -1
        if keys[pygame.K_d]: move_vector.x = 1

        if move_vector.length_squared() > 0:
            move_vector.normalize_ip()
            angle = move_vector.angle_to(pygame.math.Vector2(0, -1))
            self.image = pygame.transform.rotate(self.original_droplet_image, angle)
            self.rect = self.image.get_rect(center=self.hitbox.center)
            
            speed = 3
            self.pos_vector.x += move_vector.x * speed
            self.hitbox.centerx = round(self.pos_vector.x)
            for wall in walls:
                if self.hitbox.colliderect(wall.rect):
                    if move_vector.x > 0: self.hitbox.right = wall.rect.left
                    elif move_vector.x < 0: self.hitbox.left = wall.rect.right
                    self.pos_vector.x = self.hitbox.centerx
            
            self.pos_vector.y += move_vector.y * speed
            self.hitbox.centery = round(self.pos_vector.y)
            for wall in walls:
                if self.hitbox.colliderect(wall.rect):
                    if move_vector.y > 0: self.hitbox.bottom = wall.rect.top
                    elif move_vector.y < 0: self.hitbox.top = wall.rect.bottom
                    self.pos_vector.y = self.hitbox.centery
            
            self.rect.center = self.hitbox.center

    def _handle_input_level2(self, keys):
        speed = 10
        if keys[pygame.K_a] and self.rect.left > 0: self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < 800: self.rect.x += speed
        if keys[pygame.K_w] and self.rect.top > 0: self.rect.y -= speed
        if keys[pygame.K_s] and self.rect.bottom < 600: self.rect.y += speed

    def _handle_input_level3(self, keys, projectile_group):
        if keys[pygame.K_a] and self.rect.left > self.left_boundary:
            self.rect.x -= self.move_speed
            if self.facing_right:
                self.facing_right = False
                self.image = self.original_image_left
        if keys[pygame.K_d] and self.rect.right < self.right_boundary:
            self.rect.x += self.move_speed
            if not self.facing_right:
                self.facing_right = True
                self.image = self.original_image_right
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = self.jump_speed
            
        if keys[pygame.K_j] and self.attack_cooldown == 0:
            from weapon import Arrow
            direction = "right" if self.facing_right else "left"
            arrow = Arrow(self.rect.centerx, self.rect.centery, direction, damage=20)
            if projectile_group is not None:
                projectile_group.add(arrow)
            self.attack_cooldown = 30
    
    def _update_physics_level3(self, platforms):
        self.vy += self.gravity
        self.rect.y += self.vy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                self.on_ground = True
                break

    def _handle_input_lobby(self, keys):
        speed = 10
        if keys[pygame.K_a] and self.rect.left > -50 and self.can_move_to_dx(-speed): self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < 850 and self.can_move_to_dx(speed): self.rect.x += speed
        if keys[pygame.K_w] and self.rect.top > 0 and self.can_move_to_dy(-speed): self.rect.y -= speed
        if keys[pygame.K_s] and self.rect.bottom < 610 and self.can_move_to_dy(speed): self.rect.y += speed
        self.check_trigger_area()

    def get_collision_rect(self):
        shrink_ratio = 0.6
        new_width = int(self.rect.width * shrink_ratio)
        new_height = int(self.rect.height * shrink_ratio)
        return pygame.Rect(self.rect.centerx - new_width / 2, self.rect.centery - new_height / 2, new_width, new_height)

    def can_move_to_dx(self, dx):
        future_rect = self.get_collision_rect().move(dx, 0)
        return not any(future_rect.colliderect(block) for block in self.blocked_areas.get(self.current_map, []))

    def can_move_to_dy(self, dy):
        future_rect = self.get_collision_rect().move(0, dy)
        return not any(future_rect.colliderect(block) for block in self.blocked_areas.get(self.current_map, []))
    
    def check_trigger_area(self):
        self.current_trigger_info = None
        if self.current_map == "lobby":
            for area in self.trigger_areas:
                if area["rect"].collidepoint(self.rect.center):
                    self.current_trigger_info = {"message": area["message"], "pos": area["pos"], "target": area["target"]}
                    break
    
    def check_portal_trigger(self, event):
        if self.current_map == "lobby" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.current_trigger_info:
                return self.current_trigger_info.get("target")
        return None

    def resize_image(self, size):
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def reset_image(self):
        self.image = pygame.image.load(self.original_image_path).convert_alpha()
        self.resize_image(self.image_size)
    
    def take_damage(self, amount):
        self.blood = max(0, self.blood - amount)

    def to_dict(self):
        return { "image_path": self.original_image_path, "position": self.rect.center, "image_size": self.image_size, "current_map": self.current_map, "money": self.money, "max_blood": self.max_blood, "blood": self.blood, "exp": self.exp }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["image_path"], data["position"], tuple(data["image_size"]))
        player.current_map = data.get("current_map", "lobby")
        player.money = data.get("money", 500)
        player.max_blood = data.get("max_blood", 100)
        player.blood = data.get("blood", 100)
        player.exp = data.get("exp", 0)
        return player