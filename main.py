# main.py
import pygame
import os
import sys # 建議使用 sys.exit()
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop
import lobby.game_map as game_map
import level1.level1_game as level1_game
import level2.level2_game as level2_game
import level3.level3_game as level3_game
import json

def save_player_data_list(players, filename="player_data.json"):
    with open(filename, "w") as f:
        json.dump([p.to_dict() for p in players], f, indent=4) # 增加 indent 讓 json 更易讀

def load_player_data(filename="player_data.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return [Player.from_dict(d) for d in data]
    except (json.JSONDecodeError, TypeError):
        return [] # 如果 JSON 檔案損壞或格式不對，返回空列表

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Lobby")

# 載入背景圖 (使用 try-except 更穩健)
try:
    bg_path = os.path.join("assets", "background", "lobby.png")
    background = pygame.image.load(bg_path)
    background = pygame.transform.scale(background, (800, 600))
except pygame.error:
    print("錯誤：找不到 assets/background/lobby.png，將使用純黑背景。")
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))

# 取得圖片寬高
bg_rect = background.get_rect(topleft=(0, 0))


players = load_player_data()
if not players:
    # 如果沒有玩家數據，可以建立一個預設玩家或提示錯誤
    print("錯誤：找不到玩家數據 player_data.json 或檔案已損壞。")
    pygame.quit()
    sys.exit()

current_player = show_login_screen(players)
current_player.rect.center = (400, 500)
current_player.current_map = "lobby"

running = True
clock = pygame.time.Clock()

# === 主迴圈 ===
while running:
    # --- 事件處理迴圈 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # 點擊關閉按鈕，設定 flag 準備退出

        if current_player.current_map == "shop":
            shop.handle_events(event, current_player)
        elif current_player.current_map == "lobby": # game_map 的觸發改為非事件驅動
            target_map = current_player.check_portal_trigger(event)
            if target_map == "exit":
                running = False # 從遊戲內退出，同樣設定 flag
            elif target_map:
                current_player.current_map = target_map
    
    # --- 遊戲狀態更新 ---
    keys = pygame.key.get_pressed()
    
    if current_player.current_map == "lobby":
        current_player.handle_input(keys)
    elif current_player.current_map == "shop":
        if keys[pygame.K_ESCAPE]:
            current_player.current_map = "lobby"
    elif current_player.current_map == "game_map":
        current_player.handle_input(keys)
        # 關卡觸發判斷
        level1_zone = pygame.Rect(50, 475, 150, 40)
        level2_zone = pygame.Rect(400, 90, 100, 90)
        level3_zone = pygame.Rect(610, 80, 100, 50)
        
        if level1_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
            level1_game.init_level1(current_player)
            current_player.current_map = "level1"
        elif level2_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
            current_player.image = pygame.image.load("assets/player/fighter.png")
            current_player.resize_image(current_player.image_size)
            level2_game.init_level2(current_player)
        elif level3_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
            current_player.image = pygame.image.load("assets/player/archer.png")
            current_player.resize_image(current_player.image_size)
            level3_game.init_level3(current_player)
            current_player.current_map = "level3"

    # --- 繪圖區 ---
    if current_player.current_map == "lobby":
        screen.blit(background, (0, 0))
        current_player.draw(screen)
    elif current_player.current_map == "shop":
        shop.render(screen, current_player)
    elif current_player.current_map == "game_map":
        game_map.render(screen, current_player)
        # 可以在這裡繪製提示文字
        font = pygame.font.SysFont(None, 36)
        prompt_text = font.render("Press Enter to start the game", True, (255, 255, 255))
        if any(zone.collidepoint(current_player.rect.center) for zone in [level1_zone, level2_zone, level3_zone]):
            screen.blit(prompt_text, (300, 550))
    elif current_player.current_map == "level1":
        level1_game.update_level1(screen, current_player)
    elif current_player.current_map == "level2":
        level2_game.update_level2(current_player, screen) 
    elif current_player.current_map == "level3":
        level3_game.update_level3(screen, current_player)
    else:
        # 備用繪圖，防止有未定義的地圖狀態
        screen.blit(background, (0, 0))
        current_player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# === 迴圈結束後，安全退出 ===
print("遊戲主迴圈已結束，正在儲存與關閉...")
save_player_data_list(players)
pygame.quit()
sys.exit()