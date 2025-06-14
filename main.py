# main.py
import pygame, os, sys, json
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop, lobby.game_map as game_map
import level1.level1_game as level1_game
import level2.level2_game as level2_game
import level3.level3_game as level3_game
import pause # 導入暫停選單

def save_player_data_list(players, filename="player_data.json"):
    with open(filename, "w") as f: json.dump([p.to_dict() for p in players], f, indent=4)
def load_player_data(filename="player_data.json"):
    if not os.path.exists(filename): return []
    try:
        with open(filename, "r") as f: data = json.load(f)
        return [Player.from_dict(d) for d in data]
    except (json.JSONDecodeError, TypeError): return []

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Lobby")
try:
    bg_path = os.path.join("assets", "background", "lobby.png")
    background = pygame.image.load(bg_path); background = pygame.transform.scale(background, (800, 600))
except pygame.error:
    background = pygame.Surface((800, 600)); background.fill((0, 0, 0))

players = load_player_data()
if not players: pygame.quit(); sys.exit()
current_player = show_login_screen(players)
current_player.rect.center = (400, 500); current_player.current_map = "lobby"

# --- 新增暫停狀態 ---
is_paused = False

running = True
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        
        # --- 新增：統一的 ESC 鍵處理 ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_player.current_map in ["level1", "level2", "level3"]:
                    is_paused = not is_paused # 在關卡中，切換暫停狀態
                elif current_player.current_map == "shop":
                    current_player.current_map = "lobby" # 在商店中，返回大廳

        if current_player.current_map == "lobby":
            target_map = current_player.check_portal_trigger(event)
            if target_map == "exit": running = False
            elif target_map: current_player.current_map = target_map

    # --- 狀態更新與繪圖 ---
    keys = pygame.key.get_pressed()
    
    if is_paused:
        # 如果遊戲暫停，顯示並處理暫停選單
        pause.draw_menu(screen)
        action = pause.handle_input()
        if action:
            if action == "continue": is_paused = False
            elif action == "restart":
                if current_player.current_map == "level1": level1_game.init_level1(current_player)
                elif current_player.current_map == "level2": level2_game.init_level2(current_player)
                elif current_player.current_map == "level3": level3_game.init_level3(current_player)
                is_paused = False
            elif action == "leave":
                current_player.current_map = "game_map"; current_player.reset_image(); current_player.rect.center = (420, 180)
                is_paused = False
            elif action == "menu":
                pause.show_rules_screen(screen)
    else:
        # 如果遊戲未暫停，執行正常的遊戲邏輯
        game_status = None
        current_level_name = current_player.current_map
        
        # 繪製當前畫面
        if current_player.current_map == "lobby":
            current_player.handle_input(keys); screen.blit(background, (0, 0)); current_player.draw(screen)
        elif current_player.current_map == "shop":
            shop.render(screen, current_player)
        elif current_player.current_map == "game_map":
            current_player.handle_input(keys); game_map.render(screen, current_player)
            level1_zone = pygame.Rect(50, 475, 150, 40); level2_zone = pygame.Rect(400, 90, 100, 90); level3_zone = pygame.Rect(610, 80, 100, 50)
            if level1_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
                level1_game.init_level1(current_player); current_player.current_map = "level1"
            elif level2_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
                current_player.image = pygame.image.load("assets/player/fighter.png"); current_player.resize_image(current_player.image_size); level2_game.init_level2(current_player); current_player.current_map = "level2"
            elif level3_zone.collidepoint(current_player.rect.center) and keys[pygame.K_RETURN]:
                current_player.image = pygame.image.load("assets/player/archer.png"); current_player.resize_image(current_player.image_size); level3_game.init_level3(current_player); current_player.current_map = "level3"
            font = pygame.font.SysFont(None, 36); prompt_text = font.render("Press Enter to start the game", True, (255, 255, 255))
            if any(zone.collidepoint(current_player.rect.center) for zone in [level1_zone, level2_zone, level3_zone]): screen.blit(prompt_text, (300, 550))
        
        # 呼叫關卡更新函式並接收狀態
        elif current_player.current_map == "level1": game_status = level1_game.update_level1(screen, current_player)
        elif current_player.current_map == "level2": game_status = level2_game.update_level2(current_player, screen)
        elif current_player.current_map == "level3": game_status = level3_game.update_level3(screen, current_player)

        # 處理遊戲結束
        if game_status in ["win", "lose"]:
            # 根據關卡和輸贏來設定獎懲
            win_condition = (game_status == "win")
            level_return_pos = (120, 490) # 預設 L1 返回點

            if win_condition:
                if current_level_name == "level1": current_player.money += 100; current_player.exp += 20
                elif current_level_name == "level3": current_player.money += 500; level_return_pos = (660, 110)
            else: # lose
                if current_level_name == "level1": current_player.money = max(0, current_player.money - 20)
                elif current_level_name == "level3": current_player.money = max(0, current_player.money - 300); level_return_pos = (660, 110)
                current_player.blood = 100
            
            # 返回地圖
            current_player.current_map = "game_map"
            current_player.reset_image()
            current_player.rect.center = level_return_pos

    pygame.display.flip()
    clock.tick(60)

save_player_data_list(players)
pygame.quit()
sys.exit()