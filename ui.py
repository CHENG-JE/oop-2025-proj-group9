# ui.py
import pygame

def draw_player_stats(screen, player):
    """繪製玩家的基礎狀態 (金錢、血量、經驗)"""
    font = pygame.font.SysFont(None, 28)
    white_color = (255, 255, 255)
    
    # 確保所有玩家物件都有這些屬性
    money = getattr(player, 'money', 0)
    blood = getattr(player, 'blood', 0)
    max_blood = getattr(player, 'max_blood', 100)
    exp = getattr(player, 'exp', 0)
    
    money_text = font.render(f"Money: ${money}", True, white_color)
    hp_text = font.render(f"HP: {int(blood)}/{max_blood}", True, white_color)
    exp_text = font.render(f"EXP: {exp}", True, white_color)
    
    screen.blit(money_text, (20, 20))
    screen.blit(hp_text, (20, 45))
    screen.blit(exp_text, (20, 70))

def draw_level_hud(screen, level_name, **kwargs):
    """繪製特定關卡的額外 HUD 資訊"""
    font = pygame.font.SysFont(None, 36)
    white_color = (255, 255, 255)
    
    if level_name == "level1":
        round_count = kwargs.get('round_count', 1)
        text_surf = font.render(f"Round: {round_count}", True, white_color)
        screen.blit(text_surf, (screen.get_width() - text_surf.get_width() - 20, 20))
        
    elif level_name == "level2":
        kills = kwargs.get('kills', 0)
        text_surf = font.render(f"Kills: {kills}/40", True, (255, 255, 0))
        screen.blit(text_surf, (screen.get_width() - text_surf.get_width() - 120, 20)) # x 座標微調

    elif level_name == "level3":
        enemies_left = kwargs.get('enemies_left', 0)
        text_surf = font.render(f"Enemies left: {enemies_left}", True, (255, 255, 0))
        screen.blit(text_surf, (screen.get_width() - text_surf.get_width() - 150, 20))