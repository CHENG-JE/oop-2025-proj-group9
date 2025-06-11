import pygame
import os
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop
import lobby.game_map as game_map
import level2.level2_game as level2_game
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_player.current_map == "shop":
            shop.handle_events(event, current_player)
        elif current_player.current_map in ("lobby", "game_map"):
            target_map = current_player.check_portal_trigger(event)
            if target_map == "exit":
                # 更新 players 列表中對應 current_player 的狀態
                for i, p in enumerate(players):
                    if p.original_image_path == current_player.original_image_path:
                        players[i] = current_player
                        break
                else:
                    players.append(current_player)
                save_player_data_list(players)
                running = False
            elif target_map:
                current_player.current_map = target_map

    # 持續檢測鍵盤按鍵狀態（非 event-based）
    if current_player.current_map in ("lobby", "game_map", "shop"):
        keys = pygame.key.get_pressed()
        current_player.handle_input(keys)

        # 在 shop 中按 ESC 回到 lobby
        if current_player.current_map == "shop":
            if keys[pygame.K_ESCAPE]:
                current_player.current_map = "lobby"

    if current_player.current_map == "shop":
        shop.render(screen, current_player)
    elif current_player.current_map == "game_map":
        game_map.render(screen, current_player)

        # 進入level1
        zone_rect = pygame.Rect(105, 430, 120, 100)  # 將高度由 0 改為 100
        if zone_rect.collidepoint(current_player.rect.center):
            font = pygame.font.SysFont(None, 36)
            text = font.render("Press Enter to start the game", True, (255, 255, 255))
            # 將提示顯示邏輯放在地圖繪製之後
            screen.blit(text, (300, 550))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # 更換玩家圖片與切換關卡
                current_player.image = pygame.image.load("assets/player/fighter.png")
                current_player.image = pygame.transform.scale(current_player.image, current_player.image_size)
                level2_game.init_level2(current_player)
                current_player.current_map = "level1"

        # level2
        zone_rect = pygame.Rect(600, 200, 120, 100)  # 將高度由 0 改為 100
        if zone_rect.collidepoint(current_player.rect.center):
            font = pygame.font.SysFont(None, 36)
            text = font.render("Press Enter to start the game", True, (255, 255, 255))
            # 將提示顯示邏輯放在地圖繪製之後
            screen.blit(text, (300, 550))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # 更換玩家圖片與切換關卡
                current_player.image = pygame.image.load("assets/player/fighter.png")
                current_player.image = pygame.transform.scale(current_player.image, current_player.image_size)
                level2_game.init_level2(current_player)
                current_player.current_map = "level2"
        
        # level3
        zone_rect = pygame.Rect(384, 150, 120, 100)  # 將高度由 0 改為 100
        if zone_rect.collidepoint(current_player.rect.center):
            font = pygame.font.SysFont(None, 36)
            text = font.render("Press Enter to start the game", True, (255, 255, 255))
            # 將提示顯示邏輯放在地圖繪製之後
            screen.blit(text, (300, 550))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # 更換玩家圖片與切換關卡
                current_player.image = pygame.image.load("assets/player/fighter.png")
                current_player.image = pygame.transform.scale(current_player.image, current_player.image_size)
                level2_game.init_level2(current_player)
                current_player.current_map = "level2"

    elif current_player.current_map == "level2":
        level2_game.update_level2(current_player, screen)
    else:
        screen.blit(background, (0, 0))
        current_player.draw(screen)

    pygame.display.flip()
    clock.tick(120)  # 加這一行來限制 FPS
