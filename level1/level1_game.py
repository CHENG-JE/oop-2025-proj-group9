# level1/level1_game.py (修正版)
import pygame
import sys, os
import random
import win_or_lose
import ui

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .wall import HorizontalWall, VerticalWall
from .portal import Portal
from .lightening import Lightning

# === 常數區 ===
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 20, 15
CELL_SIZE = SCREEN_WIDTH // GRID_WIDTH
ROUND_DURATION = 15 * 60 

# === 全域物件 ===
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()

# === 場景物件 ===
portal = None
round_count = 1
maze_timer = 0
lev1_bg = pygame.transform.scale(pygame.image.load("assets/background/level1.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def show_game_title(screen):
    font = pygame.font.SysFont("arial", 50)
    text_surface = font.render("Moving Maze!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # 等待3秒

def setup_new_round(main_player):
    """建立一個全新的迷宮，並重新生成傳送門"""
    h_walls, v_walls = generate_maze()
    
    if main_player:
        player_grid_x = main_player.rect.centerx // CELL_SIZE
        player_grid_y = main_player.rect.centery // CELL_SIZE
        for y in range(player_grid_y - 1, player_grid_y + 2):
            for x in range(player_grid_x - 1, player_grid_x + 2):
                if 0 <= y < GRID_HEIGHT + 1 and 0 <= x < GRID_WIDTH: h_walls[y][x] = False
                if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH + 1: v_walls[y][x] = False
    
    create_walls_from_grid(h_walls, v_walls)
    spawn_portal()

def generate_maze():
    h_walls = [[True for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)]
    v_walls = [[True for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)]
    
    visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    stack = [(random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))]
    visited[stack[0][1]][stack[0][0]] = True

    while stack:
        x, y = stack[-1]
        neighbors = []
        if x > 0 and not visited[y][x-1]: neighbors.append('L')
        if x < GRID_WIDTH - 1 and not visited[y][x+1]: neighbors.append('R')
        if y > 0 and not visited[y-1][x]: neighbors.append('U')
        if y < GRID_HEIGHT - 1 and not visited[y+1][x]: neighbors.append('D')

        if neighbors:
            direction = random.choice(neighbors)
            if direction == 'L':
                v_walls[y][x] = False
                nx, ny = x-1, y
            elif direction == 'R':
                v_walls[y][x+1] = False
                nx, ny = x+1, y
            elif direction == 'U':
                h_walls[y][x] = False
                nx, ny = x, y-1
            elif direction == 'D':
                h_walls[y+1][x] = False
                nx, ny = x, y+1
            
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()
            
    # === 修正：強制建立邊界牆壁 ===
    # 上下邊界
    for x in range(GRID_WIDTH):
        h_walls[0][x] = True
        h_walls[GRID_HEIGHT][x] = True
    # 左右邊界
    for y in range(GRID_HEIGHT):
        v_walls[y][0] = True
        v_walls[y][GRID_WIDTH] = True
        
    return h_walls, v_walls

def create_walls_from_grid(h_walls, v_walls):
    wall_group.empty()
    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            if h_walls[y][x]: wall_group.add(HorizontalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH + 1):
            if v_walls[y][x]: wall_group.add(VerticalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))

def spawn_portal():
    portal_group.empty()
    valid_spawns = []
    
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            is_in_rings = (x in [1, 2, GRID_WIDTH-3, GRID_WIDTH-2] or y in [1, 2, GRID_HEIGHT-3, GRID_HEIGHT-2])
            
            if is_in_rings:
                valid_spawns.append((x, y))

    if valid_spawns:
        spawn_pos = random.choice(valid_spawns)
        global portal
        portal_x = spawn_pos[0] * CELL_SIZE + (CELL_SIZE - 30) / 2
        portal_y = spawn_pos[1] * CELL_SIZE + (CELL_SIZE - 30) / 2
        portal = Portal(portal_x, portal_y, CELL_SIZE)
        portal_group.add(portal)

def init_level1(main_player):
    show_game_title(pygame.display.get_surface())

    main_player.shoot_timer = 0


    global round_count, maze_timer, portal
    portal = None
    for group in [wall_group, portal_group, lightning_group]: group.empty()
    
    round_count = 1
    maze_timer = ROUND_DURATION

    # 設定玩家初始位置
    main_player.rect.center = (100, 305)
    main_player.hitbox.center = main_player.rect.center

    setup_new_round(main_player)

def update_level1(screen, main_player, keys):
    global maze_timer, round_count, portal
    
    if main_player.blood <= 0:
        win_or_lose.display(screen, main_player, False, "level1")
        return "game_over"
        
    # === 修正：改用 hitbox 進行碰撞判斷 ===
    if portal and portal.rect.colliderect(main_player.hitbox):
        win_or_lose.display(screen, main_player, True, "level1")
        return "game_over"
    
    maze_timer -= 1
    if maze_timer <= 0:
        round_count += 1
        setup_new_round(main_player)
        maze_timer = ROUND_DURATION
        
        lightning = Lightning(main_player.rect.center)
        lightning_group.add(lightning)
        main_player.take_damage(20)
        
    lightning_group.update()
    
    screen.blit(lev1_bg, (0, 0))
    wall_group.draw(screen)
    portal_group.draw(screen)
    main_player.draw(screen)
    lightning_group.draw(screen)
    
    ui.draw_player_stats(screen, main_player)
    ui.draw_level_hud(screen, "level1", round_count=round_count, time_left=maze_timer)
    
    return None