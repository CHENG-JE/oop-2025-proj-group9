# main.py (修正版)
import pygame, os, sys, json
from player import Player
from lobby.log_in import show_login_screen
import lobby.shop as shop, lobby.game_map as game_map
import level1.level1_game as level1_game
import level2.level2_game as level2_game
import level3.level3_game as level3_game
import pause
import ui

# 音樂設定
pygame.mixer.init()

def play_bgm_for_map(map_name):
    bgm_files = {
        "lobby": os.path.join("assets", "music", "lobby.mp3"),
        "level1": os.path.join("assets", "music", "lev1.mp3"),
        "level2": os.path.join("assets", "music", "lev2.mp3"),
        "level3": os.path.join("assets", "music", "lev3.mp3"),
        "shop": os.path.join("assets", "music", "shop.mp3"),
        "game_map": os.path.join("assets", "music", "game_map.mp3")
    }
    current_bgm = getattr(play_bgm_for_map, "current_bgm", None)
    if map_name in bgm_files and current_bgm != map_name:
        pygame.mixer.music.load(bgm_files[map_name])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        play_bgm_for_map.current_bgm = map_name

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
current_player.rect.center = (400, 500) 
current_player.set_level_mode("lobby")

is_paused = False
running = True
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_player.current_map in ["level1", "level2", "level3"]:
                    is_paused = not is_paused
                elif current_player.current_map == "shop":
                    current_player.set_level_mode("lobby")
                    current_player.rect.center = (120, 415)

        if not is_paused:
            if current_player.current_map == "lobby":
                target_map = current_player.check_portal_trigger(event)
                if target_map == "exit":
                    running = False
                elif target_map:
                    if target_map == "game_map":
                        current_player.rect.center = (100, 305)
                    current_player.set_level_mode(target_map)
            elif current_player.current_map == "shop":
                shop.handle_events(event, current_player)
    
    if is_paused:
        action = pause.show(screen, current_player.current_map)
        if action == "continue": is_paused = False
        elif action == "restart":
            if current_player.current_map == "level1": level1_game.init_level1(current_player)
            if current_player.current_map == "level2": level2_game.init_level2(current_player)
            if current_player.current_map == "level3": level3_game.init_level3(current_player)
            is_paused = False
        elif action == "leave":
            current_player.set_level_mode("game_map")
            current_player.rect.center = (420, 180)
            is_paused = False
    else:
        current_player.update(platforms=level3_game.platform_group)
        current_player.handle_input(keys, 
                                    walls=level1_game.wall_group, 
                                    projectile_group=level3_game.player_projectile_group)
        
        play_bgm_for_map(current_player.current_map)
        
        game_status = None
        if current_player.current_map == "lobby":
            screen.blit(background, (0, 0))
            current_player.draw(screen)
            ui.draw_player_stats(screen, current_player)
        
        elif current_player.current_map == "shop":
            shop.render(screen, current_player)

        elif current_player.current_map == "game_map":
            game_map.render(screen, current_player)
            ui.draw_player_stats(screen, current_player)

            level1_zone = pygame.Rect(50, 475, 150, 40)
            level2_zone = pygame.Rect(400, 90, 100, 90)
            level3_zone = pygame.Rect(610, 80, 100, 50)
            
            font = pygame.font.SysFont(None, 36)
            prompt_text = font.render("Press Enter to start the game", True, (255, 255, 255))
            if any(zone.collidepoint(current_player.rect.center) for zone in [level1_zone, level2_zone, level3_zone]):
                screen.blit(prompt_text, (250, 550))
            
            if keys[pygame.K_RETURN]:
                if level1_zone.collidepoint(current_player.rect.center):
                    level1_game.init_level1(current_player)
                    current_player.set_level_mode("level1")
                elif level2_zone.collidepoint(current_player.rect.center):
                    level2_game.init_level2(current_player)
                    current_player.set_level_mode("level2")
                elif level3_zone.collidepoint(current_player.rect.center):
                    level3_game.init_level3(current_player)
                    current_player.set_level_mode("level3", boundaries=(50, 750))
        
        elif current_player.current_map == "level1":
            game_status = level1_game.update_level1(screen, current_player, keys)
        
        elif current_player.current_map == "level2":
            # === 修正：將 player 改為 current_player ===
            game_status = level2_game.update_level2(current_player, screen, keys)
            
        elif current_player.current_map == "level3":
            game_status = level3_game.update_level3(screen, current_player, keys)

        if game_status == "game_over":
            is_paused = False
        
    pygame.display.flip()
    clock.tick(60)

save_player_data_list(players)
pygame.quit()
sys.exit()