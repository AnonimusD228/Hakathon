from currency import neutrons
from functions import *
from settings import *
import math as meth
from functions import random_unit_vector

class text_box():
    def __init__(self, p, width, height, size, text):
        self.active = False
        self.pos = p
        self.width = width
        self.height = size
        self.thick = 5
        self.text = text
        self.textr = [self.text]
        self.size = size
        self.ofs = self.thick / 2
        ofs = self.ofs
        self.font = pg.font.SysFont("ComicSans", size)
        self.rect = pg.Rect(p[0] - ofs, p[1] - ofs, self.width + ofs * 3, self.height + ofs * 3)

    def draw(self, screen):
        for n in range(len(self.textr)):
            a = text(self.font, self.textr[n], (255, 255, 255))
            screen.blit(a[0], (self.pos[0] + self.ofs * 2, self.pos[1] + self.size * n))
        if self.active:
            pg.draw.rect(screen, (255, 125, 0), self.rect, self.thick)
        else:
            pg.draw.rect(screen, (125, 125, 0), self.rect, self.thick)

    def update_size(self):
        self.textr = []
        pointer = 0
        l = len(self.text)
        self.textr = text_down(self.text, self.font, self.width)
        b = len(self.textr)
        self.height = b * self.size
        self.rect.height = self.height + self.ofs * 5


class wybieracz():
    def __init__(self, list, pos, width, size, border_size):
        self.border = border_size
        self.list = list
        self.pos = pos
        self.width = width
        self.font = pg.font.SysFont("TimesNewRoman", size)
        self.textsr = []
        self.rects = []
        self.size = size
        y = pos[1]
        self.ofs = 6
        self.active = 0
        for n in list:
            self.textsr.append(text_down(n, self.font, self.width))
            self.rects.append(pg.Rect(pos[0] - self.ofs, y - self.ofs, self.width + self.ofs * 3,
                                      len(self.textsr[-1]) * size + self.ofs * 3))
            y = self.rects[-1].bottom
        self.pick = 0

    def draw(self, screen):
        color = (50, 50, 50)
        if self.active:
            for n in range(len(self.rects)):
                color = (50, 50, 50)
                if n == self.pick:
                    color = (255, 125, 0)
                pg.draw.rect(screen, color, self.rects[n], self.border)
                for i in range(len(self.textsr[n])):
                    a = text(self.font, self.textsr[n][i], (255, 255, 255))
                    screen.blit(a[0], (
                    self.pos[0] + self.width / 2 - a[1] / 2 + self.ofs, self.rects[n].y + self.size * i + self.ofs))

        else:
            pg.draw.rect(screen, color,
                         pg.Rect((self.pos), (self.rects[self.pick].width, self.rects[self.pick].height)))
            for i in range(len(self.textsr[self.pick])):
                a = text(self.font, self.textsr[self.pick][i], (255, 255, 255))
                screen.blit(a[0], (
                self.pos[0] + self.width / 2 - a[1] / 2 + self.ofs, self.pos[1] + self.size * i + self.ofs))

    def check_collision(self, mp):
        if self.active:
            for n in range(len(self.list)):
                if self.rects[n].collidepoint(mp):
                    self.pick = n
                    n = -1
                    break
            self.active = n == -1
        else:
            self.active = self.rects[self.pick].collidepoint((mp[0], mp[1] + self.rects[self.pick].y - self.pos[1]))


class slider():
    def __init__(self, pos, width, height, point_radius, colors, a=1, b=0, intiger=0, vertical=0):
        self.srect = pg.Rect(pos, (width, height))
        self.pr = point_radius
        self.colors = colors
        self.v = vertical
        self.ppos = [self.srect.center[0], self.srect.center[1]]
        self.value = 0.5
        self.pos = pos
        self.size = (width, height)
        self.font = pg.font.SysFont("Arial", self.pr)
        self.a = a
        self.b = b
        self.i = intiger

    def draw(self, screen):
        pg.draw.rect(screen, self.colors[0], self.srect)
        pg.draw.circle(screen, self.colors[1], self.ppos, self.pr)

    def move(self, mp):
        if self.pos[self.v] + self.size[self.v] > mp[self.v] > self.pos[self.v] and (mp[0] - self.ppos[0]) ** 2 + (
                mp[1] - self.ppos[1]) ** 2 < self.pr ** 2:
            self.ppos[self.v] = mp[self.v]
            self.value = (mp[self.v] - self.pos[self.v]) / self.size[self.v]
            self.value *= self.a
            self.value += self.b
            if self.i:
                self.value = int(self.value)
            return True

    def show_value(self, screen):
        sv = int(self.value * 1000) / 1000
        txt = text(self.font, str(sv), (0))
        w = txt[1]
        rect = pg.Rect(self.ppos[0] - w / 2, self.ppos[1] - self.pr * 2, w, self.pr)
        pg.draw.rect(screen, (255, 255, 255), rect)
        screen.blit(txt[0], rect)


