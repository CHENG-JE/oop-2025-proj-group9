# level1/level1_game.py
import pygame
import sys, os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .wall import HorizontalWall, VerticalWall
from .portal import Portal
from .lightning import Lightning
from .droplet import Droplet

# === 常數區 ===
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 20, 15
CELL_SIZE = SCREEN_WIDTH // GRID_WIDTH
ROUND_DURATION = 6 * 60 # 每回合 6 秒 (以幀為單位)

# === 全域物件 ===
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()

# === 場景物件 ===
droplet = None
portal = None
round_count = 1
maze_timer = 0
lev1_bg = pygame.transform.scale(pygame.image.load("assets/background/level1.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))


# === 函式區 ===
def setup_new_round():
    """建立一個全新的迷宮，並重新生成傳送門"""
    h_walls, v_walls = generate_maze()
    
    # 確保玩家當前位置是安全的
    if droplet:
        player_grid_x = droplet.rect.centerx // CELL_SIZE
        player_grid_y = droplet.rect.centery // CELL_SIZE
        for y in range(player_grid_y - 1, player_grid_y + 2):
            for x in range(player_grid_x - 1, player_grid_x + 2):
                if 0 <= y < GRID_HEIGHT + 1 and 0 <= x < GRID_WIDTH: h_walls[y][x] = False
                if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH + 1: v_walls[y][x] = False
    
    create_walls_from_grid(h_walls, v_walls)
    
    # === 改正：無條件重新生成 Portal ===
    # 移除所有 if 判斷，讓 portal 每回合都換位置
    spawn_portal(h_walls, v_walls)

def generate_maze():
    # (此函式不變)
    h_walls = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)]
    v_walls = [[False for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            is_border = (y == 0 or y == GRID_HEIGHT)
            if is_border or random.random() < 0.5: h_walls[y][x] = True
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH + 1):
            is_border = (x == 0 or x == GRID_WIDTH)
            if is_border or random.random() < 0.5: v_walls[y][x] = True
    return h_walls, v_walls

def create_walls_from_grid(h_walls, v_walls):
    # (此函式不變)
    wall_group.empty()
    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            if h_walls[y][x]: wall_group.add(HorizontalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH + 1):
            if v_walls[y][x]: wall_group.add(VerticalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))

def spawn_portal(h_walls, v_walls):
    # (此函式不變)
    portal_group.empty()
    valid_spawns = []
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            is_in_rings = (x in [1, 2, GRID_WIDTH-3, GRID_WIDTH-2] or y in [1, 2, GRID_HEIGHT-3, GRID_HEIGHT-2])
            is_open = not (h_walls[y][x] or h_walls[y+1][x] or v_walls[y][x] or v_walls[y][x+1])
            if is_in_rings and is_open: valid_spawns.append((x, y))
    if valid_spawns:
        spawn_pos = random.choice(valid_spawns)
        global portal; portal = Portal(spawn_pos[0] * CELL_SIZE, spawn_pos[1] * CELL_SIZE, CELL_SIZE)
        portal_group.add(portal)

def init_level1(main_player):
    global droplet, round_count, maze_timer
    for group in [wall_group, portal_group, player_group, lightning_group]: group.empty()
        
    round_count = 1
    # === 改正：設定回合時間為 6 秒 ===
    maze_timer = ROUND_DURATION

    droplet = Droplet(start_pos=(380, 280), cell_size=CELL_SIZE)
    droplet.money = main_player.money; droplet.exp = main_player.exp
    droplet.max_blood = main_player.max_blood; droplet.blood = main_player.blood
    player_group.add(droplet)
    
    setup_new_round()

def update_level1(screen, main_player):
    global maze_timer, round_count
    
    if not droplet or droplet.blood <= 0:
        main_player.blood = droplet.blood # 同步最終血量
        return "lose"
    if pygame.sprite.spritecollide(droplet, portal_group, False):
        main_player.blood = droplet.blood # 同步最終血量
        return "win"
    
    maze_timer -= 1
    if maze_timer <= 0:
        round_count += 1
        
        # 呼叫新函式來重置場景
        setup_new_round()
        
        # === 改正：重置計時器為 6 秒 ===
        maze_timer = ROUND_DURATION
        
        lightning = Lightning(droplet.rect.center)
        lightning_group.add(lightning)
        droplet.take_damage(20)
        
    keys = pygame.key.get_pressed()
    player_group.update(keys, wall_group)
    lightning_group.update()
    
    screen.blit(lev1_bg, (0, 0))
    wall_group.draw(screen)
    portal_group.draw(screen)
    player_group.draw(screen)
    lightning_group.draw(screen)
    
    droplet.draw_ui(screen)
    font = pygame.font.SysFont(None, 36)
    round_text = font.render(f"Round: {round_count}", True, (255, 255, 255))
    screen.blit(round_text, (SCREEN_WIDTH - round_text.get_width() - 20, 20))
    return None