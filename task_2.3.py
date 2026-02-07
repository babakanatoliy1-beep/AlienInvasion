import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Краплі")

BLUE = (100, 100, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

drops = []
for x in range(0, WIDTH, 30):
    for y in range(0, HEIGHT, 60):
        drops.append([x, y])

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for d in drops:
        d[1] += 1
        pygame.draw.circle(screen, BLUE, d, 3)

        if d[1] > HEIGHT:
            d[1] = HEIGHT + 10

    pygame.display.flip()

pygame.quit()
