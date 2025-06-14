import pygame

class Player:
    def __init__(self, image_path, position, size=(150, 150)):
        self.image_size = size
        self.original_image_path = image_path  # 儲存初始圖片路徑
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.current_map = "lobby"
        self.blocked_areas = {
            "lobby": [
                pygame.Rect(0, 0, 775, 270), #wall
                pygame.Rect(230, 286, 144, 20), #chair           
                pygame.Rect(680, 325, 90, 55), #leave table                
                pygame.Rect(70, 315, 110, 55), #vending machine         
                ],
            "game_map": [
                pygame.Rect(280,485,600,200), #下方河流
                pygame.Rect(280,375,70,200) #下方河流s

            ],
            "level2":[

            ]
            #"level1":[] 如果有需要的話可以自己打上去
            #"level3":[]

        }
        if self.current_map == "lobby":
            self.trigger_areas = [
                {"rect": pygame.Rect(60, 405, 110, 50), "message": "Do you want to buy something?", "pos": (20, 150), "target": "shop"},
                {"rect": pygame.Rect(490, 315, 150, 50), "message": "Play the game NOW!", "pos": (440, 40), "target": "game_map"},
                {"rect": pygame.Rect(655, 425, 200, 50), "message": "Exit Game?", "pos": (635, 320), "target": "exit"}
            ]
        self.current_trigger_info = None
        self.money = 500 # 初始金額

        self.max_blood = 100
        self.blood = 100 #初始血量
        self.exp = 0 #初始經驗值
        self.map_initialized = {
            "lobby": False,
            "game_map": False
        }

        # === 為 Level 3 新增的屬性 ===
        self.vy = 0  # 垂直速度
        self.on_ground = False  # 是否在地面上
        self.facing_right = True  # 面朝方向，True為右
        self.attack_cooldown = 0  # 攻擊冷卻計時器
        self.invincible_timer = 0 # 無敵計時器


    def get_collision_rect(self):
        shrink_ratio = 0.6 #比例
        new_width = int(self.rect.width * shrink_ratio)
        new_height = int(self.rect.height * shrink_ratio)
        new_rect = pygame.Rect(0, 0, new_width, new_height)
        new_rect.center = self.rect.center
        return new_rect

    def can_move_to_dx(self, dx):
        future_rect = self.get_collision_rect().move(dx, 0)
        for block in self.blocked_areas.get(self.current_map, []):
            if future_rect.colliderect(block):
                return False
        return True

    def can_move_to_dy(self, dy):
        future_rect = self.get_collision_rect().move(0, dy)
        for block in self.blocked_areas.get(self.current_map, []):
            if future_rect.colliderect(block):
                return False
        return True

    def handle_input(self, keys):
        # 這個 handle_input 主要用於 lobby 和 level2 的俯視角移動
        # level3 的平台跳躍移動邏輯在 level3_game.py 中處理
        print("KEYDOWN:", (self.rect.centerx, self.rect.centery))  # 檢測座標用
        if self.current_map == "lobby":
            speed =10
        else: 
            speed = 10
        if keys[pygame.K_a] and self.can_move_to_dx(-5) and self.rect.left > -50:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.can_move_to_dx(5) and self.rect.right < 850:
            self.rect.x += speed
        if keys[pygame.K_w] and self.can_move_to_dy(-5) and self.rect.top > 0:
            self.rect.y -= speed
        if keys[pygame.K_s] and self.can_move_to_dy(5) and self.rect.bottom < 610:
            self.rect.y += speed

        self.check_trigger_area()

    def draw(self, screen,show_status = True):
        screen.blit(self.image, self.rect)
        if self.current_trigger_info:
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.current_trigger_info["message"], True, (220, 220, 220))
            screen.blit(text, self.current_trigger_info["pos"])
        if show_status:
            money_font = pygame.font.SysFont(None, 28)
            money_text = money_font.render(f"Money: ${self.money}", True, (250, 250, 250))  # 黃色金額
            screen.blit(money_text, (20, 20))  # 左上角座標
            
            blood_font = pygame.font.SysFont(None, 28)
            blood_text = blood_font.render(f"HP: {self.blood}/{self.max_blood}", True, (250, 250, 250))  # 黃色金額
            screen.blit(blood_text, (20, 40))  # 左上角座標

            exp_font = pygame.font.SysFont(None, 28)
            exp_text = exp_font.render(f"EXP: {self.exp}/1000", True, (250, 250, 250))  # 黃色金額
            screen.blit(exp_text, (20, 60))  # 左上角座標

    def can_move_to(self, dx, dy):
        future_rect = self.rect.move(dx, dy)
        for block in self.blocked_areas.get(self.current_map, []):
            if future_rect.colliderect(block):
                return False
        return True
    
    def check_trigger_area(self):
        self.current_trigger_info = None
        if self.current_map == "lobby":
            for area in self.trigger_areas:
                if area["rect"].collidepoint(self.rect.center):
                    self.current_trigger_info = {"message": area["message"], "pos": area["pos"]}
                    break
    def check_portal_trigger(self, event):
        if self.current_map == "lobby" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            for area in self.trigger_areas:
                if area["rect"].collidepoint(self.rect.center):
                    return area.get("target")
        return False
    def reset_image(self):
        self.image = pygame.image.load(self.original_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.image_size)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def resize_image(self, size):
        self.image = pygame.transform.scale(self.image, size)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
    # 更新所有計時器
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def to_dict(self):
        return {
            "image_path": self.original_image_path,
            "position": self.rect.center,
            "image_size": self.image_size,
            "current_map": self.current_map,
            "money": self.money,
            "max_blood": self.max_blood,
            "blood": self.blood,
            "exp": self.exp
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["image_path"], data["position"], tuple(data["image_size"]))
        player.current_map = data.get("current_map", "lobby")
        player.money = data.get("money", 500)
        player.max_blood = data.get("max_blood", 100)
        player.blood = data.get("blood", 100)
        player.exp = data.get("exp", 0)
        return player