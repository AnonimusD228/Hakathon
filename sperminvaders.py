import random
import pygame as pg
from pygame import K_SPACE
from settings import *
from assets import Particles
neutron_image="neu.png"

class Enemy:
    def __init__(self):
        self.respawn_delay=(80,120)
        self.active=False
        self.update_respawn()
        self.health=0
    def update_respawn(self):
        self.cur_respawn_delay=random.randint(self.respawn_delay[0],self.respawn_delay[1])
    def respawn(self,size,images):
        self.size=size
        self.rect=pg.Rect((0,0),size)
        self.type=random.randint(0,2)
        self.rect.x=random.randint(0,screen_width-self.rect.w)
        self.rect.y=-self.rect.h

        health_ranges=[(2,6),(8,12),(15,20)]
        speed_ranges=[(9,13),(6,10),(2,5)]
        self.image=images[self.type]
        self.speed=random.randint(speed_ranges[self.type][0],speed_ranges[self.type][1])
        self.max_health=random.randint(health_ranges[self.type][0],health_ranges[self.type][1])
        self.health=self.max_health

        self.update_respawn()
    def update_size(self):
        prev_center=self.rect.center
        a=0.5
        ratio=(self.max_health*a+self.health)/((1+a)*self.max_health)
        self.image=pg.transform.scale(self.image,(int(self.size[0]*ratio),int(self.size[1]*ratio)))
        self.rect=self.image.get_rect()
        self.rect.center=prev_center
    def update(self,size,images,particles):
        if not self.active:
            if self.cur_respawn_delay<=0:
                self.active=True
                self.respawn(size,images)
                return
            self.cur_respawn_delay-=1
            return
        if self.health<=0:
            self.active=False
            particles.append(Particles(self.rect.center,60,10,20,neutron_image,(30,30),fading=False))
            self.update_respawn()
            return
        self.rect.y+=self.speed
        if self.rect.y>=screen_height:
            self.active=False
            self.update_respawn()
            return True
        return False
    def collide_bullet(self,pos):
        if not self.active:
            return
        if self.rect.collidepoint(pos):
            self.health-=1
            self.update_size()
            return True
        return False
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self,pos,velocity,r=3,):
        self.r=r
        self.pos=[pos[0],pos[1]]
        self.v=velocity
    def draw(self,screen):
        pg.draw.circle(screen,(0,200,0),self.pos,self.r)
    def update(self,enemys):
        for i in range(self.v):
            self.pos[1]-=1
            for j in enemys:
                if j.collide_bullet(self.pos):
                    return True
        if self.pos[1]<=0:
            return True
        return False

class Player:
    def __init__(self,pos,size,image=None,speed=5,shoot_delay=2):
        self.rect=pg.Rect((0,0),size)
        self.rect.center=pos
        if image:
            self.image=pg.transform.scale(pg.image.load(image),size)
        else:
            self.image = pg.Surface(size)
            self.image.fill((150, 0, 0))
        self.speed=speed
        self.shoot_delay=shoot_delay
        self.cur_shoot_delay=shoot_delay
        self.bullets=[]

    def update_bullets(self,enemys):
        l=len(self.bullets)
        for i in range(l-1,-1,-1):
            if self.bullets[i].update(enemys):
                self.bullets.pop(i)

    def update(self,enemys):

        keys=pg.key.get_pressed()


        if self.cur_shoot_delay==0:
            if keys[pg.K_SPACE]:
                self.bullets.append(Bullet((self.rect.centerx,self.rect.y),10))
                self.cur_shoot_delay=self.shoot_delay
        else:
            self.cur_shoot_delay-=1
        self.update_bullets(enemys)
        if keys[pg.K_a]:
            self.rect.x-=self.speed
        if keys[pg.K_d]:
            self.rect.x+=self.speed



        self.rect.x=max(0,min(screen_width-self.rect.w,self.rect.x))
        return 0

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for i in self.bullets:
            i.draw(screen)
class Sperm_invaders:
    def start(self):
        player_size=(50,50)
        self.player=Player((screen_width//2-player_size[0]//2,screen_height-player_size[1]),player_size,speed=5)
        self.image = pg.Surface(screen_size)
        self.image.convert_alpha()

        self.enemys_scale=(100,100)
        self.enemys_images=[]
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy1.png"),self.enemys_scale))
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy2.png"),self.enemys_scale))
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy3.png"),self.enemys_scale))

        enemys=8
        self.enemys=[Enemy() for i in range(enemys)]

        self.particles=[]
    def update(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            return 1

        self.image.fill(0)
        self.player.update(self.enemys)
        for i in self.enemys:
            i.update(self.enemys_scale,self.enemys_images,self.particles)
            i.draw(self.image)
        for i in range(len(self.particles)-1,-1,-1):
            j=self.particles[i]
            if j.update(self.player.rect.center,1,15):
                self.particles.pop(i)
            j.draw(self.image)
        self.player.draw(self.image)
        return 0

    def draw(self,screen):
        screen.blit(self.image,(0,0))

