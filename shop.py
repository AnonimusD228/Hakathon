import pygame, sys, random, time, os
from settings import *

pygame.init()
pygame.mixer.init()   # <-- SOUND SYSTEM ON

WIDTH, HEIGHT = 900, 600

FONT = pygame.font.SysFont("consolas", 24)
SMALL = pygame.font.SysFont("consolas", 18)

BG = (20, 20, 20)
WHITE = (230, 230, 230)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 220, 100)

class ShopRoulette:
    def __init__(self):
        self.screen = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
        self.screen.convert_alpha()

        self.player_coins = 500
        self.owned_items = set()
        self.spin_button = pygame.Rect(WIDTH//2 - 70, HEIGHT-90, 140, 50)

        self.spinning = False
        self.spin_start_time = 0
        self.SPIN_DURATION = 1.2
        self.SPIN_SPEED = 0.05
        self.roulette_results = []

        # ---------------------
        # LOAD SOUND
        # ---------------------
        try:
            self.tick_sound = pygame.mixer.Sound("sounds/tick.wav")
            self.tick_sound.set_volume(0.4)
        except:
            print("⚠ Could not load sounds/tick.wav!")
            self.tick_sound = None

        # Sound cooldown to avoid spamming
        self.tick_cooldown = 0

        # Items...
        self.ITEM_POOL = [
            {"name": "Suspicious pill", "image": "images/pill.png","price": 80, "desc": "Found it near a dead-end. Wanna try yourluck?"},
            {"name": "Cool Headphones", "image":"images/headphones2.png", "price": 60, "desc": 'Cool and calming.Plays "Duality" by Slipknot.'},
            {"name": "100 Neutrons", "image": "images/neutrons.png","price": 90, "desc": "Some food or your friend. He will be saturatedfor 2 minutes!"},
            {"name": "Energy drink", "image": "images/energy.png","price": 100, "desc": "Gets you to code for over 24 hours.Resourceful!"},
            {"name": "Neutron porridge", "image":"images/porridge2.png", "price": 70, "desc": "Cool kasha madeaccording to GOST. Collective!"},
            {"name": "Cool top-hat", "image": "images/top_hat.png","price": 50, "desc": "Has 17-century look to it. Classy!"},
            {"name": "Christmas Hat!", "image":"images/christmas_hat.png", "price": 60, "desc": "This is not approveduniform. Festive and rebellious!"},
            {"name": "Water", "image": "images/water.png", "price":120, "desc": "Plain and boring. Does nothing. Did you expect anythingelse?"},
        ]

        for item in self.ITEM_POOL:
            item["surf"] = self.load_item_image(item["image"])

        self.start_spin()

    def load_item_image(self, path):
        raw = pygame.image.load(path).convert_alpha()
        SCALE = 8
        img = pygame.transform.scale(raw, (raw.get_width()*SCALE,
raw.get_height()*SCALE))
        surface = pygame.Surface((150, 200), pygame.SRCALPHA)
        rect = img.get_rect(center=(75, 100))
        surface.blit(img, rect)
        return surface

    def start_spin(self):
        self.spinning = True
        self.spin_start_time = time.time()
        self.tick_cooldown = 0   # reset sound timer

    def update_spin(self):
        if not self.spinning:
            return

        elapsed = time.time() - self.spin_start_time

        # ------------------------
        # PLAY SOUND WHILE SPINNING
        # ------------------------
        if self.tick_cooldown <= 0:
            if self.tick_sound:
                self.tick_sound.play()
            self.tick_cooldown = 5         # frames delay
        else:
            self.tick_cooldown -= 1

        # SPIN LOGIC
        if elapsed < self.SPIN_DURATION:
            self.roulette_results = [random.choice(self.ITEM_POOL) for
_ in range(5)]
            pygame.time.delay(int(self.SPIN_SPEED * 1000))
        else:
            self.spinning = False
            self.roulette_results = random.sample(self.ITEM_POOL, 5)
            if self.tick_sound:
                self.tick_sound.play()     # final tick

    def draw_items(self, mx, my):
        x = 50
        hovered_item = None
        for item in self.roulette_results:
            r = pygame.Rect(x, 150, 150, 200)
            self.screen.blit(item["surf"], r.topleft)
            pygame.draw.rect(self.screen, WHITE, r, 2, border_radius=12)

            t = SMALL.render(item["name"], True, WHITE)
            self.screen.blit(t, (r.centerx - t.get_width() // 2, r.bottom + 10))

            # Only hats can show "OWNED"
            if item["name"] in self.owned_items and "Hat" in item["name"]:
                o = SMALL.render("OWNED", True, GREEN)
                self.screen.blit(o, (r.centerx - o.get_width() // 2, r.y - 25))

            if r.collidepoint(mx, my):
                hovered_item = item

            x += 170
        return hovered_item

    def draw_description(self, item):
        panel = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 120)
        pygame.draw.rect(self.screen, GRAY, panel, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, panel, 2, border_radius=8)
        self.screen.blit(FONT.render(item["name"], True, WHITE),
                         (panel.x + 20, panel.y + 15))
        self.screen.blit(FONT.render(f"Price: {item['price']} coins",
                                     True, YELLOW), (panel.x + 20, panel.y + 55))
        self.screen.blit(SMALL.render(item["desc"], True, WHITE),
                         (panel.x + 20, panel.y + 90))

    def attempt_buy(self, item):
        if item["name"] in self.owned_items:
            return False
        if self.player_coins >= item["price"]:
            self.player_coins -= item["price"]
            self.owned_items.add(item["name"])
            return True
        return False

    def run(self, mp, mc, scren, energy):
        self.player_coins = energy

        x = (screen_width - WIDTH) / 2
        y = (screen_height - HEIGHT) / 2

        # FIX: do not overwrite mp
        local_mp = (mp[0] - x, mp[1] - y)


        if mc[0]:
            if self.spin_button.collidepoint(local_mp) and not self.spinning:
                self.start_spin()

            if not self.spinning:
                for idx, item in enumerate(self.roulette_results):
                    r = pygame.Rect(50 + 170 * idx, 150, 150, 200)
                    if r.collidepoint(local_mp):
                        if self.attempt_buy(item):
                            self.start_spin()

        self.update_spin()

        self.screen.fill((0, 0, 0, 0))

        pygame.draw.rect(self.screen, YELLOW, self.spin_button,
                         border_radius=10)
        s = FONT.render("SPIN!", True, BG)
        self.screen.blit(s, (self.spin_button.centerx - s.get_width() // 2,
                             self.spin_button.centery - s.get_height() // 2))

        hovered = self.draw_items(local_mp[0], local_mp[1])
        if hovered and not self.spinning:
            self.draw_description(hovered)

        scren.blit(self.screen, [screen_width / 2 - WIDTH / 2,
                                 screen_height / 2 - HEIGHT / 2])

        return self.player_coins

# # ------------------------------
# # RUN
# # ------------------------------
# if __name__ == "__main__":
#     ShopRoulette().run()