import pygame as pg
import pygame.time
from space_invaders import *
# from survivors import *
from settings import *
# from title import *
from page import pages,id
from survivors import Survivors
from uranik import *
from shop import *
from mathgame import *
pg.init()
from currency import neutrons

screen=pg.display.set_mode([screen_width,screen_height])
clock=pg.time.Clock()
minigames=[Space_invaders(), Survivors(), Mathgame()]

page = pages[id]
shop = ShopRoulette()
uranik = Uranik()
soap=Soap([950,700],100,100)
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


        # surv.update()
        # surv.draw(screen)
        uranik.dirt,uranik.happines=soap.update(mp,mc,uranik.dirt,uranik.happiness)
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

                id=0
                uranik.dirt.append(Dirt())
                uranik.happiness-=dirt_def
                minigame = False
                start = True
            continue



        page = pages[id]
        page.draw(screen)
        if id == 1:
            uranik.draw(screen)
            soap.draw(screen)
        elif id==2:
            uranik.energy=shop.run(mp,mc,screen,uranik.energy)

        #
        uranik.drawenergy(screen)



