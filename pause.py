# pause.py
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

# === 新增：所有關卡的規則文字 ===
# 使用字典來存放，key 是關卡名稱，value 是規則文字列表
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
        "Defeated enemies may drop items that grant EXP."
    ],
    "level3": [
        "A/D: Move Left/Right | SPACE: Jump",
        "J: Attack (Archery)",
        "Goal: Defeat the boss.",
        "Evade its beams and shockwaves."
    ]
}


# --- 繪圖函式 ---
def draw_menu(screen, selected_index):
    # (此函式不變)
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

# === 改正：讓規則畫面可以顯示對應關卡的規則 ===
def show_rules_screen(screen, level_name):
    font = pygame.font.SysFont(None, 40)
    # 從 RULES 字典中，根據關卡名稱獲取對應的規則文字
    rules_text = RULES.get(level_name, ["No rules found for this level."])
    
    # 固定的返回提示
    footer_text = "=== Press ESC to return to the pause menu ==="
    
    screen.blit(pause_bg, (0, 0))
    
    # 繪製關卡規則
    for i, line in enumerate(rules_text):
        text_surf = font.render(line, True, (0, 0, 0))  
        text_rect = text_surf.get_rect(center=(400, 200 + i * 50))
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

# === 改正：主函式現在會接收 level_name ===
def show(screen, level_name):
    selected_index = 0
    clock = pygame.time.Clock()

    while True:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "continue"
                if event.key == pygame.K_w: selected_index = (selected_index - 1 + len(BUTTON_TEXTS)) % len(BUTTON_TEXTS)
                if event.key == pygame.K_s: selected_index = (selected_index + 1) % len(BUTTON_TEXTS)
                if event.key == pygame.K_RETURN:
                    action = BUTTON_TEXTS[selected_index].lower()
                    # 如果是 menu，直接在這裡處理，而不是返回 main.py
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
        
        # 滑鼠懸停效果
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(BUTTON_RECTS):
            if rect.collidepoint(mouse_pos): selected_index = i; break

        # 繪圖
        draw_menu(screen, selected_index)
        pygame.display.flip()
        clock.tick(60)