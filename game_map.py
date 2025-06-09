import pygame
background = pygame.image.load("assets/background/game_map.jpg")
background = pygame.transform.scale(background, (800, 600))

def render(screen, current_player=None):
    screen.blit(background, (0, 0))  # 畫地圖背景

    if current_player:
        if current_player.current_map == "game_map":
            # 如果第一次進入 game_map，設定位置與縮放
            if not current_player.map_initialized.get("game_map", False):
                current_player.rect.center = (100, 500)  # 你想要的新位置
                current_player.resize_image((100, 100))
                current_player.map_initialized["game_map"] = True
            current_player.handle_input(pygame.key.get_pressed())  # 允許移動
        current_player.draw(screen)