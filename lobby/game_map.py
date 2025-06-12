import pygame
background = pygame.image.load("assets/background/game_map.jpg")
background = pygame.transform.scale(background, (800, 600))

def render(screen, current_player=None):
    screen.blit(background, (0, 0))  # 畫地圖背景

    if current_player:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            current_player.resize_image((150, 150))
            current_player.map_initialized["game_map"] = False  # 讓下次進入會重設位置
            current_player.rect.center = (570, 325)  # 你想要的新位置
            current_player.current_map = "lobby"
            return

        if current_player.current_map == "game_map":
            # 如果第一次進入 game_map，設定位置與縮放
            if not current_player.map_initialized.get("game_map", False):
                current_player.rect.center = (100, 305)  # 你想要的新位置
                current_player.resize_image((100, 100))
                current_player.map_initialized["game_map"] = True
            else:
                # 即使不是第一次，仍確保圖片縮放正確
                current_player.resize_image((100, 100))
                #current_player.rect.center = (100, 500)  # 你想要的新位置

        #current_player.handle_input(keys) 
        current_player.draw(screen)
        # 顯示右上角提示文字
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Press ESC back to the Lobby", True, (255, 255, 255))
        bg_rect = text_surface.get_rect(topleft=(570, 575))


        #pygame.draw.rect(screen, (0, 0, 0), bg_rect)  # 畫黑色底框
        screen.blit(text_surface, bg_rect)