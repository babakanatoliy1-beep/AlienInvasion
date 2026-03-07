import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")

clock = pygame.time.Clock()

# ---------- звуки ----------
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
alien_hit_sound = pygame.mixer.Sound("sounds/alien_hit.wav")
ship_hit_sound = pygame.mixer.Sound("sounds/ship_hit.wav")
start_sound = pygame.mixer.Sound("sounds/start.wav")

# ---------- зображення ----------
ship_img = pygame.image.load("ship.bmp")
alien_img = pygame.image.load("alien.bmp")

# ---------- рекорд ----------
try:
    with open("high_score.txt") as f:
        high_score = int(f.read())
except:
    high_score = 0

font = pygame.font.SysFont(None, 36)

MAX_BULLETS = 5


# ---------- корабель ----------
class Ship:

    def __init__(self):

        self.image = ship_img
        self.rect = self.image.get_rect()

        self.rect.midbottom = (WIDTH//2, HEIGHT-20)

        self.speed = 5

        self.moving_left = False
        self.moving_right = False

    def update(self):

        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed

        if self.moving_right and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


# ---------- куля ----------
class Bullet:

    def __init__(self, ship):

        self.rect = pygame.Rect(0,0,4,15)
        self.rect.midtop = ship.rect.midtop

        self.speed = 7

    def update(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen,(255,255,0),self.rect)


# ---------- прибулець ----------
class Alien:

    def __init__(self,x,y):

        self.image = alien_img
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 2

    def update(self):

        self.rect.x += self.speed

        # відбиття від стін
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed *= -1
            self.rect.y += 20

    def draw(self):
        screen.blit(self.image,self.rect)


# ---------- кнопка ----------
class Button:

    def __init__(self,text,y):

        self.rect = pygame.Rect(0,0,200,50)
        self.rect.center = (WIDTH//2,y)

        self.text = font.render(text,True,(255,255,255))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen,(0,150,0),self.rect)
        screen.blit(self.text,self.text_rect)

    def clicked(self,pos):
        return self.rect.collidepoint(pos)


# ---------- створення флоту ----------
def create_fleet():

    aliens = []

    for row in range(3):
        for col in range(6):

            x = 100 + col*100
            y = 60 + row*80

            aliens.append(Alien(x,y))

    return aliens


# ---------- запуск гри ----------
def start_game(level):

    global aliens, bullets, score, lives, game_active

    start_sound.play()

    bullets = []
    aliens = create_fleet()

    score = 0
    lives = 3

    game_active = True

    if level == "easy":
        speed = 1
    elif level == "normal":
        speed = 2
    else:
        speed = 3

    for alien in aliens:
        alien.speed = speed


ship = Ship()

bullets = []
aliens = create_fleet()

score = 0
lives = 3

game_active = False

play_button = Button("Play",300)
easy_button = Button("Easy",360)
normal_button = Button("Normal",420)
hard_button = Button("Hard",480)


# ---------- головний цикл ----------
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            with open("high_score.txt","w") as f:
                f.write(str(high_score))

            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                ship.moving_left = True

            if event.key == pygame.K_RIGHT:
                ship.moving_right = True

            if event.key == pygame.K_SPACE and game_active:

                # обмеження куль
                if len(bullets) < MAX_BULLETS:

                    bullet = Bullet(ship)
                    bullets.append(bullet)

                    shoot_sound.play()

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                ship.moving_left = False

            if event.key == pygame.K_RIGHT:
                ship.moving_right = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos()

            if play_button.clicked(mouse):
                game_active = False

            if easy_button.clicked(mouse):
                start_game("easy")

            if normal_button.clicked(mouse):
                start_game("normal")

            if hard_button.clicked(mouse):
                start_game("hard")


    # ---------- логіка гри ----------
    if game_active:

        ship.update()

        for bullet in bullets[:]:

            bullet.update()

            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for alien in aliens:
            alien.update()

        # зіткнення
        for bullet in bullets[:]:
            for alien in aliens[:]:

                if bullet.rect.colliderect(alien.rect):

                    alien_hit_sound.play()

                    bullets.remove(bullet)
                    aliens.remove(alien)

                    score += 10

                    if score > high_score:
                        high_score = score

                    break

        # якщо прибульці дійшли вниз
        for alien in aliens:

            if alien.rect.bottom > HEIGHT:

                ship_hit_sound.play()

                lives -= 1

                aliens = create_fleet()

                if lives <= 0:
                    game_active = False

                break

        if len(aliens) == 0:
            aliens = create_fleet()

    # ---------- малювання ----------
    screen.fill((240, 240, 140))

    ship.draw()

    for bullet in bullets:
        bullet.draw()

    for alien in aliens:
        alien.draw()

    score_text = font.render(f"Score: {score}",True,(255,255,255))
    high_text = font.render(f"High Score: {high_score}",True,(255,255,255))
    lives_text = font.render(f"Lives: {lives}",True,(255,255,255))

    screen.blit(score_text,(10,10))
    screen.blit(high_text,(10,40))
    screen.blit(lives_text,(10,70))

    if not game_active:

        play_button.draw()
        easy_button.draw()
        normal_button.draw()
        hard_button.draw()

    pygame.display.flip()
    clock.tick(60)
