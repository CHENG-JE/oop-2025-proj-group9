import pygame
import os
from player import Player
from log_in import show_login_screen
import shop
import game_map

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


# 玩家列表與初始選定角色
current_player = show_login_screen()
current_player.rect.center = (400, 500)
current_player.current_map = "lobby"  # ← 加在這

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
            if target_map:
                current_player.current_map = target_map

    # 持續檢測鍵盤按鍵狀態（非 event-based）
    if current_player.current_map in ("lobby", "game_map"):
        keys = pygame.key.get_pressed()
        current_player.handle_input(keys)

    if current_player.current_map == "shop":
        shop.render(screen, current_player)
    elif current_player.current_map == "game_map":
        game_map.render(screen, current_player)
    else:
        screen.blit(background, (0, 0))
        current_player.draw(screen)

    pygame.display.flip()
    clock.tick(120)  # 加這一行來限制 FPS
