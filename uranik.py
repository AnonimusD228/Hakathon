import random

import pygame.image
from assets import *
# from gambling import energy
# from gambling import energy
from space_invaders import *
from settings import *
from currency import neutrons
global neutrons

dirt_images=[
    pygame.transform.scale(pygame.image.load('brudy/pixil-frame-0.png'),[50,50]),
    pygame.transform.scale(pygame.image.load('brudy/pixil-frame-1.png'),[50,50]),
    pygame.transform.scale(pygame.image.load('brudy/pixil-frame-2.png'),[50,50]),
    pygame.transform.scale(pygame.image.load('brudy/pixil-frame-3.png'),[50,50]),
]

dirt_def = 10

class Dirt:
    def __init__(self):
        self.img=dirt_images[random.randint(0,3)]
        self.pos=[random.randint(600-100,600+100),random.randint(600-100,600+100)]
        self.rect=self.img.get_rect()
        self.rect.center=self.pos

    def draw(self,screen):
        screen.blit(self.img,[self.pos[0]-25,self.pos[1]-25])




class Feed:
    def __init__(self,pos,w,h,r):
        self.rect=pg.Rect(pos,(w,h))
        self.image=pg.transform.scale(pg.image.load("wiadro.png"),(w,h))
        self.neutron=pg.transform.scale(pg.image.load("neu.png"),(r,r))
        self.active=False
    def update(self,uranik):
        mc=pg.mouse.get_pressed()
        mp=pg.mouse.get_pos()
        if not self.active:
            if mc[0] and self.rect.collidepoint(mp):
                self.active=True
            return
        if not mc[0]:
            if uranik.rect.collidepoint(mp):
                uranik.neutronlevel+=min(30,neutrons.neutrons)
                uranik.neutronlevel=min(uranik.neutronlevel,uranik.max_n)
                neutrons.del_n(min(30,neutrons.neutrons))
            self.active=False
            return
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if self.active:
            mp=pg.mouse.get_pos()
            screen.blit(self.neutron,(mp[0]-self.neutron.get_width()/2,mp[1]-self.neutron.get_height()/2))
class Soap:
    def __init__(self,pos,w,h):
        self.rect=pg.Rect([pos[0]-w/2,pos[1]-h/2],(w,h))
        self.image=pg.transform.scale(pg.image.load("mydełko.png"),(w,h))
        self.w,self.h=w,h
        self.pos=pos

    def update(self,mp,mc,dirts,happiness):
        if mc[0] and self.rect.collidepoint(mp):
            self.rect.center=mp
            for i in range(len(dirts)-1,-1,-1):
                if self.rect.colliderect(dirts[i].rect):
                    dirts.pop(i)
                    happiness+=dirt_def
        else:
            self.rect.center=self.pos

        return dirts,happiness

    def draw(self,screen):
        screen.blit(self.image,self.rect)




class Bar:
    def __init__(self,pos,width,height,first_colour,second_colour,image):
        self.rect=pg.Rect(pos,(width,height))
        self.fc=first_colour
        self.sc=second_colour
        self.image=pg.transform.scale(pg.image.load(image),(self.rect.w*2,self.rect.w*2))
        self.image_rect=self.image.get_rect()
    def draw(self,screen,ratio):
        pg.draw.rect(screen,self.sc,self.rect)
        pg.draw.rect(screen,self.fc,pg.Rect(self.rect.x,self.rect.y+self.rect.h*(1-ratio),self.rect.w,self.rect.h*ratio))
        self.image_rect.center=(self.rect.centerx,self.rect.y+self.rect.h*(1-ratio))
        screen.blit(self.image,self.image_rect)
class Bar2:
    def __init__(self,pos,width,height,first_colour,second_colour,image):
        self.rect=pg.Rect(pos,(width,height))
        self.fc=first_colour
        self.sc=second_colour
        self.image=pg.transform.scale(pg.image.load(image),(self.rect.h*2,self.rect.h*2))
        self.image_rect=self.image.get_rect()
    def draw(self,screen,ratio):
        pg.draw.rect(screen,self.sc,self.rect)
        pg.draw.rect(screen,self.fc,pg.Rect(self.rect.x+self.rect.w*(1-ratio),self.rect.y,self.rect.w*ratio,self.rect.h))
        self.image_rect.center=(self.rect.x+self.rect.w*(1-ratio),self.rect.centery)
        screen.blit(self.image,self.image_rect)
