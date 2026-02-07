import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дощ")

BLUE = (100, 100, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

drops = []
for _ in range(100):
    drops.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for d in drops:
        d[1] += 2
        if d[1] > HEIGHT:
            d[1] = 0
            d[0] = random.randint(0, WIDTH)

        pygame.draw.circle(screen, BLUE, d, 3)

    pygame.display.flip()

pygame.quit()
