import random
import pygame as pg
import pygame.key
from pygame import K_SPACE
from functions import pitagolas, pidarolas, random_unit_vector, normalised_vec
from settings import *
from assets import Particles
neutron_image="neu.png"
class Health_bar:
    def __init__(self,health,width,height,offset=5):
        self.max_health=health
        self.width=width
        self.height=height
        self.offset=offset
    def draw(self,screen,player,cur_health):
        # print(player,pg.Rect(player.y-self.offset-self.height,player.x,self.width,self.height))
        pg.draw.rect(screen,(50,0,0),pg.Rect(player.x,player.y-self.offset-self.height,self.width,self.height))
        pg.draw.rect(screen,(225,0,0),pg.Rect(player.x,player.y-self.offset-self.height,self.width*(cur_health/self.max_health),self.height))
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
        l=pidarolas((0,0),(screen_width/2,screen_height/2))+pidarolas((0,0),(size[0]/2,size[1]/2))
        res_pos=random_unit_vector()
        self.rect.center=(screen_width/2-res_pos[0]*l,screen_height/2-res_pos[1]*l)

        health_ranges=[(2,6),(6,10),(11,13)]
        speed_ranges=[(5,6),(3,4),(2,3)]
        self.image=images[self.type]
        self.speed=random.randint(speed_ranges[self.type][0],speed_ranges[self.type][1])
        self.max_health=random.randint(health_ranges[self.type][0],health_ranges[self.type][1])
        self.health=self.max_health
        self.damage=random.randint(5,15)

        self.push_vec=[0,0]
        self.health_bar=Health_bar(self.max_health,size[0],15,5)
        self.update_respawn()
    def update_damage(self):
        ratio=self.health/self.max_health
        self.image=pg.transform.scale(self.image,(int(self.size[0]*ratio),int(self.size[1]*ratio)))
        self.image = pg.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))
    def move(self,target):
        vec=normalised_vec(self.rect.center,target)
        if sum(self.push_vec)==0:
            self.rect.x+=vec[0]*self.speed
            self.rect.y+=vec[1]*self.speed
        else:
            self.rect.x+=self.push_vec[0]-self.dx*self.cur
            self.rect.y+=self.push_vec[1]-self.dy*self.cur
            if abs(self.push_vec[0])<abs(self.dx*self.cur):
                self.push_vec=[0,0]
            self.cur+=1
    def collide_player(self,player):
        return self.rect.colliderect(player)
    def push(self,player,v,dur):
        l = max(v-pidarolas(self.rect.center,player.center)*0.05,0)
        push_vec = normalised_vec(player.center,self.rect.center)
        self.push_vec=[push_vec[0]*l,push_vec[1]*l]
        self.dx=self.push_vec[0]/dur
        self.dy=self.push_vec[1]/dur
        self.cur=0
    def update(self,size,images,particles,target,player):
        if not self.active:
            if self.cur_respawn_delay<=0:
                self.active=True
                self.respawn(size,images)
                return False
            self.cur_respawn_delay-=1
            return False
        if self.health<=0:
            self.active=False
            particles.append(Particles(self.rect.center,60,10,random.randint(5,15),neutron_image,(30,30),fading=False))
            self.update_respawn()
            return False
        self.move(target)
        if self.collide_player(player):
            self.active=False
            self.update_respawn()
            return True
        return False
    def collide_bullet(self,pos,damage):
        if not self.active:
            return
        if self.rect.collidepoint(pos):
            self.health=max(self.health-damage,0)
            self.update_damage()
            return True
        return False
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
            self.health_bar.draw(screen,self.rect,self.health)

class Bullet:
    def __init__(self,pos,velocity,r=3,damage=1):
        self.r=r
        self.pos=[pos[0],pos[1]]
        self.v=velocity
        self.damage=damage
    def draw(self,screen,image=None):
        pg.draw.circle(screen,(0,200,0),self.pos,self.r)
    def update(self,enemys):
        l=pidarolas((0,0),self.v)
        dx=self.v[0]/l
        dy=self.v[1]/l
        for i in range(int(l)):
            self.pos[0]+=dx
            self.pos[1]+=dy
            for j in enemys:
                if j.collide_bullet(self.pos,self.damage):
                    return True
        if 0>=self.pos[0] or self.pos[1]<=0 or self.pos[0]>screen_width or self.pos[1]>screen_height:
            return True
        return False

