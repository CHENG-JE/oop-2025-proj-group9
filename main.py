# main.py
import pygame, os, sys, json
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop, lobby.game_map as game_map
import level1.level1_game as level1_game
import level2.level2_game as level2_game
import level3.level3_game as level3_game
import pause

# 音樂設定
pygame.mixer.init()

# 統一背景音樂播放函式
def play_bgm_for_map(map_name):
    bgm_files = {
        "lobby": os.path.join("assets", "music", "lobby.mp3"),
        "level1": os.path.join("assets", "music", "lev1.mp3"),
        "level2": os.path.join("assets", "music", "lev2.mp3"),
        "level3": os.path.join("assets", "music", "lev3.mp3"),
        "shop": os.path.join("assets", "music", "shop.mp3"),
        "game_map": os.path.join("assets", "music", "game_map.mp3")
    }
    if map_name in bgm_files:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(bgm_files[map_name])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

# (save/load 函式不變)
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

is_paused = False
running = True
clock = pygame.time.Clock()

while running:
    # === 改正：將 shop 的事件處理加回事件迴圈 ===
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        
        # 統一的 ESC 鍵處理
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_player.current_map in ["level1", "level2", "level3"]:
                    is_paused = not is_paused
                elif current_player.current_map == "shop":
                    current_player.current_map = "lobby"

        # 根據地圖處理對應的事件
        if current_player.current_map == "lobby":
            target_map = current_player.check_portal_trigger(event)
            if target_map == "exit": running = False
            elif target_map: current_player.current_map = target_map
        elif current_player.current_map == "shop":
            # 將事件傳遞給 shop 模組處理
            shop.handle_events(event, current_player)

    # --- 狀態更新與繪圖 ---
    keys = pygame.key.get_pressed()
    
    if is_paused:
        action = pause.show(screen, current_player.current_map)
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
            pause.show_rules_screen(screen, current_player.current_map)

    else:
        # 如果遊戲未暫停，執行正常的遊戲邏輯
        game_status = None
        current_level_name = current_player.current_map
        # 統一背景音樂切換
        static_last_map = getattr(play_bgm_for_map, "last_map", None)
        if static_last_map != current_level_name:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            play_bgm_for_map(current_level_name)
            play_bgm_for_map.last_map = current_level_name
        
        # 繪製與邏輯更新
        if current_player.current_map == "lobby":
            current_player.handle_input(keys); screen.blit(background, (0, 0)); current_player.draw(screen)
        
        elif current_player.current_map == "shop":
            # shop 的 handle_input (A/D/Enter) 已在事件迴圈中處理
            # render 負責繪製畫面
            shop.render(screen, current_player)

        elif current_player.current_map == "game_map":
            # ... (game_map 邏輯不變)
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
        
        elif current_player.current_map == "level1":
            game_status = level1_game.update_level1(screen, current_player)
        elif current_player.current_map == "level2":
            game_status = level2_game.update_level2(current_player, screen)
        elif current_player.current_map == "level3":
            game_status = level3_game.update_level3(screen, current_player)

        # 處理遊戲結束
        if game_status == "game_over":
            is_paused = False
            pass
        
    pygame.display.flip()
    clock.tick(60)

save_player_data_list(players)
pygame.quit()
sys.exit()