#Я змінив фон на чорний в минулій задачі
import pygame
import sys

# ініціалізація PyGame
pygame.init()

# розміри вікна
WIDTH = 600
HEIGHT = 400

# створення вікна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Задача 4. Клавіші")

# кольори
BLACK = (0, 0, 0)

# головний цикл
running = True
while running:
    for event in pygame.event.get():
        # вихід з програми
        if event.type == pygame.QUIT:
            running = False

        # натискання клавіші
        if event.type == pygame.KEYDOWN:
            print("event.key =", event.key)

    # чорний фон
    screen.fill(BLACK)
    pygame.display.flip()

# завершення роботи
pygame.quit()
sys.exit()
