import pygame
import sys

# ---------------- SETTINGS ----------------
class Settings:
    def __init__(self):
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (20, 20, 40)

        self.ship_speed = 5
        self.bullet_speed = 30
        self.target_speed = 4

        self.speedup_scale = 1.1
        self.max_misses = 3

    def increase_speed(self):
        self.bullet_speed *= self.speedup_scale
        self.target_speed *= self.speedup_scale

    def reset_speed(self):
        self.ship_speed = 5
        self.bullet_speed = 7
        self.target_speed = 4


# ---------------- STATS ----------------
class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.score = 0
        self.misses = 0


# ---------------- BUTTON ----------------
class Button:
    def __init__(self, screen, msg):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 220, 70)
        self.rect.center = screen.get_rect().center
        self.color = (0, 200, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.msg = msg
        self.prep_msg()

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True,
                                          self.text_color, self.color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)


# ---------------- SHIP ----------------
class Ship:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(50, settings.screen_height // 2 - 40, 40, 80)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.settings.ship_speed

    def move_down(self):
        if self.rect.bottom < self.settings.screen_height:
            self.rect.y += self.settings.ship_speed

    def center_ship(self):
        self.rect.centery = self.settings.screen_height // 2

    def draw(self):
        pygame.draw.rect(self.screen, (0, 150, 255), self.rect)


# ---------------- BULLET ----------------
class Bullet:
    def __init__(self, screen, settings, ship_rect):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(ship_rect.right, ship_rect.centery - 2, 12, 4)

    def update(self):
        self.rect.x += self.settings.bullet_speed

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 0), self.rect)


# ---------------- TARGET ----------------
class Target:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(
            settings.screen_width - 80,
            settings.screen_height // 2 - 40,
            40, 80
        )
        self.direction = 1

    def update(self):
        self.rect.y += self.settings.target_speed * self.direction

        if self.rect.top <= 0 or self.rect.bottom >= self.settings.screen_height:
            self.direction *= -1

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)


# ---------------- GAME ----------------
class SideShooter:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Training Shooter")

        self.stats = GameStats(self.settings)
        self.ship = Ship(self.screen, self.settings)
        self.target = Target(self.screen, self.settings)
        self.bullets = []

        self.play_button = Button(self.screen, "Play")

        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()

    # ----------- START GAME -----------
    def start_game(self):
        self.settings.reset_speed()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.bullets.clear()
        self.ship.center_ship()
        self.target = Target(self.screen, self.settings)

    # ----------- EVENTS -----------
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.stats.game_active:
                    if self.play_button.rect.collidepoint(event.pos):
                        self.start_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.stats.game_active:
                    self.bullets.append(
                        Bullet(self.screen, self.settings, self.ship.rect))

    # ----------- UPDATE -----------
    def update_game(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.ship.move_up()
        if keys[pygame.K_DOWN]:
            self.ship.move_down()

        self.target.update()

        for bullet in self.bullets[:]:
            bullet.update()

            if bullet.rect.colliderect(self.target.rect):
                self.bullets.remove(bullet)
                self.stats.score += 1
                self.settings.increase_speed()

            elif bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)
                self.stats.misses += 1

        if self.stats.misses >= self.settings.max_misses:
            self.stats.game_active = False

    # ----------- DRAW -----------
    def update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.ship.draw()
            self.target.draw()

            for bullet in self.bullets:
                bullet.draw()

            score = self.font.render(
                f"Score: {self.stats.score}", True, (255, 255, 255))
            misses = self.font.render(
                f"Misses: {self.stats.misses}/3", True, (255, 100, 100))

            self.screen.blit(score, (20, 20))
            self.screen.blit(misses, (20, 60))

        else:
            self.play_button.draw()

        pygame.display.flip()

    # ----------- MAIN LOOP -----------
    def run_game(self):
        while True:
            self.clock.tick(60)
            self.check_events()

            if self.stats.game_active:
                self.update_game()

            self.update_screen()


if __name__ == "__main__":
    game = SideShooter()
    game.run_game()
