import pygame
import sys

# ---------- НАЛАШТУВАННЯ ----------
WIDTH = 800
HEIGHT = 600
BLUE = ("black")
SPEED = 5


# ---------- КЛАС РАКЕТИ ----------
class Rocket:
    def __init__(self, image_path, screen):
        self.screen = screen
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(BLUE)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED

        # не виходити за межі екрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        self.screen.blit(self.image, self.rect)


# ---------- ГОЛОВНА ПРОГРАМА ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ракета")

clock = pygame.time.Clock()

rocket = Rocket("rocket.bmp", screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    rocket.move(keys)

    screen.fill(BLUE)
    rocket.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
