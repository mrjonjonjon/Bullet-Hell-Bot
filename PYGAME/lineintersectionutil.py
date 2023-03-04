import numpy as np
import pygame as pg
def element_wise_mul(l1,l2):
    res= [a*b for a,b in zip(l1,l2)]
    return res

def scale_list(l1,s):
    res = [s*e for e in l1]
    return res
def lineLineIntersect(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        #print('vsovneon')
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
    if norm(v)==0:
        return v
    return v / norm(v)

#projects point (x,y) onto line defined by points (p0,p1) and (q0,q1)
def project_onto(point:tuple,line_points:list):
    point = Point(*point)
    line = LineString([*line_points])
    #print(f"POINT {point}\n")
    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n)
    return tuple(P)

def get_distance_from_screen_edge(point:list,SCREEN_WIDTH,SCREEN_HEIGHT,screen=None,player=None):
    window_lines = [[(0,0),(SCREEN_WIDTH,0)],
                        [(SCREEN_WIDTH,0),(SCREEN_WIDTH,SCREEN_HEIGHT)],
                        [(SCREEN_WIDTH,SCREEN_HEIGHT),(0,SCREEN_HEIGHT)],
                        [(0,SCREEN_HEIGHT),(0,0)]
                        ]
     
    my_point = list(point)
    
    res=1000000000000000
    minline=None
    for wl in window_lines:
        projected_point = project_onto(my_point,wl)
        perp_line = [projected_point[0] - point[0],projected_point[1]-point[1]]
        if norm(np.array(perp_line))<res:
            res=min(res, norm(np.array(perp_line)))
            minline = projected_point
        
    if screen is not None:
            pg.draw.line(screen,(0,255,0),(point[0],point[1]),(minline[0],minline[1]))
    return res
    
#print(project_onto(point=(5,5),line_points=[(0,0),(1,0)]))
def draw_text(text:str,screen,pos:tuple):
  
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
        


def random_color():
    color = list(np.random.choice(range(256), size=3))
    return color
