import pygame
import sys

# ініціалізація
pygame.init()

# розміри екрана
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Задача 5. Бічна стрілянина")

# FPS
clock = pygame.time.Clock()
FPS = 60

# кольори
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# ===== КОРАБЕЛЬ =====
ship_image = pygame.image.load("rocket.bmp").convert_alpha()
ship_width = 50
ship_height = 40
ship_image = pygame.transform.scale(ship_image, (ship_width, ship_height))

ship_x = 20
ship_y = HEIGHT // 2 - ship_height // 2
ship_speed = 5

# ===== КУЛІ =====
bullets = []
bullet_width = 10
bullet_height = 4
bullet_speed = 8

# головний цикл
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # постріл
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = ship_x + ship_width
                bullet_y = ship_y + ship_height // 2 - bullet_height // 2
                bullets.append([bullet_x, bullet_y])

    # керування кораблем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= ship_speed
    if keys[pygame.K_DOWN] and ship_y < HEIGHT - ship_height:
        ship_y += ship_speed

    # рух куль
    for bullet in bullets[:]:
        bullet[0] += bullet_speed
        if bullet[0] > WIDTH:
            bullets.remove(bullet)

    # малювання
    screen.fill(BLACK)

    # корабель
    screen.blit(ship_image, (ship_x, ship_y))

    # кулі
    for bullet in bullets:
        pygame.draw.rect(
            screen,
            RED,
            (bullet[0], bullet[1], bullet_width, bullet_height)
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
