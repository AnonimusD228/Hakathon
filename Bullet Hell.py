import pygame
import random
import sys
import math


class BulletHell:
    def __init__(self, width=640, height=480, energy=0):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bullet Hell")

        # Colors
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Player
        self.player_size = 40
        self.player_speed = 5

        # Beam properties
        self.beam_speed = 5
        self.beam_interval = 800
        self.beams = []

        # Game state
        self.energy = energy
        self.game_time = 10000  # survive 10 seconds

        # Fonts
        self.font = pygame.font.SysFont("consolas", 28)

    def create_player(self):
        return pygame.Rect(self.WIDTH // 2, self.HEIGHT - 60, self.player_size, self.player_size)

    def spawn_beam(self, player):
        x = random.randint(0, self.WIDTH)
        y = 0
        dx = player.centerx - x + random.randint(-50, 50)
        dy = player.centery - y
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        dx /= length
        dy /= length
        dx *= self.beam_speed
        dy *= self.beam_speed
        return {"rect": pygame.Rect(x, y, 10, 10), "dx": dx, "dy": dy}

    def draw_window(self, player, beams, start_time, game_over, win):
        self.WIN.fill(self.BLACK)
        pygame.draw.rect(self.WIN, self.GREEN, player)
        for b in beams:
            pygame.draw.rect(self.WIN, self.RED, b["rect"])
        timer_text = self.font.render(
            f"Time Left: {max(0, (self.game_time - (pygame.time.get_ticks() - start_time)) // 1000)}", True,
            self.YELLOW)
        self.WIN.blit(timer_text, (10, 10))
        energy_text = self.font.render(f"Energy: {self.energy}", True, self.GREEN)
        self.WIN.blit(energy_text, (10, 40))
        if game_over:
            msg = "YOU SURVIVED! +150 ENERGY" if win else "HIT! -50 ENERGY"
            msg_text = self.font.render(msg, True, self.WHITE)
            self.WIN.blit(msg_text,
                          (self.WIDTH // 2 - msg_text.get_width() // 2, self.HEIGHT // 2 - msg_text.get_height() // 2))
        pygame.display.update()

    def run(self):
        player = self.create_player()
        self.beams.clear()
        beam_timer = pygame.time.get_ticks()
        start_time = pygame.time.get_ticks()
        game_over = False
        win = False

        running = True
        while running:
            dt = self.clock.tick(self.FPS)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if not game_over:
                if keys[pygame.K_LEFT] and player.left > 0:
                    player.x -= self.player_speed
                if keys[pygame.K_RIGHT] and player.right < self.WIDTH:
                    player.x += self.player_speed
                if keys[pygame.K_UP] and player.top > 0:
                    player.y -= self.player_speed
                if keys[pygame.K_DOWN] and player.bottom < self.HEIGHT:
                    player.y += self.player_speed

            # Spawn beams
            if not game_over and now - beam_timer > self.beam_interval:
                beam_timer = now
                self.beams.append(self.spawn_beam(player))

            # Move beams
            if not game_over:
                for b in self.beams:
                    b["rect"].x += b["dx"]
                    b["rect"].y += b["dy"]

            # Collision
            if not game_over:
                for b in self.beams:
                    if player.colliderect(b["rect"]):
                        game_over = True
                        win = False
                        self.energy -= 50
                        break

            # Check win
            if not game_over and now - start_time >= self.game_time:
                game_over = True
                win = True
                self.energy += 150

            self.draw_window(player, self.beams, start_time, game_over, win)

            # Restart after hit or win
            if game_over:
                pygame.time.delay(1500)
                player = self.create_player()
                self.beams.clear()
                beam_timer = pygame.time.get_ticks()
                start_time = pygame.time.get_ticks()
                game_over = False
                win = False
