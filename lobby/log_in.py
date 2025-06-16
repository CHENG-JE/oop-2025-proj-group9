import pygame
import os
from player import Player
import json

def load_players_from_json(file_path="player_data.json"):
    with open(file_path, "r") as f:
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


# 角色生成（你可以生成多個）
# 從 JSON 載入角色資料
players = load_players_from_json()

# 顯示登入畫面，選擇角色
def show_login_screen(players):
    font = pygame.font.SysFont(None, 36)
    prompt = font.render("Use A / D to select character, Enter to start", True, (255, 255, 255))
    selected_index = 0
    clock = pygame.time.Clock()
    
    # 在登入畫面顯示時，為每個角色設定選擇位置
    select_positions = [(300 + i * 200, 300) for i in range(len(players))]
    
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
            # 暫存原始位置
            orig_center = player.rect.center
            # 移動到選擇位置繪製
            player.rect.center = select_positions[i]
            player.draw(screen)
            if i == selected_index:
                pygame.draw.rect(screen, (255, 255, 0), player.rect.inflate(10, 10), 3)
            # 恢復原始位置
            player.rect.center = orig_center

        selected_player = players[selected_index]
        info_font = pygame.font.SysFont(None, 28)
        money_text = info_font.render(f"Money: ${selected_player.money}", True, (255, 255, 255))
        blood_text = info_font.render(f"HP: {selected_player.blood}/{selected_player.max_blood}", True, (255, 255, 255))
        exp_text = info_font.render(f"EXP: {selected_player.exp}/1000", True, (255, 255, 255))

        screen.blit(money_text, (20, 20))
        screen.blit(blood_text, (20, 40))
        screen.blit(exp_text, (20, 60))

        pygame.display.flip()
        clock.tick(60)
