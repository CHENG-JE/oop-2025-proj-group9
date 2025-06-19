import pygame
import numpy as np
import ui
# 載入背景
background = pygame.image.load("assets/background/shop.png")
background = pygame.transform.scale(background, (800, 600))

# 載入商品圖片並縮小
item_images = [
    pygame.transform.scale(pygame.image.load("assets/items/gift.png"), (200, 200)),
    pygame.transform.scale(pygame.image.load("assets/items/blood.png"), (200, 200)),
    pygame.transform.scale(pygame.image.load("assets/items/xp_book.png"), (200, 200)),
]

# 商品區塊位置（選取框位置）
item_rects = [
    pygame.Rect(130, 240, 200, 200),
    pygame.Rect(290, 240, 200, 200),
    pygame.Rect(450, 240, 200, 200),
]

selected_index = 0
purchase_message = ""

def render(screen, player):
    global purchase_message
    screen.blit(background, (0, 0))

    # 設定字型與大小
    font = pygame.font.SysFont(None, 50)
    prices = ["$100", "$150", "$200"]

    # 畫出商品圖片並加上選取框與金額
    for i, rect in enumerate(item_rects):
        screen.blit(item_images[i], rect.topleft)
        if i == selected_index:
            pygame.draw.rect(screen, (255, 255, 0), rect.inflate(-60, -60), 4)

        # 顯示金額文字在商品下方
        price_surface = font.render(prices[i], True, (255, 255, 255))
        price_rect = price_surface.get_rect(center=(rect.centerx, rect.bottom + 35))
        screen.blit(price_surface, price_rect)

    # 顯示右上角提示文字
    esc_font = pygame.font.SysFont(None, 30)
    esc_text = esc_font.render("Press ESC to return to lobby", True, (255, 255, 255))
    screen.blit(esc_text, (520, 10))

    # === 改正：呼叫 ui 模組來繪製狀態 ===
    # 移除舊的 money_font, blood_font, exp_font 等程式碼
    ui.draw_player_stats(screen, player)

    # 顯示購買訊息
    if purchase_message:
        msg_font = pygame.font.SysFont(None, 40)
        msg_surface = msg_font.render(purchase_message, True, (255, 255, 255))
        msg_rect = msg_surface.get_rect(center=(400, 550))
        screen.blit(msg_surface, msg_rect)

def handle_events(event, player):
    global selected_index
    global purchase_message
    purchase_sound = pygame.mixer.Sound("assets/music/purchase_sound_effect.mp3")
    no_cash_sound = pygame.mixer.Sound("assets/music/no_enough_money.mp3")
    wrong_sound = pygame.mixer.Sound("assets/music/wrong.mp3")
    if event.type == pygame.KEYDOWN:
        print(f"Key pressed: {event.key}")  # 除錯列印
        if event.key == pygame.K_a:
            selected_index = (selected_index - 1) % 3
        elif event.key == pygame.K_d:
            selected_index = (selected_index + 1) % 3
        elif event.key == pygame.K_RETURN:
            item_prices = [100,150,200]
            #item_names = ["Gift","Blood","Experience book"]
            price = item_prices[selected_index]

            if player.money >= price:
                # 根據購買項目給予不同訊息
                if selected_index == 0:
                    purchase_sound.play()
                    player.money -= price
                    choice = np.random.rand()
                    if choice > 0.8:
                        player.max_blood += 50
                        player.blood = player.max_blood
                        purchase_message = "Bought Gift: Max HP +50 & Fully healed!"
                    elif choice > 0.5:
                        player.max_blood += 20
                        player.blood = player.max_blood
                        purchase_message = "Bought Gift: Max HP +20 & Fully healed!"
                    elif choice > 0.3:
                        player.blood = 100
                        purchase_message = "Bought Gift: HP restored to 100."
                    else:
                        player.blood = 50
                        player.exp = 0
                        purchase_message = "Bought Gift: Bad luck... HP=50 and Reset everything."
                        
                elif selected_index == 1:
                    if player.blood == player.max_blood:
                        purchase_message = "HP already full, Purchase failed"
                        wrong_sound.play()
                    elif player.blood + 50 >= player.max_blood:
                        purchase_sound.play()
                        player.money -= price
                        player.blood = player.max_blood
                        purchase_message = "HP fully restored"
                    else:
                        purchase_sound.play()
                        player.money -= price
                        player.blood += 50
                        purchase_message = "Bought Blood Pack: HP +50"

                elif selected_index == 2:
                    if player.exp == 1000:
                        purchase_message = "Max EXP, Purchase failed"
                        wrong_sound.play()
                    elif player.exp +50 > 1000:
                        purchase_sound.play()
                        player.money -= price
                        purchase_message = "Max EXP"
                    else:
                        purchase_sound.play()
                        purchase_message = "Bought XP Book: EXP +50"
                        player.money -= price
                    player.exp += 50
                    player.exp = min(player.exp , 1000)

            else:
                purchase_message = "No enough cash"
                no_cash_sound.play()

            # 已根據購買項目給予效果，避免重複處理

        elif event.key == pygame.K_ESCAPE:
            player.current_map = "lobby"

        # 顯示當前選取框的座標
        print("Selected item rect position:", item_rects[selected_index].topleft, "center:", item_rects[selected_index].center)

"""
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    class DummyPlayer:
        def __init__(self):
            self.money = 500
        def draw(self, screen):
            pass

    player = DummyPlayer()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_events(event, player)

        render(screen, player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
"""