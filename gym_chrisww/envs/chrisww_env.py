import pygame
import random
import sys
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os
import math


SCALE=24
SCREEN_WIDTH = SCALE*20
SCREEN_HEIGHT = SCALE*20


class Chrisww_gym(gym.Env):
   
    def __init__(self):
        pygame.init()
        self.action_space = spaces.Discrete(4)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        


    def step(self, action):
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player.update(action)

        for entity in self.all_sprites:
            self.screen.blit(entity.surf,(entity.x*SCALE+1,entity.y*SCALE+1))
        self.clock.tick(60)
        
    
    def reset(self):
        pygame.init()
        self.action_space = spaces.Discrete(4)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def render(self, mode='human', close=False):
        pygame.display.flip()

    def close(self):
        pygame.quit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([0,255,0])
        self.rect = self.surf.get_rect()
        self.x=0
        self.y=0


    def update(self, action):
        if action==0:
            if(self.x<19):
                self.x+=1
        if action==1:
            if(self.x>1):
                self.x-=1
        if action==2:
            if(self.y<19):
                self.y+=1
        if action==3:
            if(self.y>1):
                self.y-=1

