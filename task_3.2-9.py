import pygame
import sys

pygame.init()

# ---------- SETTINGS ----------
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Навчальна стрілянина")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)

FONT = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# ---------- GAME STATE ----------
game_active = False
misses = 0
MAX_MISSES = 3

# ---------- SHIP ----------
ship = pygame.Rect(40, HEIGHT // 2 - 25, 40, 50)
ship_speed = 5

# ---------- TARGET ----------
target = pygame.Rect(WIDTH - 60, 100, 30, 80)
target_speed = 3
target_speed_start = 3
target_dir = 1

# ---------- BULLET ----------
bullet = None
bullet_speed = 8

# ---------- BUTTON ----------
play_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 30, 160, 60)


def draw_play_button():
    pygame.draw.rect(screen, GREEN, play_button)
    text = FONT.render("PLAY", True, BLACK)
    screen.blit(text, text.get_rect(center=play_button.center))


def reset_game():
    global misses, bullet, game_active, target_speed
    misses = 0
    bullet = None
    target.y = 100
    target_speed = target_speed_start
    game_active = True


# ---------- MAIN LOOP ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active and play_button.collidepoint(event.pos):
                reset_game()

        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE and bullet is None:
                bullet = pygame.Rect(ship.right, ship.centery - 5, 10, 10)

    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_UP] and ship.top > 0:
            ship.y -= ship_speed
        if keys[pygame.K_DOWN] and ship.bottom < HEIGHT:
            ship.y += ship_speed

    # ---------- UPDATE ----------
    if game_active:
        # target movement
        target.y += target_speed * target_dir
        if target.top <= 0 or target.bottom >= HEIGHT:
            target_dir *= -1

        # bullet movement
        if bullet:
            bullet.x += bullet_speed
            if bullet.left > WIDTH:
                bullet = None
                misses += 1

        # collision
        if bullet and bullet.colliderect(target):
            bullet = None
            target_speed += 1  # ⬆ speed increases

        # game over
        if misses >= MAX_MISSES:
            game_active = False

    # ---------- DRAW ----------
    screen.fill(WHITE)

    if game_active:
        pygame.draw.rect(screen, BLUE, ship)
        pygame.draw.rect(screen, RED, target)
        if bullet:
            pygame.draw.rect(screen, BLACK, bullet)

        miss_text = FONT.render(f"Misses: {misses}/3", True, BLACK)
        screen.blit(miss_text, (10, 10))
    else:
        draw_play_button()

    pygame.display.flip()
    clock.tick(60)
