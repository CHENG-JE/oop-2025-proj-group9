import pygame
import os
from player import Player
from log_in import show_login_screen

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
# 主迴圈
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current_player.handle_input()

    screen.blit(background, (0, 0))
    current_player.draw(screen)

    pygame.display.flip()
