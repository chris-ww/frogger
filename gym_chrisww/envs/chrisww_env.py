import pygame
import random
import sys
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os
import math
import numpy as np


SCALE=24
DIM=5
SCREEN_WIDTH = SCALE*DIM
SCREEN_HEIGHT = SCALE*DIM



class Chrisww_gym(gym.Env):
   
    def __init__(self):
        pygame.init()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.zeros((DIM*DIM)),
            np.full((DIM*DIM),2) , dtype=np.int16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player()
        self.door = Door()
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.door)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state=self.get_state()
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)

    def step(self, action):
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player.update(action)
        reward=self.distance-(abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y))-1
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        self.state=self.get_state()
        if(self.distance==0):
            self.done=True
        return np.ndarray.flatten(self.state), reward, self.done,{}
    
    def reset(self):
        pygame.init()
        self.observation_space = spaces.Box(np.zeros((DIM*DIM)),
            np.full((DIM*DIM),2) , dtype=np.int16)
        self.action_space = spaces.Discrete(4)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player()
        self.door = Door()
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.door)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state=self.get_state()
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        return np.ndarray.flatten(self.state)
        
    def render(self, mode='human', close=False):
        self.clock.tick(60)
        pygame.display.flip()

    def close(self):
        pygame.quit()
    
    def get_state(self):
        state=np.zeros((DIM,DIM))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf,(entity.x*SCALE+1,entity.y*SCALE+1))
            state[entity.x,entity.y]=entity.colour
        return state


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([0,255,0])
        self.rect = self.surf.get_rect()
        self.x=random.randint(0,DIM-1)
        self.y=random.randint(0,DIM-1)
        self.colour=1

    def update(self, action):
        if action==0:
            if(self.x<DIM-1):
                self.x+=1
        if action==1:
            if(self.x>0):
                self.x-=1
        if action==2:
            if(self.y<DIM-1):
                self.y+=1
        if action==3:
            if(self.y>0):
                self.y-=1

class Door(pygame.sprite.Sprite):
    def __init__(self):
        super(Door, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([255,255,0])
        self.rect = self.surf.get_rect()
        self.x=random.randint(0,DIM-1)
        self.y=random.randint(0,DIM-1)
        self.colour=2

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([0,0,255])
        self.rect = self.surf.get_rect()
        self.x=10
        self.y=10