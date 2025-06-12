import pygame
import os
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop
import lobby.game_map as game_map
import level2.level2_game as level2_game
import level3.level3_game as level3_game
import json

def save_player_data_list(players, filename="player_data.json"):
    with open(filename, "w") as f:
        json.dump([p.to_dict() for p in players], f)

def load_player_data(filename="player_data.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        data = json.load(f)
    return [Player.from_dict(d) for d in data]

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Lobby")

# 載入背景圖
bg_path = os.path.join("assets", "background", "lobby.png")
background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (800, 600))

# 取得圖片寬高
bg_rect = background.get_rect()
bg_rect.topleft = (0, 0)  # 設定左上角在 (0, 0)


players = load_player_data()
current_player = show_login_screen(players)
current_player.rect.center = (400, 500)
current_player.current_map = "lobby"

running = True
clock = pygame.time.Clock()
# 主迴圈
while running:
    # ### DEBUG ### 在每一幀開始時印出當前地圖狀態
    print(f"--- FRAME START --- Map: {current_player.current_map}, Player at: {current_player.rect.center}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_player.current_map == "shop":
            shop.handle_events(event, current_player)
        elif current_player.current_map in ("lobby", "game_map"):
            target_map = current_player.check_portal_trigger(event)
            if target_map == "exit":
                # ... 省略 ...
                running = False
            elif target_map:
                current_player.current_map = target_map
    
    keys = pygame.key.get_pressed()
    
    # 根據當前地圖更新遊戲狀態
    if current_player.current_map == "lobby":
        screen.blit(background, (0, 0))
        current_player.handle_input(keys)
        current_player.draw(screen)

    elif current_player.current_map == "shop":
        # ... 省略 ...
        shop.render(screen, current_player)

    elif current_player.current_map == "game_map":
        game_map.render(screen, current_player)
        current_player.handle_input(keys)

        level1_zone = pygame.Rect(50, 475, 150, 40)
        level2_zone = pygame.Rect(400, 90, 100, 90)
        level3_zone = pygame.Rect(610, 80, 100, 50)

        font = pygame.font.SysFont(None, 36)
        prompt_text = font.render("Press Enter to start the game", True, (255, 255, 255))

        if level1_zone.collidepoint(current_player.rect.center):
            screen.blit(prompt_text, (300, 550))
            if keys[pygame.K_RETURN]:
                print("### DEBUG ### 'Level 1' 區域觸發 (載入 Level 2)")
                current_player.image = pygame.image.load("assets/player/fighter.png")
                current_player.resize_image(current_player.image_size)
                level2_game.init_level2(current_player)
                print(f"### DEBUG ### 地圖狀態被 init_level2 設定為: {current_player.current_map}")
                
        elif level2_zone.collidepoint(current_player.rect.center):
            screen.blit(prompt_text, (300, 550))
            if keys[pygame.K_RETURN]:
                print("### DEBUG ### 'Level 2' 區域觸發")
                current_player.image = pygame.image.load("assets/player/fighter.png")
                current_player.resize_image(current_player.image_size)
                level2_game.init_level2(current_player)
                print(f"### DEBUG ### 地圖狀態被 init_level2 設定為: {current_player.current_map}")
                
        elif level3_zone.collidepoint(current_player.rect.center):
            screen.blit(prompt_text, (300, 550))
            if keys[pygame.K_RETURN]:
                print("### DEBUG ### 'Level 3' 區域觸發")
                current_player.image = pygame.image.load("assets/player/archer.png")
                current_player.resize_image(current_player.image_size)
                level3_game.init_level3(current_player)
                print(f"### DEBUG ### 地圖狀態被 init_level3 設定為: {current_player.current_map}")
                
    elif current_player.current_map == "level2":
        level2_game.update_level2(current_player, screen)
    elif current_player.current_map == "level3":
        level3_game.update_level3(current_player, screen)
    else:
        screen.blit(background, (0, 0))
        current_player.draw(screen)

    pygame.display.flip()
    clock.tick(60) # 建議用 60 幀比較穩定