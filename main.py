import pygame as pg
import pygame.time
from sperminvaders import *
# from survivors import *
from settings import *
# from title import *
from page import pages,id
from survivors import Survivors
from uranik import Uranik
from shop import *
from mathgame import *
pg.init()
from currency import neutrons

screen=pg.display.set_mode([screen_width,screen_height])
clock=pg.time.Clock()
minigames=[Sperm_invaders(),Survivors(),Mathgame()]

page = pages[id]
shop = ShopRoulette()
uranik = Uranik()
minigame=False
start=True
if  __name__ == "__main__":

    # run_title_screen()
    while True:
        # print(id,0)
        clock.tick(fps)
        mp,mc=pg.mouse.get_pos(),pg.mouse.get_pressed()



        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()

        # sperm_invaders.update()
        # sperm_invaders.draw(screen)
        # surv.update()
        # surv.draw(screen)
        neutrons.update()
        uranik.update(mp,mc,id)
        uranik.draw_bars(screen,id)
        neutrons.draw(screen)
        pg.display.flip()
        screen.fill(bg_color)

        # print(id,1)
        if id<=2:
            id = page.update(mp, mc,id)



        if id>2:
            if start:
                minigames[id-3].start()
                start=False
            minigames[id - 3].draw(screen)
            if minigames[id - 3].update()==1:
                print('ESC')
                id=0
                minigame = False
                start = True
            continue



        page = pages[id]
        page.draw(screen)
        if id == 1:
            uranik.draw(screen)
        elif id==2:
            uranik.energy=shop.run(mp,mc,screen,uranik.energy)

        #
        uranik.drawenergy(screen)



