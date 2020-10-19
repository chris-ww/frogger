import pygame
import random
import sys
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os
import math
import numpy as np


class Chrisww_gym(gym.Env):
    def __init__(self,**kwargs):
        self.dim=kwargs['dim']
        self.res=kwargs['res']
        try:
            self.scale=self.res/self.dim
        except:
            print("Resolution must be multiple of dimension")
            
        pygame.init()
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.zeros((self.dim*self.dim*2)),
            np.full((self.dim*self.dim*2),True ), dtype=np.bool)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.res,self.res))
        self.player = Player(self.dim,self.scale)
        self.door = Door(self.dim,self.scale)
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.door)
        self.all_sprites.add(self.player)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        self.state=self.get_state(self.scale,self.dim)
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)

    def step(self, action):
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        self.player.update(action,self.dim)
        reward=self.distance-(abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y))-1
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        self.state=self.get_state(self.scale,self.dim)
        if(self.distance==0):
            self.done=True
        return np.ndarray.flatten(self.state), reward, self.done,{}
    
    def reset(self):
        pygame.init()
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.zeros((self.dim*self.dim*2)),
            np.full((self.dim*self.dim*2),True ), dtype=np.bool)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.res,self.res))
        self.player = Player(self.dim,self.scale)
        self.door = Door(self.dim,self.scale)
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.door)
        self.all_sprites.add(self.player)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        self.state=self.get_state(self.scale,self.dim)
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        return np.ndarray.flatten(self.state)
        
    def render(self, mode='human', close=False):
        self.clock.tick(20)
        pygame.display.flip()

    def close(self):
        pygame.quit()
    
    def get_state(self,scale,dim):
        state=np.zeros((dim,dim,2),dtype=np.bool)
        for entity in self.all_sprites:
            self.screen.blit(entity.surf,(entity.x*scale+1,entity.y*scale+1))
            state[entity.x,entity.y,entity.colour]=True
        return state


class Player(pygame.sprite.Sprite):
    def __init__(self,dim,scale):
        super(Player, self).__init__()
        self.surf = pygame.Surface((scale-2, scale-2))
        self.surf.fill([0,255,0])
        self.rect = self.surf.get_rect()
        self.x=random.randint(0,dim-1)
        self.y=random.randint(0,dim-1)
        self.colour=0

    def update(self, action,dim):
        if action==0:
            if(self.x<dim-1):
                self.x+=1
        if action==1:
            if(self.x>0):
                self.x-=1
        if action==2:
            if(self.y<dim-1):
                self.y+=1
        if action==3:
            if(self.y>0):
                self.y-=1

class Door(pygame.sprite.Sprite):
    def __init__(self,dim,scale):
        super(Door, self).__init__()
        self.surf = pygame.Surface((scale-2, scale-2))
        self.surf.fill([255,255,0])
        self.rect = self.surf.get_rect()
        self.x=random.randint(0,dim-1)
        self.y=random.randint(0,dim-1)
        self.colour=1

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([0,0,255])
        self.rect = self.surf.get_rect()
        self.x=10
        self.y=10