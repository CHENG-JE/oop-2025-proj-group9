# pause.py (修正版)
import pygame
import sys

# --- 初始化與資源載入 ---
pygame.font.init()
try:
    pause_bg = pygame.image.load("assets/background/pause.jpeg").convert()
    pause_bg = pygame.transform.scale(pause_bg, (800, 600))
except pygame.error:
    pause_bg = pygame.Surface((800, 600), pygame.SRCALPHA); pause_bg.fill((10, 10, 30, 200))

# --- 按鈕設定 ---
BUTTON_TEXTS = ["Continue", "Restart", "Leave", "Menu"]
BUTTON_RECTS = [pygame.Rect(270, 140 + i * 80, 260, 50) for i in range(len(BUTTON_TEXTS))]

# === 所有關卡的規則文字 ===
RULES = {
    "level1": [
        "W/A/S/D: Move Up/Left/Down/Right",
        "Goal: Reach the portal within 12 seconds.",
        "The maze resets every round, ",
        "and you will be struck by lightning."
    ],
    "level2": [
        "W/A/S/D: Move Up/Left/Down/Right",
        "Goal: Defeat 40 enemy planes.",
        "Bonus: Heal 20 HP for every 10 kills.",
        "Eat the yellow blocks to grant 10 EXP."
    ],
    "level3": [
        "A/D: Move Left/Right | SPACE: Jump",
        "ENTER: Attack",
        "Goal: Defeat the boss.",
        "Evade its beams and shockwaves."
    ]
}


# --- 繪圖函式 ---
def draw_menu(screen, selected_index):
    screen.blit(pause_bg, (0, 0))
    font = pygame.font.SysFont(None, 50)
    mouse_pos = pygame.mouse.get_pos()
    for i, text in enumerate(BUTTON_TEXTS):
        rect = BUTTON_RECTS[i]
        if i == selected_index or rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (150, 150, 200), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 0), rect, 4, border_radius=10)
        else:
            pygame.draw.rect(screen, (100, 100, 150), rect, border_radius=10)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def show_rules_screen(screen, level_name):
    font = pygame.font.SysFont(None, 40)
    rules_text = RULES.get(level_name, ["No rules found for this level."])
    footer_text = "=== Press ESC to return to the pause menu ==="
    
    screen.blit(pause_bg, (0, 0))
    
    # === 修正：新增灰色背景板 ===
    # 1. 計算背景板的尺寸和位置
    panel_width = 600
    # 根據文字行數和間距計算高度，並增加一些邊距
    panel_height = len(rules_text) * 50 + 40 
    panel_x = (screen.get_width() - panel_width) / 2
    # 讓面板的頂部從 150px 開始
    panel_y = 150 
    
    # 2. 建立一個帶有透明度的 Surface 作為背景板
    panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surf.fill((50, 50, 50, 200)) # 半透明的深灰色
    
    # 3. 繪製背景板
    screen.blit(panel_surf, (panel_x, panel_y))
    
    # 繪製關卡規則文字
    for i, line in enumerate(rules_text):
        # === 修正：將文字顏色從 (0, 0, 0) 改為 (255, 255, 255) ===
        text_surf = font.render(line, True, (255, 255, 255))
        # 文字的位置基於背景板的位置來計算
        text_rect = text_surf.get_rect(center=(400, panel_y + 40 + i * 50))
        screen.blit(text_surf, text_rect)
        
    # 繪製返回提示
    footer_font = pygame.font.SysFont(None, 30)
    footer_surf = footer_font.render(footer_text, True, (200, 200, 200))
    footer_rect = footer_surf.get_rect(center=(400, 500))
    screen.blit(footer_surf, footer_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

def show(screen, level_name):
    selected_index = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "continue"
                if event.key == pygame.K_w or event.key == pygame.K_UP: 
                    selected_index = (selected_index - 1 + len(BUTTON_TEXTS)) % len(BUTTON_TEXTS)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN: 
                    selected_index = (selected_index + 1) % len(BUTTON_TEXTS)
                if event.key == pygame.K_RETURN:
                    action = BUTTON_TEXTS[selected_index].lower()
                    if action == "menu":
                        show_rules_screen(screen, level_name)
                    else:
                        return action

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(BUTTON_RECTS):
                    if rect.collidepoint(event.pos):
                        action = BUTTON_TEXTS[i].lower()
                        if action == "menu":
                            show_rules_screen(screen, level_name)
                        else:
                            return action
        
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(BUTTON_RECTS):
            if rect.collidepoint(mouse_pos):
                selected_index = i
                break

        draw_menu(screen, selected_index)
        pygame.display.flip()
        clock.tick(60)