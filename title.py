import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 900, 600
BG = (20, 20, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 100)
GREEN = (0, 255, 0)

FONT = pygame.font.SysFont("consolas", 24)
SMALL = pygame.font.SysFont("consolas", 18)

funny_comments = [
    "Don't do drugs",
    "Sponsored by C. Plover",
    "Keep your distance from glowing rocks.",
    "Stay away!",
    "No, you can't drink the coolant.",
    "Please, dont eat toxic waste",
    "2.5 cups of coffee later",
    "Warning: side effects may include instant death.",
    "I crave Uranium.",
    "Not responsible for DNA damage."
]

title_img = pygame.image.load("title.png").convert_alpha()
TITLE_SCALE = 6
title_img = pygame.transform.scale(title_img, (title_img.get_width()*TITLE_SCALE, title_img.get_height()*TITLE_SCALE))

start_button = pygame.Rect(WIDTH//2 - 70, HEIGHT//2 + 100, 140, 50)

def run_title_screen(WIN):
    clock = pygame.time.Clock()
    sequence_stage = 0
    stage_timer = 0
    stage_duration = [2, 2, 2]  # durations for first three messages
    flash_duration = 2.0
    flash_alpha = 255
    current_comment = random.choice(funny_comments)

    while True:
        dt = clock.tick(60) / 1000
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if sequence_stage == 4 and start_button.collidepoint(mx, my):
                    return  # exit title screen

        stage_timer += dt
        WIN.fill(BG)

        if sequence_stage == 0:
            text = FONT.render("CPlovers Studio Presents", True, YELLOW)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            if stage_timer >= stage_duration[0]:
                sequence_stage += 1
                stage_timer = 0
        elif sequence_stage == 1:
            text = FONT.render("In association with HackTheTopo", True, YELLOW)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            if stage_timer >= stage_duration[1]:
                sequence_stage += 1
                stage_timer = 0
                current_comment = random.choice(funny_comments)
        elif sequence_stage == 2:
            text = SMALL.render(current_comment, True, YELLOW)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            if stage_timer >= stage_duration[2]:
                sequence_stage += 1
                stage_timer = 0
                flash_alpha = 255
        elif sequence_stage == 3:
            # Draw title under flash
            title_rect = title_img.get_rect(center=(WIDTH//2, HEIGHT//2))
            WIN.blit(title_img, title_rect.topleft)
            # Flash fade
            flash_surf = pygame.Surface((WIDTH, HEIGHT))
            flash_surf.fill(WHITE)
            flash_alpha = max(0, int(255 * (1 - stage_timer / flash_duration)))
            flash_surf.set_alpha(flash_alpha)
            WIN.blit(flash_surf, (0, 0))
            if stage_timer >= flash_duration:
                sequence_stage += 1
        elif sequence_stage == 4:
            title_rect = title_img.get_rect(center=(WIDTH//2, HEIGHT//2))
            WIN.blit(title_img, title_rect.topleft)
            pygame.draw.rect(WIN, GREEN, start_button, border_radius=10)
            txt = FONT.render("START", True, BG)
            WIN.blit(txt, (start_button.centerx - txt.get_width()//2,
                           start_button.centery - txt.get_height()//2))

        pygame.display.update()
