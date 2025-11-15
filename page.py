import pygame.surface
from assets import *
from settings import *
from shop import ShopRoulette
#labels:  [names]
#buttons: [names]



id=1



labels= {
    # 'home': Simple_label([500,0],screen_width/6,'home',50,fontcolor,choice_color,0),
    # 'shop': Simple_label([700,0],screen_width/6,'shop',50,fontcolor,color1,0),
    # 'minigames': Simple_label([300,0],screen_width/6,'minigames',50,fontcolor,color1,0)

}




buttons= {
    'minigames'  : Button('minigames',screen_width/6,screen_height/12,[300,0],5,50,color1,color2,fontcolor,pos_type=0),
    'home'  : Button('home',screen_width/6,screen_height/12,[500,0],5,50,choice_color,choice_color2,fontcolor,pos_type=0),
    'shop'  : Button('shop',screen_width/6,screen_height/12,[700,0],5,50,color1,color2,fontcolor,pos_type=0),
'sperm invaders'  : Button('sperm invaders',300,300,[75,250],5,50,color1,color2,fontcolor,pos_type=0),
'survivors'  : Button('survivors',300,300,[450,250],5,50,color1,color2,fontcolor,pos_type=0),
'mathgame'  : Button('mathgame',300,300,[825,250],5,50,color1,color2,fontcolor,pos_type=0),

}


class Page:
    def __init__(self,name,labels,buttons,bg_color=None,bg_image=None):


        self.back_ground=pygame.Surface(screen_size)
        self.back_ground.fill((0,0,0))
        if bg_color:
            self.back_ground.fill(bg_color)# <----------------- !!!!!!!!!!!!!!!
        elif bg_image:
            self.back_ground.blit(pygame.transform.scale(pygame.image.load(bg_image),screen_size),(0,0))# <---------------- !!!!!!!!!!!!!!

        self.name=name
        self.buttons=buttons
        self.labels=labels

    def update(self,mp,mc,id):
        for name in self.buttons:
            if buttons[name].update(mp,mc):


                if name=='home':
                    if id in {0,1,2}:
                        buttons[pages[id].name].top_color = color1
                        buttons[pages[id].name].bottom_color = color2
                    id = 1
                    buttons['home'].top_color = choice_color
                    buttons['home'].bottom_color = choice_color2

                elif name == 'minigames':
                    if id in {0, 1, 2}:
                        buttons[pages[id].name].top_color = color1
                        buttons[pages[id].name].bottom_color = color2
                    id = 0
                    buttons['minigames'].top_color = choice_color
                    buttons['minigames'].bottom_color = choice_color2


                elif name=='shop':
                    if id in {0, 1, 2}:
                        buttons[pages[id].name].top_color = color1
                        buttons[pages[id].name].bottom_color = color2
                    id = 2
                    buttons['shop'].top_color = choice_color
                    buttons['shop'].bottom_color = choice_color2

                if id<3:
                    if name=='sperm invaders':

                        id = 3
                    elif name=='survivors':

                        id = 4
                    elif name=='mathgame':

                        id=5

        return id









    def draw(self,screen):
        screen.blit(self.back_ground,[0,0])
        for name in self.buttons:
            buttons[name].draw(screen)
        for name in self.labels:
            labels[name].draw(screen)



pages=[
    Page('minigames',[],['home','shop','minigames','sperm invaders','mathgame','survivors'],bg_image='pixil-frame-0(11).png'),
    Page('home',[],['home','shop','minigames'],bg_image='pixil-frame-0(9).png'),
    Page('shop',[],['home','shop','minigames'],bg_image='pixil-frame-0(10).png'),
]



