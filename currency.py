import pygame as pg
from functions import text
font_name="Calibri"
class label():
    def __init__(self, pos, width, txt, size, font_color, bgcolor=0):
        self.font = pg.font.SysFont(font_name, size)
        self.label = text( self.font,txt, font_color)
        self.color=font_color
        self.bgcolor = bgcolor
        self.txt=txt
        self.rect=pg.Rect(pos,(width,size))
    def draw(self, screen):
        if self.bgcolor:
            pg.draw.rect(screen, self.bgcolor, self.rect)
        screen.blit(self.label[0],self.rect)
    def update_text(self,txt):
        self.txt=txt
        self.label = text(self.font,txt, self.color)
    def change_pos(self,new_pos):
        self.rect.topleft=new_pos
    def update_size(self,size):
        self.font = pg.font.SysFont(font_name, size)
        self.update_text(self.txt)
class Neutron:
    def __init__(self):
        self.neutrons=0
        self.txt=f"Neutrons: {self.neutrons}"
        self.main_size=45
        self.cur_size=self.main_size
        self.label=label((20,100),0,self.txt,self.main_size,(0,0,255))
    def add_neutrons(self,q):
        self.cur_size+=q*2
        self.neutrons+=q
        self.txt=f"Neutrons: {self.neutrons}"
        self.label.update_text(self.txt)
        self.label.update_size(self.cur_size)
    def del_n(self,q):
        self.neutrons = max(self.neutrons-q,0)
        self.txt = f"Neutrons: {self.neutrons}"
        self.label.update_text(self.txt)
    def update(self):
        if self.cur_size!=self.main_size:
            self.cur_size-=1
        self.label.update_size(self.cur_size)
    def draw(self,screen):
        self.label.draw(screen)
neutrons=Neutron()

