import pygame
import sys
import random
from settings import *

class NumGame:
    def __init__(self, width=screen_width, height=screen_height, energy=0):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Radioactive Lab Puzzle")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (50, 50, 50)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.grid_size = 3
        self.tile_size = self.WIDTH // self.grid_size
        self.EMPTY = None
        self.energy = energy

        self.font = pygame.font.SysFont("consolas", 28)
        self.puzzle = self.create_puzzle()

    def create_puzzle(self):
        tiles = [i for i in range(1, self.grid_size * self.grid_size)]
        tiles.append(self.EMPTY)
        random.shuffle(tiles)
        puzzle = []
        for i in range(self.grid_size):
            row = tiles[i * self.grid_size:(i + 1) * self.grid_size]
            puzzle.append(row)
        return puzzle

    def find_empty(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.puzzle[y][x] == self.EMPTY:
                    return x, y
        return None

    def draw_puzzle(self):
        self.WIN.fill(self.BLACK)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                val = self.puzzle[y][x]
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if val != self.EMPTY:
                    pygame.draw.rect(self.WIN, self.GREEN, rect)
                    text = pygame.font.SysFont("consolas", 40).render(str(val), True, self.BLACK)
                    self.WIN.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
                pygame.draw.rect(self.WIN, self.WHITE, rect, 3)
        energy_text = self.font.render(f"Energy: {self.energy}", True, self.YELLOW)
        self.WIN.blit(energy_text, (10, 10))
        pygame.display.update()

    def is_solved(self):
        correct = list(range(1, self.grid_size * self.grid_size))
        correct.append(self.EMPTY)
        flat = [self.puzzle[y][x] for y in range(self.grid_size) for x in range(self.grid_size)]
        return flat == correct

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    ex, ey = self.find_empty()
                    if event.key == pygame.K_LEFT and ex < self.grid_size - 1:
                        self.puzzle[ey][ex], self.puzzle[ey][ex + 1] = self.puzzle[ey][ex + 1], self.puzzle[ey][ex]
                    if event.key == pygame.K_RIGHT and ex > 0:
                        self.puzzle[ey][ex], self.puzzle[ey][ex - 1] = self.puzzle[ey][ex - 1], self.puzzle[ey][ex]
                    if event.key == pygame.K_UP and ey < self.grid_size - 1:
                        self.puzzle[ey][ex], self.puzzle[ey + 1][ex] = self.puzzle[ey + 1][ex], self.puzzle[ey][ex]
                    if event.key == pygame.K_DOWN and ey > 0:
                        self.puzzle[ey][ex], self.puzzle[ey - 1][ex] = self.puzzle[ey - 1][ex], self.puzzle[ey][ex]

            self.draw_puzzle()

            if self.is_solved():
                self.energy += 200
                font = pygame.font.SysFont("consolas", 36)
                msg = font.render("PUZZLE SOLVED! +200 ENERGY", True, self.YELLOW)
                self.WIN.blit(msg, (self.WIDTH // 2 - msg.get_width() // 2, self.HEIGHT // 2 - msg.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(2000)
                running = False