class Player:
    def __init__(self,pos,size,image=None,speed=5,shoot_delay=10,push_delay=200,dash_delay=200):
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

        self.push_delay=push_delay
        self.cur_push=push_delay

        self.dash_delay=dash_delay
        self.cur_dash=dash_delay
        self.dash_dur=60

        self.bullets=[]
        self.max_health=100
        self.health=100
        self.health_bar=Health_bar(self.max_health,500,50,25)
        self.damage=1
        self.strength=0
        # self.push_icon=Icon(pg.image.load("push.png"),(100,100),push_delay,shade_alpha=100)

    def update_bullets(self,enemys):
        l=len(self.bullets)
        for i in range(l-1,-1,-1):
            if self.bullets[i].update(enemys):
                self.bullets.pop(i)
    # def update_icons(self):
    #     self.push_icon.update(self.cur_push)
    def update(self,enemys,particles):

        keys=pg.key.get_pressed()
        if not self.strength:
            self.damage=1
        else:
            self.strength-=1
            particles.append(Particles(self.rect.center,30,3,1,None,(20,20),color=(0,200,0),nf=True))
        if self.cur_shoot_delay==0:
            if keys[pg.K_SPACE]:
                bullet_vel=8
                vec=normalised_vec(self.rect.center,pg.mouse.get_pos())
                self.bullets.append(Bullet((self.rect.centerx,self.rect.y),(vec[0]*bullet_vel,vec[1]*bullet_vel),damage=self.damage))
                self.cur_shoot_delay=self.shoot_delay
        else:
            self.cur_shoot_delay-=1
        if self.cur_push==0:
            if keys[pg.K_e]:
                for i in enemys:
                    i.push(self.rect,40,20)
                self.cur_push=self.push_delay
        else:
            self.cur_push-=1

        if self.cur_dash==0:
            if keys[pg.K_q]:
                self.cur_dash=self.dash_delay+self.dash_dur
        else:
            self.cur_dash-=1

        dash=2 if self.cur_dash>self.dash_delay else 1
        self.update_bullets(enemys)
        if keys[pg.K_a]:
            self.rect.x-=self.speed* dash
        if keys[pg.K_d]:
            self.rect.x+=self.speed* dash
        if keys[pg.K_w]:
            self.rect.y-=self.speed* dash
        if keys[pg.K_s]:
            self.rect.y+=self.speed* dash
        self.rect.y=max(0,min(screen_height-self.rect.h,self.rect.y))
        self.rect.x=max(0,min(screen_width-self.rect.w,self.rect.x))
        return self.health<=0

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for i in self.bullets:
            i.draw(screen)
        self.health_bar.draw(screen,pg.Rect(screen_width/2-self.health_bar.width/2,screen_height,50,50),self.health)
        # self.push_icon.draw(screen,(screen_width/2-self.health_bar.width/2-150,screen_height-150))
    def get_damage(self,damage):
        self.health=max(self.health-damage,0)
class item:
    def __init__(self):
        self.respawn_delay=(300,500)
        self.active=False
        self.update_respawn()
    def update_respawn(self):
        self.cur_respawn_delay=random.randint(self.respawn_delay[0],self.respawn_delay[1])
    def respawn(self,images):
        self.type=random.randint(0,1)
        self.image=images[self.type]
        self.rect=self.image.get_rect()
        self.rect.x=random.randint(100,screen_width-200)
        self.rect.y=random.randint(100,screen_height-200)
        self.active=True
    def update(self,player: Player,images):
        if not self.active:
            self.cur_respawn_delay-=1
            if not self.cur_respawn_delay:
                self.active=True
                self.respawn(images)
            return
        if not self.rect.colliderect(player.rect):
            return
        if self.type==0:
            player.health=min(player.max_health,player.health+random.randint(30,60))
            self.update_respawn()
            self.active=False
            return
        player.strength=500
        player.damage=3
        self.update_respawn()
        self.active=False
    def draw(self,screen):
        if not self.active:
            return
        screen.blit(self.image,self.rect)

class Survivors:
    def start(self):
        player_size=(50,50)
        self.player=Player((screen_width//2,screen_height//2),player_size,speed=5)
        self.image = pg.Surface(screen_size)
        self.image.convert_alpha()
        self.bg=pg.transform.scale(pg.image.load("bgv.png"),(screen_width,screen_height)).convert_alpha()


        self.enemys_scale=(100,100)
        self.enemys_images=[]
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy1.png"),self.enemys_scale))
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy2.png"),self.enemys_scale))
        self.enemys_images.append(pg.transform.scale(pg.image.load("enemy3.png"),self.enemys_scale))


        self.potion_scale=(80,80)
        self.potion_images=[]
        self.potion_images.append(pg.transform.scale(pg.image.load("health.png"),self.potion_scale))
        self.potion_images.append(pg.transform.scale(pg.image.load("strenght.png"),self.potion_scale))

        enemys=8
        self.enemys=[Enemy() for i in range(enemys)]

        pots=3

        self.pots=[item() for i in range(pots)]
        self.particles=[]
    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            return 1

        if self.player.health>0:
            self.image.blit(self.bg,(0,0
                                     ))
            self.player.update(self.enemys,self.particles)
            for i in self.enemys:
                if i.update(self.enemys_scale,self.enemys_images,self.particles,self.player.rect.center,self.player):
                    self.player.get_damage(i.damage)
                i.draw(self.image)
            for i in self.pots:
                i.update(self.player,self.potion_images)
                i.draw(self.image)
            for i in range(len(self.particles)-1,-1,-1):
                j=self.particles[i]
                if j.update(self.player.rect.center,1,15):
                    self.particles.pop(i)
                j.draw(self.image)
            self.player.draw(self.image)
        elif keys[pg.K_r]:
            self.start()

        return 0

    def draw(self,screen):
        if self.player.health<=0:
            self.image.blit(pygame.transform.scale(pygame.image.load('deathscreen.png'),[1200,800]),[0,0])
        screen.blit(self.image,(0,0))

