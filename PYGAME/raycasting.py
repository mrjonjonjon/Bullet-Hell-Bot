import numpy as np
import lineintersectionutil
from numpy import array
import pygame as pg
class Ray:
    def __init__(self,start_point,dir,dist) -> None:
        
        self.start_point=array(start_point)
        self.dist=dist
        self.dir=lineintersectionutil.normalize(dir)
        self.end_point = self.start_point + self.dir*self.dist
        #self.end_point = array(end_point)
        #dir = array(end_point) - array(start_point)
        #self.dir = lineintersectionutil.normalize(dir)
        
    def cast(self,segment_length=10,screen=None,parts=None):
        collision_rects = [p.rect for p in parts]
        prev_point = self.start_point
       
        #segment_length = lineintersectionutil.norm(array(self.end_point-self.start_point))/num_divs
        num_divs = lineintersectionutil.norm(array(self.end_point-self.start_point))/segment_length
        for i in range(int(num_divs)):
            
            next_point = prev_point + self.dir*segment_length
            if screen is not None:
                pg.draw.line(screen,(0,255,0),list(self.start_point),list(next_point),width=1)
                
                
            if collision_rects is not None:
                for rect in collision_rects:
                    if rect is None:
                        continue
                    if rect.collidepoint(tuple(next_point)):
                        #print('nriufnbriub3')
                        return rect,lineintersectionutil.norm(next_point-self.start_point)
          
            #print("COLOR CHANGED")
        
            prev_point=next_point
        return None,self.dist
            