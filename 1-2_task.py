import pygame
import sys

WIDTH = 800
HEIGHT = 600
BLUE = (0, 150, 255)


class Player:
    def __init__(self, image_path, screen):
        self.screen = screen
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(BLUE)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def draw(self):
        self.screen.blit(self.image, self.rect)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue sky")

clock = pygame.time.Clock()

player = Player("hero.bmp", screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)
    player.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
