import sys
import pygame
from pygame.sprite import Sprite, Group


# ================= SETTINGS =================

class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 650
        self.bg_color = (10, 10, 40)

        self.ship_limit = 3
        self.speedup_scale = 1.2
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 4
        self.bullet_speed = 6
        self.alien_speed = 1.2
        self.fleet_drop_speed = 20
        self.fleet_direction = 1
        self.bullets_allowed = 4
        self.alien_points = 50

    def set_difficulty(self, level):
        self.initialize_dynamic_settings()

        if level == "easy":
            self.ship_speed = 5
            self.bullet_speed = 7
            self.alien_speed = 0.3
            self.bullets_allowed = 6

        elif level == "normal":
            self.ship_speed = 4
            self.bullet_speed = 6
            self.alien_speed = 0.5
            self.bullets_allowed = 4

        elif level == "hard":
            self.ship_speed = 3
            self.bullet_speed = 5
            self.alien_speed = 0.7
            self.bullets_allowed = 3

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


# ================= GAME STATS =================

class GameStats:
    def __init__(self):
        self.reset_stats()
        self.game_active = False
        self.high_score = self._load_high_score()

    def reset_stats(self):
        self.ships_left = 3
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        try:
            with open("highscore.txt") as f:
                return int(f.read())
        except:
            return 0


# ================= BUTTON =================

class Button:
    def __init__(self, ai_game, text, center):
        self.screen = ai_game.screen
        self.rect = pygame.Rect(0, 0, 200, 50)
        self.rect.center = center
        self.color = (0, 150, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        self.text_image = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.text_image, self.text_rect)


# ================= SHIP =================

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def draw(self):
        self.screen.blit(self.image, self.rect)


# ================= BULLET =================

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(0, 0, 4, 18)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)


# ================= ALIEN =================

class Alien(Sprite):
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


# ================= SCOREBOARD =================

class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.font = pygame.font.SysFont(None, 36)
        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        self.score_img = self.font.render(
            f"Score: {self.stats.score}", True, (255, 255, 255))
        self.score_rect = self.score_img.get_rect(topright=(980, 10))

    def prep_high(self):
        self.high_img = self.font.render(
            f"High: {self.stats.high_score}", True, (255, 255, 0))
        self.high_rect = self.high_img.get_rect(midtop=(500, 10))

    def prep_level(self):
        self.level_img = self.font.render(
            f"Level: {self.stats.level}", True, (255, 255, 255))
        self.level_rect = self.level_img.get_rect(topright=(980, 40))

    def prep_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + i * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def draw(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_img, self.high_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)


# ================= MAIN GAME =================

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
             self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats()
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = Group()
        self.aliens = Group()

        self.easy_button = Button(self, "Easy", (500, 300))
        self.normal_button = Button(self, "Normal", (500, 370))
        self.hard_button = Button(self, "Hard", (500, 440))

    # ---------- GAME LOOP ----------

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # ---------- EVENTS ----------

    def _check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._save_high_score()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.stats.game_active:
                    self._check_buttons(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _check_buttons(self, mouse_pos):
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.start_game("easy")
        elif self.normal_button.rect.collidepoint(mouse_pos):
            self.start_game("normal")
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self.start_game("hard")

    # ---------- START GAME ----------

    def start_game(self, level):
        self.settings.set_difficulty(level)
        self.stats.reset_stats()
        self.stats.game_active = True

        self.sb.prep_images()

        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center()

    # ---------- BULLETS ----------

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_collisions()

    def _check_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += \
                    self.settings.alien_points * len(aliens)

            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score

            self.sb.prep_images()

        if not self.aliens:
            self.start_new_level()

    # ---------- NEW LEVEL ----------

    def start_new_level(self):
        self.bullets.empty()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_images()
        self._create_fleet()

    # ---------- ALIENS ----------

    def _create_fleet(self):
        alien = Alien(self)
        alien_w = alien.rect.width
        alien_h = alien.rect.height

        available_x = self.settings.screen_width - 2 * alien_w
        num_x = available_x // (2 * alien_w)

        for row in range(3):
            for col in range(num_x):
                alien = Alien(self)
                alien.rect.x = alien_w + 2 * alien_w * col
                alien.rect.y = 100 + 2 * alien_h * row
                alien.x = float(alien.rect.x)
                self.aliens.add(alien)

    def _check_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for alien in self.aliens.sprites():
                    alien.rect.y += self.settings.fleet_drop_speed
                self.settings.fleet_direction *= -1
                break

    def _update_aliens(self):
        self._check_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    # ---------- SHIP HIT ----------

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_images()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center()
        else:
            self.stats.game_active = False

    # ---------- SAVE ----------

    def _save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.stats.high_score))

    # ---------- DRAW ----------

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.ship.draw()
            for bullet in self.bullets.sprites():
                bullet.draw()
            self.aliens.draw(self.screen)
            self.sb.draw()
        else:
            self.easy_button.draw()
            self.normal_button.draw()
            self.hard_button.draw()

        pygame.display.flip()


if __name__ == "__main__":
    AlienInvasion().run_game()
