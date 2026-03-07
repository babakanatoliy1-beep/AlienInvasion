import sys
import random
import pygame
from pygame.sprite import Sprite, Group

# ================= SETTINGS =================

class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 650
        self.bg_color = (240, 240, 240)

        self.ship_speed = 2
        self.bullet_speed = 7
        self.alien_speed = 1
        self.fleet_drop_speed = 25

        self.bullets_allowed = 5
        self.alien_fire_rate = 60
        self.ship_limit = 3

    def set_difficulty(self, level):
        if level == "easy":
            self.alien_speed = 0.2
            self.alien_fire_rate = 800
            self.ship_limit = 5
        elif level == "normal":
            self.alien_speed = 0.4
            self.alien_fire_rate = 750
            self.ship_limit = 3
        elif level == "hard":
            self.alien_speed = 0.6
            self.alien_fire_rate = 700
            self.ship_limit = 2

# ================= STATS =================

class GameStats:
    def __init__(self):
        self.game_active = False
        self.level = 1
        self.ships_left = 3

# ================= SHIP =================

class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
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

# ================= BULLETS =================

class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, 4, 16)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 255), self.rect)

class AlienBullet(Sprite):
    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, 4, 14)
        self.rect.midbottom = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self):
        self.y += 0.2
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

# ================= SHELTER BLOCK =================

class Block(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 15))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

# ================= ALIEN =================

class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

    def update(self, direction):
        self.x += self.settings.alien_speed * direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

# ================= GAME =================

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()
        self.blocks = Group()

        self.fleet_direction = 1
        self.fire_timer = 0
        self.font = pygame.font.SysFont(None, 42)

    # ================= MAIN LOOP =================

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
            self._update_screen()

    # ================= EVENTS =================

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.key == pygame.K_1 and not self.stats.game_active:
                    self._start_game("easy")
                elif event.key == pygame.K_2 and not self.stats.game_active:
                    self._start_game("normal")
                elif event.key == pygame.K_3 and not self.stats.game_active:
                    self._start_game("hard")

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    # ================= GAME LOGIC =================

    def _start_game(self, difficulty):
        self.settings.set_difficulty(difficulty)
        self.stats.ships_left = self.settings.ship_limit
        self.stats.level = 1
        self.stats.game_active = True

        self.bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()
        self.blocks.empty()

        self._create_fleet()
        self._create_shelters()
        self.ship.center()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        pygame.sprite.groupcollide(self.bullets, self.blocks, True, True)

        if not self.aliens:
            self.stats.level += 1
            self._create_fleet()

    def _update_alien_bullets(self):
        self.fire_timer += 1
        if self.fire_timer > self.settings.alien_fire_rate and self.aliens:
            alien = random.choice(self.aliens.sprites())
            self.alien_bullets.add(AlienBullet(self, alien))
            self.fire_timer = 0

        self.alien_bullets.update()

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        pygame.sprite.groupcollide(self.alien_bullets, self.blocks, True, True)

        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

    def _update_aliens(self):
        edge_hit = False
        for alien in self.aliens:
            if alien.check_edges():
                edge_hit = True
                break

        if edge_hit:
            self.fleet_direction *= -1
            for alien in self.aliens:
                alien.rect.y += self.settings.fleet_drop_speed

        for alien in self.aliens:
            alien.update(self.fleet_direction)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        self.stats.ships_left -= 1
        if self.stats.ships_left <= 0:
            self.stats.game_active = False
        else:
            self.ship.center()
            self.alien_bullets.empty()

    # ================= CREATE =================

    def _create_fleet(self):
        for row in range(3):
            for col in range(8):
                alien = Alien(self)
                alien.rect.x = 100 + col * 100
                alien.rect.y = 80 + row * 70
                alien.x = alien.rect.x
                self.aliens.add(alien)

    def _create_shelters(self):
        y = self.settings.screen_height - 150
        for x in (200, 450, 700):
            for row in range(4):
                for col in range(6):
                    self.blocks.add(Block(x + col * 20, y + row * 15))

    # ================= DRAW =================

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.ship.draw()
            for b in self.bullets: b.draw()
            for b in self.alien_bullets: b.draw()
            self.aliens.draw(self.screen)
            self.blocks.draw(self.screen)

            lives = self.font.render(f"Lives: {self.stats.ships_left}", True, (255,255,255))
            level = self.font.render(f"Level: {self.stats.level}", True, (255,255,0))
            self.screen.blit(lives, (20, 20))
            self.screen.blit(level, (20, 60))
        else:
            txt = self.font.render("1-EASY   2-NORMAL   3-HARD", True, (255,255,255))
            self.screen.blit(txt, (280, 300))

        pygame.display.flip()

# ================= RUN =================

if __name__ == "__main__":
    AlienInvasion().run_game()
