# win_or_lose.py
import pygame
import sys

def display(screen, main_player, win, level_name):
    """
    顯示遊戲結束畫面，處理獎懲，並等待玩家輸入。
    """
    font_large = pygame.font.SysFont(None, 60)
    font_medium = pygame.font.SysFont(None, 40)
    font_small = pygame.font.SysFont(None, 30)
    
    level_return_pos = (420, 180) # 預設返回點
    text1, text2_str = None, ""

    # 根據輸贏和關卡，設定文字與獎懲
    if win:
        text1 = font_large.render("You Win!", True, (0, 255, 0))
        if level_name == "level1":
            from level1.level1_game import droplet
            text2_str = "You got $100 & 20 EXP"
            main_player.money += 100; main_player.exp += 20
            if droplet: main_player.blood = droplet.blood
            level_return_pos = (120, 490)
        elif level_name == "level2":
            text2_str = "You got $1000 & 100 EXP"
            main_player.money += 1000
            if main_player.exp <= 900: main_player.exp += 100
            else: main_player.exp = 1000
            level_return_pos = (445, 125)
        elif level_name == "level3":
            from level3.level3_game import archer
            text2_str = "You got $500"
            main_player.money += 500
            if archer: main_player.blood = archer.blood
            level_return_pos = (660, 110)
            
    else: # 失敗
        text1 = font_large.render("You were defeated!", True, (255, 0, 0))
        if level_name == "level1":
            text2_str = "You lose $20"; main_player.money = max(0, main_player.money - 20)
            level_return_pos = (120, 490)
        elif level_name == "level2":
            text2_str = "You lose $100 & all EXP"; main_player.money = max(0, main_player.money - 100); main_player.exp = 0
            level_return_pos = (460, 170)
        elif level_name == "level3":
            text2_str = "You lose $300"; main_player.money = max(0, main_player.money - 300)
            level_return_pos = (660, 110)
        
        main_player.blood = 100

    # === 改正 1：修改提示文字 ===
    text2 = font_medium.render(text2_str, True, (255, 255, 255))
    text3 = font_small.render("Press M to return to the game map", True, (255, 255, 255))
    
    # 用一個半透明的遮罩讓背景變暗，突顯文字
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    screen.blit(text1, (screen.get_width()//2 - text1.get_width()//2, screen.get_height()//2 - 60))
    screen.blit(text2, (screen.get_width()//2 - text2.get_width()//2, screen.get_height()//2))
    screen.blit(text3, (screen.get_width()//2 - text3.get_width()//2, screen.get_height()//2 + 50))
    pygame.display.flip()

    # === 改正 2：修改按鍵判斷 ===
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 只在按下 "M" 鍵時才結束等待
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    waiting = False

    # 設定返回地圖的狀態
    main_player.current_map = "game_map"
    main_player.reset_image()
    main_player.rect.center = level_return_pos