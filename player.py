import pygame

class Player:
    def __init__(self, image_path, position, size=(150, 150)):
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
            "game_map": []
        }
        self.trigger_areas = [
            {"rect": pygame.Rect(98, 405, 97, 50), "message": "Do you want to buy something?", "pos": (20, 150)},
            {"rect": pygame.Rect(497, 320, 123, 50), "message": "Play the game NOW!", "pos": (440, 40)}
        ]
        self.current_trigger_info = None
    def handle_input(self):
        keys = pygame.key.get_pressed()
        print("KEYDOWN:", (self.rect.centerx,self.rect.centery))#檢測座標用  

        # Use self.rect.centerx and self.rect.centery for movement
        # Boundary based on image size (150x150): center cannot go beyond 75 from edge
        if keys[pygame.K_a] and self.can_move_to(-1, 0) and self.rect.centerx >= 35:
            self.rect.centerx -= 1
        if keys[pygame.K_d] and self.can_move_to(1, 0) and self.rect.centerx <= 763:
            self.rect.centerx += 1

        if keys[pygame.K_w] and self.can_move_to(0, -1) and self.rect.centery >= 66:
            self.rect.centery -= 1

        if keys[pygame.K_s] and self.can_move_to(0, 1) and self.rect.centery <= 530:
            self.rect.centery += 1

        self.check_trigger_area()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.current_trigger_info:
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.current_trigger_info["message"], True, (220, 220, 220))
            screen.blit(text, self.current_trigger_info["pos"])

    def can_move_to(self, dx, dy):
        future_rect = self.rect.copy()
        future_rect.centerx += dx
        future_rect.centery += dy
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