import pygame
import sys

# 載入圖片 (只在需要時載入一次)
try:
    pause_bg = pygame.image.load("assets/background/pause.jpeg")
    pause_bg = pygame.transform.scale(pause_bg, (800, 600))
except pygame.error:
    pause_bg = pygame.Surface((800, 600)); pause_bg.fill((10, 10, 30))

# 按鈕文字和位置
button_texts = ["Continue", "Restart", "Leave", "Menu"]
button_rects = []
for i, text in enumerate(button_texts):
    # 將按鈕垂直排列在畫面中央
    rect = pygame.Rect(270, 140 + i * 80, 260, 50) # 按鈕大小為 260x50
    button_rects.append(rect)

def draw_menu(screen):
    """繪製暫停選單的背景和按鈕"""
    screen.blit(pause_bg, (0, 0))
    font = pygame.font.SysFont(None, 50)
    
    for i, text in enumerate(button_texts):
        # 繪製按鈕背景
        pygame.draw.rect(screen, (100, 100, 150), button_rects[i], border_radius=10)
        # 繪製文字
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=button_rects[i].center)
        screen.blit(text_surf, text_rect)

def handle_input():
    """處理暫停選單中的輸入，返回一個動作指令"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 在暫停選單中也要能關閉遊戲
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # 按 ESC 也可以繼續遊戲
            if event.key == pygame.K_ESCAPE:
                return "continue"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 左鍵點擊
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        # 返回對應的按鈕指令 (小寫)
                        return button_texts[i].lower()
    return None # 如果沒有任何操作，返回 None

def show_rules_screen(screen):
    """顯示規則畫面 (目前為 placeholder)"""
    font = pygame.font.SysFont(None, 40)
    rules_text = [
        "This is the game rules screen.",
        "Currently under construction.",
        "",
        "Press ESC to return to the pause menu."
    ]
    screen.blit(pause_bg, (0, 0))
    for i, line in enumerate(rules_text):
        text_surf = font.render(line, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(400, 250 + i * 50))
        screen.blit(text_surf, text_rect)
    
    pygame.display.flip()
    
    # 等待玩家按 ESC 返回
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
