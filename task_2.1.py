import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Зірки")

star = pygame.image.load("star.png")
star = pygame.transform.scale(star, (30, 30))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x in range(0, 600, 40):
        for y in range(0, 400, 40):
            screen.blit(star, (x, y))

    pygame.display.flip()

pygame.quit()
