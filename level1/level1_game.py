# level1/level1_game.py
import pygame
import sys, os
import random

# 確保可以從父目錄導入模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 從新檔案中導入類別
from level1.wall import Wall
from level1.portal import Portal
from level1.lighting import Lighting
from level1.droplet import Droplet

# === 常數區 ===
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 40, 30
CELL_SIZE = SCREEN_WIDTH // GRID_WIDTH

# === 全域物件 (Sprite Groups) ===
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
lighting_group = pygame.sprite.Group()

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
    grid_data = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            is_border = (x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1)
            if is_border or random.random() < 0.25: # 25% 的機率生成牆壁
                grid_data[y][x] = True
                wall_group.add(Wall(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))
    return grid_data

def spawn_portal(grid_data):
    portal_group.empty()
    
    # 找出所有在外兩圈，且不是牆壁的位置
    valid_spawns = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            is_in_outer_rings = (x in [1, 2, GRID_WIDTH - 2, GRID_WIDTH - 3] or 
                                 y in [1, 2, GRID_HEIGHT - 2, GRID_HEIGHT - 3])
            if is_in_outer_rings and not grid_data[y][x]:
                valid_spawns.append((x, y))
    
    if valid_spawns:
        spawn_pos = random.choice(valid_spawns)
        global portal
        portal = Portal(spawn_pos[0] * CELL_SIZE, spawn_pos[1] * CELL_SIZE, CELL_SIZE)
        portal_group.add(portal)

def init_level1(main_player):
    global droplet, round_count, maze_timer, portal_timer
    
    # 清空所有群組
    for group in [wall_group, portal_group, player_group, lighting_group]:
        group.empty()
        
    # 初始化變數
    round_count = 1
    maze_timer = 4 * 60 # 4秒
    portal_timer = 28 * 60 # 28秒

    # 建立迷宮和傳送門
    grid = generate_maze()
    spawn_portal(grid)

    # 建立玩家
    droplet = Droplet(start_pos=(CELL_SIZE * 1.5, CELL_SIZE * 1.5), cell_size=CELL_SIZE)
    droplet.money = main_player.money
    droplet.exp = main_player.exp
    droplet.max_blood = main_player.max_blood
    droplet.blood = main_player.blood
    player_group.add(droplet)

def update_level1(screen, main_player):
    global maze_timer, portal_timer, round_count
    
    # 遊戲結束判斷
    if not droplet or droplet.blood <= 0:
        handle_game_over(screen, main_player, win=False)
        return
    if pygame.sprite.spritecollide(droplet, portal_group, False):
        handle_game_over(screen, main_player, win=True)
        return

    # --- 更新計時器 ---
    maze_timer -= 1
    if maze_timer <= 0:
        round_count += 1
        grid = generate_maze()
        spawn_portal(grid) # 迷宮重置時，傳送門也重置
        portal_timer = 28 * 60
        maze_timer = 4 * 60
        # 產生閃電
        lighting = Lighting(droplet.rect.center)
        lighting_group.add(lighting)
        droplet.take_damage(20)

    portal_timer -= 1
    if portal_timer <= 0:
        # 重新生成傳送門需要 grid data，但我們沒有儲存
        # 為了簡化，我們讓它和迷宮一起重置
        portal_timer = 28 * 60
        
    # --- 更新物件 ---
    keys = pygame.key.get_pressed()
    player_group.update(keys, wall_group)
    lighting_group.update()
    
    # --- 繪製所有內容 ---
    screen.blit(lev1_bg, (0, 0))
    wall_group.draw(screen)
    portal_group.draw(screen)
    player_group.draw(screen)
    lighting_group.draw(screen)
    
    # UI
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