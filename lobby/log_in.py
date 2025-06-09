import pygame
import os
from player import Player

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


# 角色生成（你可以生成多個）
# 直接採用 Pygame 的絕對畫面座標，兩角色橫向置中分開
player1 = Player("assets/player/player1.png", (0, 0))
player1.rect.center = (300, 300)

player2 = Player("assets/player/player2.png", (0, 0))
player2.rect.center = (500, 300)

# 玩家列表與初始選定角色
players = [player1, player2]

# 顯示登入畫面，選擇角色
def show_login_screen():
    font = pygame.font.SysFont(None, 36)
    prompt = font.render("Use A / D to select character, Enter to start", True, (255, 255, 255))
    selected_index = 0
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                print("KEYDOWN:", event.key)  
                # 支援 A/D 大小寫，移除方向鍵支援
                if event.key == pygame.K_a:
                    selected_index = (selected_index - 1) % len(players)
                elif event.key == pygame.K_d:
                    selected_index = (selected_index + 1) % len(players)
                elif event.key == pygame.K_RETURN:
                    return players[selected_index]

        screen.fill((0, 0, 0))
        screen.blit(prompt, (200, 500))
        for i, player in enumerate(players):
            player.draw(screen)
            if i == selected_index:
                pygame.draw.rect(screen, (255, 255, 0), player.rect.inflate(10, 10), 3)
        pygame.display.flip()
        clock.tick(60)
