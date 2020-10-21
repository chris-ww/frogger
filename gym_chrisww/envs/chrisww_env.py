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
        self.mines_count=kwargs['mines']
        self.r_mines=kwargs['r_mines']
        self.r_door=kwargs['r_door']
        self.r_dist=kwargs['r_dist']
        try:
            self.scale=self.res/self.dim
        except:
            print("Resolution must be multiple of dimension")
            
        pygame.init()
        x_list=[]
        y_list=[]
        x_list,y_list=self.generate_xy(2+self.mines_count)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.zeros((self.dim*self.dim*3)),
            np.full((self.dim*self.dim*3),True ), dtype=np.bool)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.res,self.res))
        self.player = Player(self.scale,self.dim,x_list[0],y_list[0])
        self.door = Door(self.scale,x_list[1],y_list[1],self.r_door)
        self.mines = pygame.sprite.Group()
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.door)
        self.all_sprites.add(self.player)
        for i in range(self.mines_count):
            new_mine = Mine(self.scale,x_list[i+2],y_list[i+2],self.r_mines)
            self.mines.add(new_mine)
            self.all_sprites.add(new_mine)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        self.state,done,bonus=self.get_state()
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)

    def step(self, action):
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        reward=-(self.distance-(abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y))-1)*self.r_dist
        reward+=self.player.update(action,self.dim)
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        self.state, self.done, bonus =self.get_state()
        reward+=bonus
        return np.ndarray.flatten(self.state), reward, self.done,{}
    
    def reset(self):
        pygame.init()
        x_list=[]
        y_list=[]
        x_list,y_list=self.generate_xy(2+self.mines_count)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.zeros((self.dim*self.dim*3)),
            np.full((self.dim*self.dim*3),True ), dtype=np.bool)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.res,self.res))
        self.player = Player(self.scale,self.dim,x_list[0],y_list[0])
        self.door = Door(self.scale,x_list[1],y_list[1],self.r_door)
        self.mines = pygame.sprite.Group()
        self.done=False
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.door)
        self.all_sprites.add(self.player)
        for i in range(self.mines_count):
            new_mine = Mine(self.scale,x_list[i+2],y_list[i+2],self.r_mines)
            self.mines.add(new_mine)
            self.all_sprites.add(new_mine)
        self.screen.fill([0, 0, 0])
        self.screen = pygame.display.set_mode((self.res, self.res))
        self.state,done,bonus=self.get_state()
        self.distance=abs(self.player.x-self.door.x) +abs(self.player.y-self.door.y)
        return np.ndarray.flatten(self.state)
    
    def render(self, mode='human', close=False):
        self.clock.tick(20)
        pygame.display.flip()

    def close(self):
        pygame.quit()
    
    def get_state(self):
        state=np.zeros((self.dim,self.dim,3),dtype=np.bool)
        done=False
        bonus=0
        for entity in self.all_sprites:
            self.screen.blit(entity.surf,(entity.x*self.scale+1,entity.y*self.scale+1))
            state[entity.x,entity.y,entity.colour]=True
            if(entity.x==self.player.x and entity.y==self.player.y and entity.colour!=0):
                done=True
                bonus=entity.bonus
        return state, done, bonus
    
    def generate_xy(self,n):
        total=self.dim*self.dim
        loc=np.array(random.sample(range(total),n))
        y_list=loc//self.dim
        x_list=loc % self.dim
        return x_list,y_list
                

class Player(pygame.sprite.Sprite):
    def __init__(self,scale,dim,x,y):
        super(Player, self).__init__()
        self.surf = pygame.Surface((scale-2, scale-2))
        self.surf.fill([0,255,0])
        self.rect = self.surf.get_rect()
        self.x=x
        self.y=y
        self.colour=0
        self.visited=np.zeros((dim,dim))

    def update(self, action,dim):
        reward=0
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
        reward=-self.visited[self.x,self.y]
        self.visited[self.x,self.y]+=1
        return reward

class Door(pygame.sprite.Sprite):
    def __init__(self,scale,x,y,bonus):
        super(Door, self).__init__()
        self.surf = pygame.Surface((scale-2, scale-2))
        self.surf.fill([255,255,0])
        self.rect = self.surf.get_rect()
        self.x=x
        self.y=y
        self.colour=1
        self.bonus=bonus

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.Surface((22, 22))
        self.surf.fill([0,0,255])
        self.rect = self.surf.get_rect()
        self.x=10
        self.y=10

class Mine(pygame.sprite.Sprite):
    def __init__(self,scale,x,y,bonus):
        super(Mine, self).__init__()
        self.surf = pygame.Surface((scale-2, scale-2))
        self.surf.fill([255,0,0])
        self.rect = self.surf.get_rect()
        self.x=x
        self.y=y
        self.colour=2
        self.bonus=bonus
