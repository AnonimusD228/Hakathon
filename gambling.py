import pygame
import random
import sys

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radiation Slots Machine")

FONT = pygame.font.SysFont("consolas", 32)
SMALL = pygame.font.SysFont("consolas", 20)

# --- Colors ---
GREEN = (0, 255, 0)
DARKGREEN = (0, 180, 0)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# --- Slot Symbols (letters) ---
# --- Load images ---
SYMBOL_IMAGES = {
    "A": pygame.image.load("gambling/pixilart-drawing(5).png").convert_alpha(),
    "B": pygame.image.load("gambling/pixilart-drawing(2).png").convert_alpha(),
    "C": pygame.image.load("gambling/pixilart-drawing(1).png").convert_alpha(),
    "D": pygame.image.load("gambling/pixilart-drawing(3).png").convert_alpha(),
    "E": pygame.image.load("gambling/pixilart-drawing(4).png").convert_alpha()
}

SYMBOL_KEYS = list(SYMBOL_IMAGES.keys())  # ["A", "B", "C", "D", "E"]



# --- Game state ---
reels = ["A", "B", "C"]
spinning = False
spin_timer = 0
SPIN_DURATION = 900  # ms
BUTTON = pygame.Rect(WIDTH//2 - 60, HEIGHT - 80, 120, 50)

clock = pygame.time.Clock()

# --- Energy system ---
energy = 1000
SPIN_COST = 50
JACKPOT_REWARD = 500
STRAIGHT_REWARD = 150

win_message = ""

# --- Helper Functions ---
def draw_reels():
    x_start = WIDTH//2 - 150
    for i, symbol in enumerate(reels):
        rect = pygame.Rect(x_start + i*150, HEIGHT//2 - 80, 120, 160)
        pygame.draw.rect(WIN, GRAY, rect, border_radius=8)

        # Draw image centered in rect
        img = SYMBOL_IMAGES[symbol]
        img = pygame.transform.scale(img, (100, 140))  # adjust size if needed
        WIN.blit(img, (rect.centerx - img.get_width()//2,
                       rect.centery - img.get_height()//2))

def draw_button():
    pygame.draw.rect(WIN, DARKGREEN, BUTTON, border_radius=10)
    text = FONT.render("SPIN", True, BLACK)
    WIN.blit(text, (BUTTON.centerx - text.get_width()//2,
                    BUTTON.centery - text.get_height()//2))

def draw_message(msg, color=YELLOW):
    text = SMALL.render(msg, True, color)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, 20))

def draw_energy():
    text = SMALL.render(f"Energy: {energy}", True, GREEN)
    WIN.blit(text, (20, 20))

def random_symbol():
    return random.choice(SYMBOL_KEYS)


# --- Game Loop ---
running = True
while running:
    dt = clock.tick(60)
    WIN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BUTTON.collidepoint(event.pos) and not spinning:
                if energy >= SPIN_COST:
                    energy -= SPIN_COST
                    spinning = True
                    spin_timer = pygame.time.get_ticks()
                    win_message = ""
                else:
                    win_message = "Not enough energy!"

    # --- spinning logic ---
    if spinning:
        for i in range(3):
            reels[i] = random_symbol()

        if pygame.time.get_ticks() - spin_timer >= SPIN_DURATION:
            spinning = False
            # final results
            reels = [random_symbol() for _ in range(3)]

            # win detection
            if len(set(reels)) == 1:
                win_message = f"JACKPOT! {' '.join(reels)} +{JACKPOT_REWARD}"
                energy += JACKPOT_REWARD
            else:
                win_message = "No win. Try again!"

    # --- Draw everything ---
    draw_reels()
    draw_button()
    draw_energy()
    if win_message:
        draw_message(win_message)

    pygame.display.update()

pygame.quit()
sys.exit()
