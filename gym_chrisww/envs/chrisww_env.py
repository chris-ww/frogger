import pygame
import random
import sys
import gym
from gym import error, spaces, utils
from gym.utils import seeding

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
        self.level=1
        self.score=0
        self.lives=5
        self.scale=16
        self.clock = pygame.time.Clock()
        self.BackGround = Background('map0.png', [0,0])
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
        pygame.init()


    def step(self, action):    
        pressed_keys = action
        self.player.update(pressed_keys)
    
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.BackGround.image, self.BackGround.rect)

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
            
        if pygame.sprite.spritecollide(self.player, self.doors, dokill=False):
           self.player.kill()
    
        self.clock.tick(60)
        self.render()
        
    
    def reset(self):
        self.level=1
        self.time=0
        self.score=0
        self.lives=5
    
    def render(self, mode='human', close=False):
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image_still = pygame.image.load("rabbit_forward_still.png").convert_alpha()
        self.image_run1 = pygame.image.load("rabbit_forward_half.png").convert_alpha()
        self.image_run2 = pygame.image.load("rabbit_forward_jump.png").convert_alpha()
        self.surf = self.image_still
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))
        self.rect = self.surf.get_rect(center=(int(SCREEN_SIZE/2),int(SCALE*15.5)))
        self.cooldown=0
        self.angle=0

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if(self.cooldown <= 0):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -16)
                self.cooldown = 5
                self.angle=0
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 16)
                self.cooldown = 5
                self.angle=180
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-16, 0)
                self.cooldown = 5
                self.angle=90
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(16, 0)
                self.cooldown = 5
                self.angle=270
        elif(self.cooldown >=1):
            self.cooldown = self.cooldown -1
        if(self.cooldown >=3):
            self.surf = self.image_run2
        else:
            self.surf = self.image_still
        self.surf = pygame.transform.rotate(self.surf,self.angle)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))


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
        self.surf = pygame.image.load("blue_van.png").convert_alpha()
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
        self.surf = pygame.image.load("castledoors.png").convert_alpha()
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
    