class Uranik:
    def __init__(self):
        self.pos=[600,600]
        self.max_h=100
        self.max_n=100
        self.happiness = self.max_h
        self.neutronlevel = self.max_n
        self.size=[300,300]
        self.time = -1
        self.tick=0
        self.hearts=[]
        self.dirt=[]

        self.state=0
        self.animation=0
        self.animations=[[pygame.transform.scale(pygame.image.load('idle1.png'),self.size),pygame.transform.scale(pygame.image.load('idle2.png'),self.size)],
                         [pygame.transform.scale(pygame.image.load('horny.png'),self.size)]]
        self.rect=self.animations[0][0].get_rect()
        self.rect.center=self.pos

        self.happiness_bar=Bar((1000,150),50,450,(200, 0, 0),(100, 0, 0),"happiness.png")
        self.neutron_bar=Bar((1100,150),50,450,(0, 128, 255),(10, 78, 145),"saturation.png")

        self.happiness_bar2=Bar2((screen_width-220,20),190,30,(200, 0, 0),(100, 0, 0),"happiness.png")
        self.neutron_bar2=Bar2((screen_width-220,70),190,30,(0, 128, 255),(10, 78, 145),"saturation.png")

        self.heart = "heart.png"
        self.pressed=False
        self.energy=0
        self.energy_img=pygame.transform.scale(pygame.image.load('gambling/pixilart-drawing(1).png'),[50,50])
        self.energylabel=Simple_label([0,50],200,f'{self.happiness//10} energy/second',35,'black',pos_type=0)
        self.energylabel1 = Simple_label([50, 0], 200, str(self.energy), 50, 'black',
                                        pos_type=0)
        self.feed=Feed((200,600),150,150,50)

    def update(self,mp,mc,id):
        self.time+=1
        self.time%=60
        self.tick+=1
        self.tick%=1000
        self.feed.update(self)
        if self.time == 0:
            self.happiness=max(self.happiness-1,0)
            self.neutronlevel=max(self.neutronlevel-2,0)
            self.energy+=self.happiness//10
            self.energylabel.update_text(f'{self.happiness // 10} energy/second')
            self.energylabel1.update_text(f'{self.energy}')
        # self.time

        if mc[0] and self.rect.collidepoint(mp):
            if id==1 and self.pressed==False:
                self.pressed=True
                self.happiness=min(self.max_h,self.happiness+1)
                self.hearts.append(Particles(mp,67,6.7,10,self.heart,(30,30)))

        else:
            self.pressed=False

        for i in range(len(self.hearts)-1,-1,-1):
            if self.hearts[i].update():
                self.hearts.pop(i)

        if self.happiness>self.max_h*0.8:
            self.state=1
        else:
            self.state=0
            #jeszcze particle !!!!!!!!!!!!!


    def draw_bars(self,screen,id):
        if id==1:

            self.neutron_bar.draw(screen,self.neutronlevel/self.max_n)
            self.happiness_bar.draw(screen,self.happiness/self.max_h)
        else:
            self.neutron_bar2.draw(screen,self.neutronlevel/self.max_n)
            self.happiness_bar2.draw(screen,self.happiness/self.max_h)






    def draw(self,screen):
        if self.tick%100==0:
            print(self.animation)
            self.animation+=1
        self.animation%=len(self.animations[self.state])
        screen.blit(self.animations[self.state][self.animation],self.rect)
        self.feed.draw(screen)
        for i in self.hearts:
            i.draw(screen)
        for i in self.dirt:
            i.draw(screen)




    def drawenergy(self,screen):
        screen.blit(self.energy_img, [0, 0])
        self.energylabel.draw(screen)
        self.energylabel1.draw(screen)





