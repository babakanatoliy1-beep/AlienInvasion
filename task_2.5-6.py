import pygame
import random

# ініціалізація
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("М'яч — кінець гри")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# гравець
player = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 30, 80, 15)
player_speed = 4   # повільний рух

# м'яч
ball = pygame.Rect(random.randint(0, WIDTH - 20), 0, 20, 20)
ball_speed = 2     # повільне падіння

misses = 0
MAX_MISSES = 3
game_over = False

running = True
while running:
    clock.tick(30)  # уповільнення всієї гри

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # рух м'яча
        ball.y += ball_speed

        # зловили м'яч
        if ball.colliderect(player):
            ball.x = random.randint(0, WIDTH - 20)
            ball.y = 0

        # промах
        elif ball.top > HEIGHT:
            misses += 1
            ball.x = random.randint(0, WIDTH - 20)
            ball.y = 0

            if misses >= MAX_MISSES:
                game_over = True

    # малювання
    screen.fill(BLACK)

    if game_over:
        text = font.render("Гру завершено", True, WHITE)
        screen.blit(text, (200, 170))
    else:
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.ellipse(screen, WHITE, ball)

        info = font.render(f"Промахи: {misses}", True, WHITE)
        screen.blit(info, (10, 10))

    pygame.display.flip()

pygame.quit()
