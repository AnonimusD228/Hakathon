import pygame
import sys
import random
import math  # <-- standard math module
from currency import neutrons
global neutrons
class Mathgame:
    def start(self, width=1200, height=800, neutrons=0):
        pygame.init()
        self.pressed=False
        self.WIDTH, self.HEIGHT = width, height
        self.WIN = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Atomic Puzzle - Ordered Rods!")

        # Colors
        self.BLACK = (10, 10, 10)
        self.WHITE = (230, 230, 230)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 240, 120)
        self.GRAY = (120, 120, 120)
        self.GRAY_DARK = (60, 60, 60)
        self.BLUE = (0, 120, 255)
        self.BLUE_GLOW = (0, 150, 255)
        self.RED = (255, 80, 80)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Numbers and operators
        self.numbers = [1,2,3,4,5]
        self.operators = ['+', '-', '*', '/']

        # Rods
        self.rods = []
        self.selected = None
        self.offset_x = 0
        self.offset_y = 0
        self.rod_images=[
            pygame.transform.scale(pygame.image.load('enemy1.png'),[55,65]),
            pygame.transform.scale(pygame.image.load('enemy2.png'), [55, 65]),
            pygame.transform.scale(pygame.image.load('enemy3.png'), [55, 65]),
        ]

        # Reactor core
        self.core_x = self.WIDTH//2
        self.core_y = self.HEIGHT//2
        self.core_radius = 85

        # Attempt button
        self.attempt_button = pygame.Rect(self.WIDTH//2 - 80,
                                          self.core_y + self.core_radius + 30,
                                          160, 50)

        self.font = pygame.font.SysFont("consolas", 30)
        self.smallfont = pygame.font.SysFont("consolas", 20)
        self.pulse = 0  # reactor pulse animation

        # List to track **order of rods placed in reactor**
        self.ordered_rods = []

        self.new_puzzle()

    # --------------------------------------------------------------------
    # Setup rods: numbers + operators
    # --------------------------------------------------------------------
    def new_puzzle(self):
        self.rods.clear()
        self.selected = None
        self.ordered_rods.clear()

        # Pick 5 random numbers
        self.current_numbers = [random.choice(self.numbers) for _ in range(5)]

        # Pick 4 random operators
        self.current_ops = [random.choice(self.operators) for _ in range(4)]

        # Always solvable target
        self.target = self.generate_target(self.current_numbers, self.current_ops)

        # Place rods on the right side
        vertical_space = self.HEIGHT - 120
        # rod_height = vertical_space // 9 - 10
        # rod_height = max(40, min(rod_height, 70))
        rod_height = 130

        y = 130
        x=self.WIDTH - 85

        # Number rods
        for num in self.current_numbers:
            rect = pygame.Rect(x, y, 110, rod_height)
            self.rods.append({"type":"number", "value": num, "rect": rect})
            y += rod_height + 10
            if y>=self.HEIGHT-rod_height:
                y=130
                x-=85

        # Operator rods
        for op in self.current_ops:
            rect = pygame.Rect(x, y, 55, rod_height)
            self.rods.append({"type":"operator", "value": op, "rect": rect})
            y += rod_height + 10
            if y >= self.HEIGHT - rod_height:
                y = 130
                x -= 85

    # --------------------------------------------------------------------
    # Generate target equation
    # --------------------------------------------------------------------
    def generate_target(self, nums, ops):
        total = nums[0]
        for i, n in enumerate(nums[1:]):
            op = ops[i % len(ops)]
            if op == '+':
                total += n
            elif op == '-':
                total -= n
            elif op == '*':
                total *= n
            elif op == '/':
                if n != 0:
                    total //= n
        return total

    # --------------------------------------------------------------------
    # Draw reactor
    # --------------------------------------------------------------------
    def draw_reactor(self):
        self.pulse += 0.05
        pulse_add = int(6 * math.sin(self.pulse))

        pygame.draw.circle(self.WIN, (0, 80, 180), (self.core_x,
self.core_y), self.core_radius + 25 + pulse_add)
        pygame.draw.circle(self.WIN, (0, 50, 140), (self.core_x,
self.core_y), self.core_radius + 15)
        pygame.draw.circle(self.WIN, (40, 40, 40), (self.core_x,
self.core_y), self.core_radius + 8)
        pygame.draw.circle(self.WIN, (80, 80, 80), (self.core_x,
self.core_y), self.core_radius + 4)
        pygame.draw.circle(self.WIN, self.BLUE_GLOW, (self.core_x, self.core_y),
                           self.core_radius - 5 +
int(math.sin(self.pulse * 2) * 3))

    # --------------------------------------------------------------------
    # Draw rod outside reactor
    # --------------------------------------------------------------------
    def draw_rod(self, rod):
        r = rod["rect"]

        if rod["type"]=='number':
            self.WIN.blit(self.rod_images[rod["value"]%3],r)
        else:
            color = self.GRAY if rod["type"]=="number" else self.YELLOW
            pygame.draw.rect(self.WIN, color, r, border_radius=14)
            pygame.draw.line(self.WIN, self.WHITE, (r.x + 4, r.y + 4),(r.x + 4, r.bottom - 4), 2)
            pygame.draw.line(self.WIN, self.GRAY_DARK, (r.right - 4, r.y +4), (r.right - 4, r.bottom - 4), 2)
        t = self.font.render(str(rod["value"]), True, self.BLUE)
        self.WIN.blit(t, (r.centerx - t.get_width()//2, r.centery -t.get_height()//2))

    # --------------------------------------------------------------------
    # Draw connected rod for rods inside reactor
    # --------------------------------------------------------------------
    def draw_connected_rod(self):
        if not self.ordered_rods:
            return

        # Build the full text
        expr_text = ''.join(str(r["value"]) for r in self.ordered_rods)

        # Draw a single horizontal rod at the TOP of reactor
        rod_width = max(50 * len(self.ordered_rods), 150)
        rod_height = 60
        rod_rect = pygame.Rect(self.core_x - rod_width//2,
                               self.core_y - self.core_radius - rod_height - 10,
                               rod_width, rod_height)

        pygame.draw.rect(self.WIN, self.BLUE, rod_rect, border_radius=20)
        pygame.draw.rect(self.WIN, self.WHITE, rod_rect, 2, border_radius=20)

        # Draw text centered
        t = self.font.render(expr_text, True, self.WHITE)
        self.WIN.blit(t, (rod_rect.centerx - t.get_width()//2,
                          rod_rect.centery - t.get_height()//2))

    # --------------------------------------------------------------------
    # Draw all
    # --------------------------------------------------------------------
    def draw(self,screen):
        self.WIN.fill(self.BLACK)
        self.draw_reactor()

        tgt = self.font.render(f"Target: {self.target}", True, self.YELLOW)
        self.WIN.blit(tgt, (20, 20))

        # Draw rods outside reactor
        for rod in self.rods:
            self.draw_rod(rod)

        # Draw connected rod inside reactor (top)
        self.draw_connected_rod()

        # Draw attempt button
        pygame.draw.rect(self.WIN, self.GREEN, self.attempt_button,
border_radius=8)
        btn_text = self.smallfont.render("ATTEMPT", True, self.BLACK)
        self.WIN.blit(btn_text, (self.attempt_button.centerx -
btn_text.get_width()//2,
                                 self.attempt_button.centery -
btn_text.get_height()//2))


        screen.blit(pygame.transform.scale(self.WIN,[1200,800]),[0,0])


    # --------------------------------------------------------------------
    # Evaluate rods in the order they were added
    # --------------------------------------------------------------------
    def evaluate_rods(self, rods):
        expr = ''.join(str(r["value"]) for r in rods)
        try:
            return int(eval(expr))
        except:
            return None

    # --------------------------------------------------------------------
    # Check puzzle on ATTEMPT
    # --------------------------------------------------------------------
    def check_puzzle(self):
        if not self.ordered_rods:
            self.show_message("No rods in reactor!", self.RED)
            return

        result = self.evaluate_rods(self.ordered_rods)
        if result == self.target:
            neutrons.add_neutrons(20)
            self.show_message("REACTOR STABLE +20N", self.GREEN)
        else:
            self.show_message(f"UNSTABLE", self.RED)

        pygame.time.delay(1200)
        self.new_puzzle()

    # --------------------------------------------------------------------
    # Show message
    # --------------------------------------------------------------------
    def show_message(self, text, color):
        msg = self.font.render(text, True, color)
        self.WIN.blit(msg,
            (self.WIDTH//2 - msg.get_width()//2,
             self.HEIGHT//2 - msg.get_height()//2))

    # --------------------------------------------------------------------
    # Main loop
    # --------------------------------------------------------------------
    def update(self):
        mp=pygame.mouse.get_pos()
        mc=pygame.mouse.get_pressed()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return 1

        if mc[0] and self.pressed==False:
            self.pressed=True
            mx, my = mp
            for rod in reversed(self.rods):
                if rod["rect"].collidepoint(mx, my):
                    self.selected = rod
                    self.offset_x = rod["rect"].x - mx
                    self.offset_y = rod["rect"].y - my
                    break
            if self.attempt_button.collidepoint(mx, my):
                self.check_puzzle()

        if not mc[0]:
            if self.pressed:
                # Add/remove from ordered rods
                if self.selected:
                    if self.selected in self.ordered_rods:
                        # Remove if dragged out of reactor
                        dx = self.selected["rect"].centerx - self.core_x
                        dy = self.selected["rect"].centery - self.core_y
                        if (dx**2 + dy**2)**0.5 > self.core_radius:
                            self.ordered_rods.remove(self.selected)
                    else:
                        # Add if inside reactor
                        dx = self.selected["rect"].centerx - self.core_x
                        dy = self.selected["rect"].centery - self.core_y
                        if (dx**2 + dy**2)**0.5 < self.core_radius:
                            self.ordered_rods.append(self.selected)

                self.selected = None
            self.pressed=False


        if mc[0] and self.selected:
            mx, my = mp
            self.selected["rect"].x = mx + self.offset_x
            self.selected["rect"].y = my + self.offset_y
        return 0
        # self.draw(screen)


