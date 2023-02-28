import numpy as np
import pygame as pg
def lineLineIntersect(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        print('vsovneon')
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
    return None


def norm(v):
    v=np.array(v)
    return np.sqrt(np.sum(v**2))


from shapely.geometry import Point
from shapely.geometry import LineString

def normalize(v):
    return v / np.sqrt(np.sum(v**2))

def project_onto(point:tuple[float,float],line_points:list[tuple[float,float]]):
    point = Point(*point)
    line = LineString([*line_points])

    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n)
    return tuple(P)

#print(project_onto(point=(5,5),line_points=[(0,0),(1,0)]))
def draw_text(text:str,screen,pos:tuple[int,int]):
  
    font = pg.font.SysFont(None, 24)
    img = font.render(text, True, (255,255,255))
    screen.blit(img, pos)
    
#computes useful information about the relationship between the player and a particle
#perp_dist = perpendicular distance between the player and the particle's line of trajectory
#moving_towards_player = is the particle moving towards or away from the player?
#time_to_min_dist = how much time until the particle is as close to the player as possible?
#part_on_target = is the player on the particles trajectory? ie will the particle hit the player if the player doesnt move?

def perp_dist_part_player(p,player_position:list,player_rad,draw=False,screen=None):
            partxv,partyv=p.velocity
            partx,party=p.x,p.y
            playx,playy=player_position[0],player_position[1]
            part_dir = normalize(np.array([partxv,partyv]))
            part_dir_points = [(partx,party),(partx+part_dir[0],party+part_dir[1])]
            projected_player = project_onto((playx,playy),part_dir_points)
            part_to_player = [playx-partx,playy-party]
            if draw:
                pg.draw.line(screen,(0,255,0),(playx,playy),projected_player)
            perp_dist = norm([playx-projected_player[0],playy-projected_player[1]])
            moving_towards_player = True if np.dot( np.array(p.velocity), np.array(part_to_player))>0 else False
            time_to_min_dist = norm([projected_player[0]-partx,projected_player[1]-party])/norm(p.velocity)*(1 if moving_towards_player else -1)
            part_on_target = (perp_dist< (player_rad + p.rad))  and moving_towards_player
            return perp_dist, moving_towards_player,time_to_min_dist,part_on_target
        

