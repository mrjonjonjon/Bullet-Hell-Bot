import pygame
from pygame import *
from realgamesim import Game

if __name__=='__main__':
        game = Game(FPS=30,AI_control=False,num_particles=1,velocity_multiplier=0.5)
        while game.running:
            game.step()
            game.render()