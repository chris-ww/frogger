import pygame
import random
import sys
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os
import math



from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCALE = 16
SCREEN_SIZE=SCALE*16
SCREEN_WIDTH = SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_SIZE
MAP=0
ROT = random.randrange(4)*90


class Chrisww_gym(gym.Env):
   
    def __init__(self):
        pygame.init()
        self.action_space = spaces.Discrete(4)
       # self.level=1
       # self.score=0
       # self.lives=5
        self.clock = pygame.time.Clock()
        self.BackGround = Background(os.path.join(os.path.dirname(__file__), "pictures/map0.png"), [0,0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
       # self.cooldown= 0
        self.player = Player()
       # new_door=Door()
       # self.doors = pygame.sprite.Group()
       # self.doors.add(new_door)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
       # self.all_sprites.add(new_door)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.BackGround.image, self.BackGround.rect)
        


    def step(self, action):
       # self.player.update(action)
    
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.BackGround.image, self.BackGround.rect)
        self.player.update(action)

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
       #     
       # if pygame.sprite.spritecollide(self.player, self.doors, dokill=False):
       #    self.player.kill()

        self.clock.tick(60)
        
    
    def reset(self):
        self.level=1
        self.score=0
        self.lives=5
        self.scale=16
        self.clock = pygame.time.Clock()
        self.BackGround = Background(os.path.join(os.path.dirname(__file__), "pictures/map0.png"), [0,0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.cooldown= 0
        self.player = Player()
        new_door=Door()
        self.doors = pygame.sprite.Group()
        self.doors.add(new_door)
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(new_door)
        self.action_space = spaces.Discrete(4)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.BackGround.image, self.BackGround.rect)
        pygame.init()
        
    def render(self, mode='human', close=False):
        pygame.display.flip()

    def close(self):
        pygame.quit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image= pygame.image.load(os.path.join(os.path.dirname(__file__), "pictures/robot.png")).convert()
        self.image = pygame.transform.scale(self.image,(SCALE,SCALE))
        self.surf = self.image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x=int(SCREEN_SIZE/2)
        self.y=int(SCALE*15.5)
        self.rect = self.surf.get_rect(center=(self.x,self.y))
        self.cooldown=0
        self.angle=0

    def update(self, action):
        if action==0:
            self.angle += 3 % 360
        if action==1:
            self.angle -= 3 % 360   
        if action==2:
            self.x,self.y = calculate_new_xy(self.x,self.y,1,self.angle)
            self.rect = self.surf.get_rect(center = (self.x, self.y)) 
        if action==3:
            self.x,self.y = calculate_new_xy(self.x,self.y,-1,self.angle)
            self.rect = self.surf.get_rect(center = (self.x, self.y)) 
        #if action ==3:
        #    x,y = calculate_new_xy(x,y,-1,self.angle)
        self.surf = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.surf.get_rect(center = (self.x, self.y)) 
        
        

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join(os.path.dirname(__file__), "pictures/blue_van.png")).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE*2,SCALE))
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                -20,
                208,
            )
        )
        self.speed = 5

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > 256:
            self.kill()


class Door(pygame.sprite.Sprite):
    def __init__(self):
        super(Door, self).__init__()
        self.surf = pygame.image.load(os.path.join(os.path.dirname(__file__), "pictures/castledoors.png")).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, 15)*SCALE,
                int(SCALE/2),
            )
        )



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def calculate_new_xy(x,y,speed,angle):
    new_x = x - (speed*math.sin(angle*math.pi/180))
    new_y = y - (speed*math.cos(angle*math.pi/180))
    #print(angle,',',speed*math.sin(angle*math.pi/180) ,',',(speed*math.cos(angle*math.pi/180)), ',',x, new_x,',',y, new_y)
    return new_x, new_y
