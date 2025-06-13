# level1/level1_game.py
import pygame
import sys, os
import random

# 確保可以從父目錄導入模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 從新檔案中導入類別
from level1.wall import HorizontalWall, VerticalWall
from level1.portal import Portal
from level1.lightning import Lightning
from level1.droplet import Droplet

# === 常數區 ===
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 40, 30
CELL_SIZE = SCREEN_WIDTH // GRID_WIDTH

# === 全域物件 (Sprite Groups) ===
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()

# === 場景物件 ===
droplet = None
portal = None
round_count = 1
maze_timer = 0
portal_timer = 0
lev1_bg = pygame.transform.scale(pygame.image.load("assets/background/level1.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# === 函式區 ===
def generate_maze():
    wall_group.empty()
    # 建立兩個網格，分別存儲水平和垂直的牆壁狀態
    h_walls = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)]
    v_walls = [[False for _ in range(GRID_WIDTH + 1)] for _ in range(GRID_HEIGHT)]

    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            # 建立最外圈的水平牆壁
            is_top_or_bottom_border = (y == 0 or y == GRID_HEIGHT)
            if is_top_or_bottom_border or random.random() < 0.2:
                h_walls[y][x] = True

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH + 1):
            # 建立最外圈的垂直牆壁
            is_left_or_right_border = (x == 0 or x == GRID_WIDTH)
            if is_left_or_right_border or random.random() < 0.2:
                v_walls[y][x] = True
                
    return h_walls, v_walls

def create_walls_from_grid(h_walls, v_walls):
    wall_group.empty()
    # 根據網格數據建立牆壁物件
    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            if h_walls[y][x]:
                wall_group.add(HorizontalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH + 1):
            if v_walls[y][x]:
                wall_group.add(VerticalWall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))

def spawn_portal(h_walls, v_walls):
    portal_group.empty()
    valid_spawns = []
    for y in range(1, GRID_HEIGHT - 1): # 確保不在最頂和最底
        for x in range(1, GRID_WIDTH - 1): # 確保不在最左和最右
            is_in_outer_rings = (x in [1, 2, GRID_WIDTH - 2, GRID_WIDTH - 3] or 
                                 y in [1, 2, GRID_HEIGHT - 2, GRID_HEIGHT - 3])
            # 檢查該格子四周是否都沒有牆
            is_open = not (h_walls[y][x] or h_walls[y+1][x] or v_walls[y][x] or v_walls[y][x+1])
            if is_in_outer_rings and is_open:
                valid_spawns.append((x, y))
    
    if valid_spawns:
        spawn_pos = random.choice(valid_spawns)
        global portal
        portal = Portal(spawn_pos[0] * CELL_SIZE, spawn_pos[1] * CELL_SIZE, CELL_SIZE)
        portal_group.add(portal)

def init_level1(main_player):
    global droplet, round_count, maze_timer, portal_timer, grid_data
    for group in [wall_group, portal_group, player_group, lightning_group]: group.empty()
        
    round_count = 1; maze_timer = 4 * 60; portal_timer = 28 * 60

    h_walls, v_walls = generate_maze()
    
    # 清空出生點區域的牆壁
    start_grid_x = 380 // CELL_SIZE
    start_grid_y = 280 // CELL_SIZE
    for y in range(start_grid_y - 1, start_grid_y + 2):
        for x in range(start_grid_x - 1, start_grid_x + 2):
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                h_walls[y][x] = False
                h_walls[y+1][x] = False
                v_walls[y][x] = False
                v_walls[y][x+1] = False
    
    create_walls_from_grid(h_walls, v_walls)
    spawn_portal(h_walls, v_walls)

    droplet = Droplet(start_pos=(380, 280), cell_size=CELL_SIZE)
    droplet.money = main_player.money; droplet.exp = main_player.exp
    droplet.max_blood = main_player.max_blood; droplet.blood = main_player.blood
    player_group.add(droplet)

def update_level1(screen, main_player):
    global maze_timer, portal_timer, round_count
    
    if not droplet or droplet.blood <= 0: handle_game_over(screen, main_player, win=False); return
    if pygame.sprite.spritecollide(droplet, portal_group, False): handle_game_over(screen, main_player, win=True); return

    maze_timer -= 1
    if maze_timer <= 0:
        round_count += 1
        h_walls, v_walls = generate_maze()
        create_walls_from_grid(h_walls, v_walls)
        spawn_portal(h_walls, v_walls)
        portal_timer = 28 * 60
        maze_timer = 4 * 60
        lightning = Lightning(droplet.rect.center); lightning_group.add(lightning)
        droplet.take_damage(20)

    portal_timer -= 1
    if portal_timer <= 0:
        # 由於 portal 生成依賴網格數據，我們讓它在迷宮重置時一起重置即可
        portal_timer = 28 * 60
        
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

def handle_game_over(screen, main_player, win):
    # (此函式與 Level 3 基本相同)
    if win:
        main_player.money += 100
        main_player.exp += 20
    else:
        main_player.money = max(0, main_player.money - 20)
    main_player.blood = droplet.blood

    # (等待畫面與返回邏輯)
    font = pygame.font.SysFont(None, 60)
    if win: text1 = font.render("You Win!", True, (0, 255, 0)); text2_str = "You got $100 & 20 EXP"
    else: text1 = font.render("You were lost...", True, (255, 0, 0)); text2_str = "You lose $20"
    text2 = pygame.font.SysFont(None, 40).render(text2_str, True, (255, 255, 255))
    text3 = pygame.font.SysFont(None, 30).render("Press any key to return to map...", True, (255, 255, 255))
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2 - 60))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2))
    screen.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, SCREEN_HEIGHT//2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN: waiting = False
    
    main_player.reset_image()
    main_player.current_map = "game_map"
    main_player.rect.center = (420, 180)