
#GET VALUE OF STATE
import lineintersectionutil
#[a*b for a,b in zip(lista,listb)]
import numpy as np
ACTIONS =[ 
           [0,0], # DONT MOVE
           [0,-1], # MOVE UP
           [0,1], # MOVE DOWN
           [-1,0],# MOVE LEFT
           [1,0], # MOVE RIGHT
           
           [1,1],# MOVE RIGHT AND DOWN
           [1,-1],# MOVE RIGHT AND UP
           [-1,1],#MOVE LEFT AND DOWN
           [-1,-1]#MOVE LEFT AND UP
           
           ]
class state:
    def __init__(self,player,particles) -> None:
       self.player=player
       self.particles = particles
   
   
   
   
   
#parametrized model
class model:
  def __init__(self,all_possible_states,all_possible_actions,rad) -> None:
       # self.all_possible_states=all_possible_states
        self.all_possible_actions = all_possible_actions
        #radius in which particles are "seen" by the player
        self.rad=rad
    
  def Q(self,state:state,action:list,dt):
      
      player,particles = state.player,state.particles
      player_speed=np.array(player.speed)
      action_direction = lineintersectionutil.normalize(np.array(action))
      
      future_player_position = np.add(
           np.array(player.x,player.y),
           player_speed * action_direction * dt
          ) 
      #simple model. only care if we're on a particle trajectory
      res=0
      for particle in particles:
            perp_dist,moving_towards_player,time_to_min_dist,part_on_target = lineintersectionutil.perp_dist_part_player(particle,player_position=[future_player_position[0],future_player_position[1]],player_rad=player.rad,draw=False,screen=None)
            if part_on_target:
                res-=1
      return res

      
  def U(self,state:state):
    player,particles=state.player,state.particles
    
    score=0
    for particle in particles:
        perp_dist,moving_towards_player,time_to_min_dist,part_on_target = lineintersectionutil.perp_dist_part_player(particle,player,draw=False,screen=None)
        if part_on_target:
            score -= 1/max(0.1,time_to_min_dist)
        else:
           score += max(0,-time_to_min_dist)
    return score
            
            #d=s*t ... t=d/s

