# win_or_lose.py (修正版)
import pygame
import sys

def display(screen, main_player, win, level_name):
    """
    顯示遊戲結束畫面，處理獎懲，並等待玩家輸入。
    """
    font_large = pygame.font.SysFont(None, 60)
    font_medium = pygame.font.SysFont(None, 40)
    font_small = pygame.font.SysFont(None, 30)
    
    level_return_pos = (420, 180)
    text1, text2_str = None, ""

    # 根據輸贏和關卡，設定文字與獎懲
    if win:
        text1 = font_large.render("You Win!", True, (0, 255, 0))
        if level_name == "level1":
            # === 修正：移除對 droplet 的依賴 ===
            text2_str = "You got $100 & 20 EXP"
            main_player.money += 100
            main_player.exp += 20
            # main_player 的血量就是最終血量，不需再同步
            level_return_pos = (120, 490)
        elif level_name == "level2":
            text2_str = "You got $1000 & 100 EXP"
            main_player.money += 1000
            if main_player.exp <= 900: main_player.exp += 100
            else: main_player.exp = 1000
            level_return_pos = (445, 125)
        elif level_name == "level3":
            # === 修正：移除對 archer 的依賴 ===
            text2_str = "You got $500"
            main_player.money += 500
            # main_player 的血量就是最終血量，不需再同步
            level_return_pos = (660, 110)
            
    else: # 失敗
        text1 = font_large.render("You were defeated!", True, (255, 0, 0))
        if level_name == "level1":
            text2_str = "You lose $20"
            main_player.money = max(0, main_player.money - 20)
            level_return_pos = (120, 490)
        elif level_name == "level2":
            text2_str = "You lose $100 & all EXP"
            main_player.money = max(0, main_player.money - 100)
            main_player.exp = 0
            level_return_pos = (460, 170)
        elif level_name == "level3":
            text2_str = "You lose $300"
            main_player.money = max(0, main_player.money - 300)
            level_return_pos = (660, 110)
        
        main_player.blood = 100 # 失敗後血量回滿

    text2 = font_medium.render(text2_str, True, (255, 255, 255))
    text3 = font_small.render("Press M to return to the game map", True, (255, 255, 255))
    
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    screen.blit(text1, (screen.get_width()//2 - text1.get_width()//2, screen.get_height()//2 - 60))
    screen.blit(text2, (screen.get_width()//2 - text2.get_width()//2, screen.get_height()//2))
    screen.blit(text3, (screen.get_width()//2 - text3.get_width()//2, screen.get_height()//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    waiting = False

    main_player.set_level_mode("game_map") # 統一使用 set_level_mode
    main_player.rect.center = level_return_pos