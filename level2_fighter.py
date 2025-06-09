import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 初始位置與設定
laser_x = 0
laser_y = 300
laser_width = 30
laser_height = 5
laser_speed = 10
laser_color = (255, 0, 0, 180)  # 半透明紅色

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 黑背景

    # 更新雷射位置（向右移動）
    laser_x += laser_speed

    # 建立雷射子彈（長條矩形）
    laser = pygame.Surface((laser_width, laser_height), pygame.SRCALPHA)
    pygame.draw.rect(laser, laser_color, (0, 0, laser_width, laser_height))

    # 繪製在目前座標
    screen.blit(laser, (laser_x, laser_y))

    pygame.display.flip()
    clock.tick(60)

    # 當雷射飛出畫面就停止（你也可以重設位置）
    if laser_x > 800:
        running = False

pygame.quit()