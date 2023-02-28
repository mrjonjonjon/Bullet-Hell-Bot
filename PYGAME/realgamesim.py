from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import pygame as pg
import random

import numpy as np
import lineintersectionutil
import player_AI


pg.display.init()
pg.font.init()

screen = pg.display.set_mode((800,600))
SCREEN_WIDTH,SCREEN_HEIGHT=pg.display.get_window_size()


def normalize(v):
    v=np.array(v)
    return v / np.sqrt(np.sum(v**2))
class Particle:
  def __init__(self, coord, rad,velocity=[0,0],bounce=False):
    x,y=coord
    self.x = x
    self.y = y
    self.rad = rad
    self.colour = (255, 0, 0)
    self.thickness = 1
    self.velocity = velocity
    self.bounce=bounce


  def draw(self,display_trajectory=False):
    global screen
    pg.draw.circle(screen, self.colour, (self.x, self.y), self.rad)
    if display_trajectory:
        wx,wy=pg.display.get_window_size()
        #TODO: COMPUTE THIS
        window_lines = [((0,0),(SCREEN_WIDTH,0)),
                        ((SCREEN_WIDTH,0),(SCREEN_WIDTH,SCREEN_HEIGHT)),
                        ((SCREEN_WIDTH,SCREEN_HEIGHT),(0,SCREEN_HEIGHT)),
                        ((0,SCREEN_HEIGHT),(0,0))]
        dist=10*(SCREEN_WIDTH+SCREEN_HEIGHT)
        nx,ny = normalize(np.array(self.velocity))
        my_line = (
            (self.x,self.y),(self.x+dist*(nx),self.y+dist*(ny))
            )
        for wl in window_lines:
            ip= lineintersectionutil.lineLineIntersect(*wl,*my_line) 
            if ip is not None:
                pg.draw.line(screen,(255,255,255),(self.x,self.y),ip)
                return


        #end_pos = (0,0)
       # pg.draw.line(screen, (0,255,0), (self.x,self.y), end_pos)



  def update_position(self,dt):
      self.x+=self.velocity[0]*dt
      self.y+=self.velocity[1]*dt
      if self.bounce:
          if self.x>SCREEN_WIDTH:
              self.x=SCREEN_WIDTH
              self.velocity[0]*=-1
          if self.x<0:
              self.x=0
              self.velocity[0]*=-1

          if self.y>SCREEN_HEIGHT:
              self.y=SCREEN_HEIGHT
              self.velocity[1]*=-1
          if self.y<0:
              self.y=0
              self.velocity[1]*=-1
      
class Player:
  def __init__(self, coord, rad,speed=5,colour=(255,0,0)):
    x,y=coord
    self.x = x
    self.y = y
    self.rad = rad
    self.colour = colour
    self.thickness = 1
    self.speed = speed
    self.velocity=[0,0]


  def draw(self,display_trajectory=False):
    global screen
    pg.draw.circle(screen, self.colour, (self.x, self.y), self.rad)

  def set_velocity(self):
        keys = pg.key.get_pressed()  #checking pressed keys
        self.velocity=np.array([0,0])
        if keys[pg.K_LEFT]:
            self.velocity = np.add(self.velocity, normalize(np.array([-1,0]))*self.speed*dt)
            
        if keys[pg.K_RIGHT]:
            self.velocity =  np.add(self.velocity,normalize(np.array([1,0]))*self.speed*dt)

        if keys[pg.K_UP]:
            self.velocity = np.add(self.velocity,normalize(np.array([0,-1]))*self.speed*dt)
        if keys[pg.K_DOWN]:
            self.velocity = np.add(self.velocity,normalize(np.array([0,1]))*self.speed*dt)

      
  def update_position(self,dt):
        self.set_velocity()
        
        player.x +=self.velocity[0]
        player.y +=self.velocity[1]
      





def spawn_particles(num,velocty_multiplier=1,bounce=False):
    parts=[]
    for i in range(num):
        parts.append(
            Particle(
            coord=(random.randrange(0,400),random.randrange(0,400)), 
            rad=5,
            velocity=[velocty_multiplier*(random.random()-0.5),velocty_multiplier*(random.random()-0.5)],
            bounce=bounce
            )
            )
        

    return parts




######### G A M E #############
FPS = 60
clock = pg.time.Clock()

running=True
player = Player(coord=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2),rad=20,speed=0.3,colour=(0,0,255))


parts=spawn_particles(1,velocty_multiplier=0.2,bounce=True)





while running:
        screen.fill((0,0,0))
        
        dt=clock.tick(FPS)
        for event in pg.event.get():
             if event.type==pg.QUIT:
                running=False
        
        player.update_position(dt)
        player.draw() 
        #model = player_AI.model(player,parts,rad=5)
        #player_state = player_AI.state(player,parts)
        #action_scores = {action: model.Q(player_state,action,dt) for action in player_AI.ACTIONS}
        #lineintersectionutil.draw_text(f'SCORE : {player_state.U()}',screen,(SCREEN_WIDTH/2,50))
        for p in parts:
            p.update_position(dt)
            p.draw(True)
            
            #perp_dist,moving_towards_player,time_to_min_dist,part_on_target = perp_dist_part_player(p,player,draw=True,screen=screen)
            #draw_text(f'time_to_min_dist :{round(time_to_min_dist/1000,2)}  ,  {part_on_target}',screen,(SCREEN_WIDTH/2,10))
            
           
        pg.display.update()