gui_font = pg.font.Font(None,30)
class Button:
    def __init__(self,text,width,height,pos,elevation,font_size,color_1,color_2,font_color=(255,255,255),font="Arial",pos_type=0):
        if pos_type:
            pos=pos[0]-width/2,pos[1]-height/2
        self.pressed = False
        self.elevation = elevation
        self.swap = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pg.Rect(pos,(width,height))
        self.top_color = color_1

        self.bottom_rect = pg.Rect(pos,(width,height))
        self.bottom_color = color_2
        self.text_surf = pg.font.SysFont(font,font_size).render(text,True,font_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.do=0
    def draw(self,screen):
        self.top_rect.y = self.original_y_pos - self.swap
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.swap

        pg.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pg.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
    def update(self,mp,mc):
        self.check_click(mp,mc)
        return self.do
    def check_click(self,mp,mc):
        self.do=0
        if self.top_rect.collidepoint(mp):
            if mc[0]:
                self.swap = 0
                self.pressed = True
            else:
                self.swap = self.elevation
                if self.pressed == True:
                    self.do=1
                    self.pressed = False
        else:
            self.swap = self.elevation


class label():
    def __init__(self, pos, width, txt, size, font_color, bgcolor=0):
        self.font = pg.font.SysFont("Arial", size)
        self.labels = text_down(txt, self.font, width)
        self.surfaces = []
        self.bgcolor = bgcolor
        self.size = size
        maxx = 0
        for n in self.labels:
            self.surfaces.append(text(self.font, n, font_color))
            maxx = max(self.surfaces[-1][1], maxx)

        self.rect = pg.Rect(pos, (maxx, size * len(self.surfaces)))

    def draw(self, screen):
        if self.bgcolor:
            pg.draw.rect(screen, self.bgcolor, self.rect)
        for n in range(len(self.surfaces)):
            screen.blit(self.surfaces[n][0], (self.rect.x, self.rect.y + self.size * n))
class Simple_label():
    def __init__(self, pos, width, txt, size, font_color, bgcolor=0,pos_type=0):
        self.font = pg.font.SysFont("Arial", size)
        self.label = text( self.font,txt, font_color)
        self.color=font_color
        self.bgcolor = bgcolor
        self.pos_type=pos_type
        if pos_type:
            # self.rect=pg.Rect(pos[0]-self.label[1]//2,pos[1]-self.label[2]//2, width, size)
            self.rect = pg.Rect(pos[0] - width // 2, pos[1] - self.label[2] // 2, width, size)
        else:
            self.rect=pg.Rect(pos,(width,size))
    def draw(self, screen):
        if self.bgcolor:
            pg.draw.rect(screen, self.bgcolor, self.rect)
        screen.blit(self.label[0],self.rect)
    def update_text(self,txt):
        self.label = text(self.font,txt, self.color)
        if self.pos_type:
            r=self.label[0].get_rect()
            r.center=self.rect.center
            self.rect=r
            del r

class Simple_list:
    def __init__(self, pos, width, texts, size, font_color, bgcolor=0,pos_type=0):
        self.size=len(texts)
        self.labels=[Simple_label([pos[0],pos[1]+size*i],width, texts[i], size, font_color, bgcolor,pos_type)for i in range(self.size)]
        self.info=[pos, width, size, font_color, bgcolor,pos_type]
    def draw(self, screen):
        for i in self.labels:
            i.draw(screen)
    def update_text(self,txt,index):
        self.labels[index].update_text(txt)
    def add(self,txt):
        self.labels.append(Simple_label([self.info[0][0],self.info[0][1]+self.info[2]*self.size],self.info[1],txt
                                        ,self.info[2],self.info[3],self.info[4],self.info[5]))
        self.size+=1
    def insert(self,txt,index):
        pass

class Particle:
    def __init__(self,image,pos,vel,dur):
        self.image=image
        self.pos=[pos[0],pos[1]]
        self.vel=vel
        self.dur=dur
    def update(self,cur):
        ratio=cur/self.dur
        self.pos[0]+=self.vel[0]*ratio
        self.pos[1]+=self.vel[1]*ratio
    def update_speed(self,vec,speed):
        self.vel=[vec[0]*speed,vec[1]*speed]
    def draw(self,screen):
        screen.blit(self.image,self.pos)
class Particles:
    def __init__(self,start,duration,vel,q,image,size,fading=True,color=None,nf=False):
        self.nf=nf
        if image:
            self.image=pg.transform.scale(pg.image.load(image),size)
        else:
            self.image=pg.Surface(size)
            pg.draw.circle(self.image,color,(int(size[0]/2),int(size[1]/2)),int(size[0]/2))
        self.particles=[]
        self.dur=duration
        self.cur=duration
        for i in range(q):
            r=random_unit_vector()
            self.particles.append(Particle(self.image,start,(r[0]*vel,r[1]*vel),duration))
        self.fading=fading
    def update(self,target=None,target_at=None,speed=0):
        ratio=self.cur/self.dur
        if self.fading:
            self.image.set_alpha(int(255*ratio))
        for j in range(len(self.particles)-1,-1,-1):
            i=self.particles[j]
            if not self.nf and target and target_at==self.cur:
                i.update_speed(normalised_vec(i.pos,target),speed)
                i.update(self.dur)
                if pitagolas(i.pos,target)<=speed**2:
                    self.particles.pop(j)
                    neutrons.add_neutrons(1)
            else:
                i.update(self.cur)
        if self.nf or (not target or target_at!=self.cur):
            self.cur-=1
        return self.cur==0 or not self.particles
    def draw(self,screen):
        for i in self.particles:
            i.draw(screen)


import pygame


# class Icon:
#     def __init__(self, image: pygame.Surface, size, max_val, cur_val=0, shade_alpha=140):
#         self.max_val = max_val
#         self.cur_val = cur_val
#
#         self.w, self.h = size
#         self.radius = self.w // 2
#
#         # Precompute circular mask once (expensive!)
#         self.mask = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
#         pygame.draw.circle(self.mask, (255, 255, 255), (self.radius, self.radius), self.radius)
#         self.mask.blit(image,(0,0))
#
#         # Build first frame
#         self.update(self.cur_val)
#
#     def update(self, new_val):
#         self.cur_val = new_val
#     def draw(self, surface: pygame.Surface, pos):
#         final=0
#         surface.blit(self.final, pos)

