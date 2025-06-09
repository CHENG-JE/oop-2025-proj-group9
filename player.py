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
                pygame.Rect(0, 0, 775, 250),
                pygame.Rect(116, 325, 36, 5),
                pygame.Rect(217, 286, 144, 1),                
                ],
            "game_map": [
                pygame.Rect(250,172,80,100),
                pygame.Rect(270,390,60,100),
                pygame.Rect(380,500,500,100),
                pygame.Rect(270,500,500,100)
            ],
            "level2":[

            ]

        }
        if self.current_map == "lobby":
            self.trigger_areas = [
                {"rect": pygame.Rect(98, 405, 97, 50), "message": "Do you want to buy something?", "pos": (20, 150), "target": "shop"},
                {"rect": pygame.Rect(497, 320, 123, 20), "message": "Play the game NOW!", "pos": (440, 40), "target": "game_map"}
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


    def can_move_to_dx(self, dx):
        future_rect = self.rect.move(dx, 0)
        for block in self.blocked_areas.get(self.current_map, []):
            if future_rect.colliderect(block):
                return False
        return True

    def can_move_to_dy(self, dy):
        future_rect = self.rect.move(0, dy)
        for block in self.blocked_areas.get(self.current_map, []):
            if future_rect.colliderect(block):
                return False
        return True

    def handle_input(self, keys):
        print("KEYDOWN:", (self.rect.centerx, self.rect.centery))  # 檢測座標用
        if self.current_map == "lobby":
            speed = 5
        else: 
            speed = 5
        if keys[pygame.K_a] and self.can_move_to_dx(-5) and self.rect.left > -50:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.can_move_to_dx(5) and self.rect.right < 850:
            self.rect.x += speed
        if keys[pygame.K_w] and self.can_move_to_dy(-5) and self.rect.top > 0:
            self.rect.y -= speed
        if keys[pygame.K_s] and self.can_move_to_dy(5) and self.rect.bottom < 610:
            self.rect.y += speed

        self.check_trigger_area()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.current_trigger_info:
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.current_trigger_info["message"], True, (220, 220, 220))
            screen.blit(text, self.current_trigger_info["pos"])
        money_font = pygame.font.SysFont(None, 28)
        money_text = money_font.render(f"Money: ${self.money}", True, (250, 250, 250))  # 黃色金額
        screen.blit(money_text, (20, 20))  # 左上角座標
        
        blood_font = pygame.font.SysFont(None, 28)
        blood_text = blood_font.render(f"Blood: {self.blood}/{self.max_blood}", True, (250, 250, 250))  # 黃色金額
        screen.blit(blood_text, (20, 40))  # 左上角座標

        exp_font = pygame.font.SysFont(None, 28)
        exp_text = exp_font.render(f"Exp: {self.exp}/1000", True, (250, 250, 250))  # 黃色金額
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
    # 預留未來動畫或狀態更新用，目前不做任何事
        pass