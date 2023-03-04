import pygame
from pygame import *
from realgamesim import *
from raycasting import *
if __name__=='__main__':
        game = Game(FPS=100,AI_control=False,num_particles=1)
        ray = Ray([0,0],[1,1],500)
       
        
        while game.running:
            game.step() 
            rects = [p.rect for p in game.parts]
            ray.cast(10,game.screen,rects)
            game.render()