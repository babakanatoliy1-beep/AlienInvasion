import sys
import pygame


# ---------------- SETTINGS ----------------
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 200)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.bullet_speed = 7
        self.alien_speed = 2
        self.fleet_drop_speed = 20
        self.fleet_direction = 1
        self.bullet_allowed = 5
        self.alien_points = 50

    def set_difficulty(self, level):
        if level == "easy":
            self.ship_speed = 6
            self.bullet_speed = 8
            self.alien_speed = 0.5
            self.bullet_allowed = 7

        elif level == "normal":
            self.ship_speed = 5
            self.bullet_speed = 7
            self.alien_speed = 1
            self.bullet_allowed = 5

        elif level == "hard":
            self.ship_speed = 4
            self.bullet_speed = 6
            self.alien_speed = 1.5
            self.bullet_allowed = 3


# ---------------- GAME STATS ----------------
class GameStats:
    def __init__(self):
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.ships_left = 3
        self.score = 0


# ---------------- BUTTON ----------------
class Button:
    def __init__(self, ai_game, msg, center):
        self.screen = ai_game.screen
        self.width, self.height = 200, 50
        self.button_color = (0, 180, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


# ---------------- SHIP ----------------
class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen.get_rect().right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def center_ship(self):
        self.rect.midbottom = self.screen.get_rect().midbottom

    def draw(self):
        self.screen.blit(self.image, self.rect)


# ---------------- BULLET ----------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(0, 0, 5, 15)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)


# ---------------- ALIEN ----------------
class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0


# ---------------- MAIN GAME ----------------
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.font = pygame.font.SysFont(None, 40)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.easy_button = Button(self, "Easy", (600, 300))
        self.normal_button = Button(self, "Normal", (600, 380))
        self.hard_button = Button(self, "Hard", (600, 460))

    def _create_fleet(self):
        self.aliens.empty()
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        for row in range(5):
            for alien_number in range(number_aliens_x):
                alien = Alien(self)
                alien.rect.x = alien_width + 2 * alien_width * alien_number
                alien.rect.y = alien_height + 2 * alien_height * row
                alien.x = float(alien.rect.x)
                self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for alien in self.aliens.sprites():
                    alien.rect.y += self.settings.fleet_drop_speed
                self.settings.fleet_direction *= -1
                break

    def _ship_hit(self):
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()

                self._check_fleet_edges()
                self.aliens.update()

                collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, True
                )

                if collisions:
                    for aliens in collisions.values():
                        self.stats.score += self.settings.alien_points * len(aliens)

                if pygame.sprite.spritecollideany(self.ship, self.aliens):
                    self._ship_hit()

                self._check_aliens_bottom()

                if not self.aliens:
                    self._create_fleet()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.stats.game_active:
                    pos = pygame.mouse.get_pos()
                    if self.easy_button.rect.collidepoint(pos):
                        self._start_game("easy")
                    elif self.normal_button.rect.collidepoint(pos):
                        self._start_game("normal")
                    elif self.hard_button.rect.collidepoint(pos):
                        self._start_game("hard")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE and self.stats.game_active:
                    if len(self.bullets) < self.settings.bullet_allowed:
                        self.bullets.add(Bullet(self))

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _start_game(self, level):
        self.settings.initialize_dynamic_settings()
        self.settings.set_difficulty(level)
        self.stats.reset_stats()
        self.stats.game_active = True
        self.bullets.empty()
        self._create_fleet()
        pygame.mouse.set_visible(False)

    def _draw_hearts(self):
        for i in range(self.stats.ships_left):
            heart = pygame.Rect(20 + i * 40, 20, 30, 30)
            pygame.draw.rect(self.screen, (255, 0, 0), heart)

    def _draw_score(self):
        score_image = self.font.render(
            f"Score: {self.stats.score}", True, (255, 255, 255)
        )
        self.screen.blit(score_image, (950, 20))

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.ship.draw()

            for bullet in self.bullets.copy():
                bullet.draw()
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            self.aliens.draw(self.screen)
            self._draw_hearts()
            self._draw_score()
        else:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    AlienInvasion().run_game()
