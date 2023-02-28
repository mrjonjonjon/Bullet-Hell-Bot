import pygame
#initilaize
pygame.display.init()
pygame.font.init()

#create screen
screen = pygame.display.set_mode((800,600))

#game icon
pygame.display.set_caption("BULLET HELL")
#icon = pygame.image.load('img.png')
#pygame.display.set_icon(icon)

#pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#player
playerimg=pygame.image.load('player.png')

playerx=0
playery=0
playerxspeed=playeryspeed= 4
IMAGE = pygame.Surface((100, 60))
IMAGE.fill(pygame.Color('sienna2'))
pygame.draw.circle(IMAGE, pygame.Color('royalblue2'), (50, 30), 20)

bulletimg=pygame.image.load('bullet.png')
bulletx=bullety=playerxspeed
#ready=cant see bullet
#fire=bullet is firing
bullet_state='ready'
bullet_speed = (3,3)
def fire_bullet(x,y):
     global bullet_state
     bullet_state='fire'
     screen.blit(bulletimg,(x,y))


def player(x,y):
    #screen.blit(playerimg,(x,y))
    screen.blit(IMAGE, (x, y))


FPS = 60
clock = pygame.time.Clock()
running=True
#game loop
while running:
        dt=clock.tick(FPS)
        screen.fill((0,255,255))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            playerx -=playerxspeed*dt
        if keys[pygame.K_RIGHT]:
            playerx+=playerxspeed*dt
        if keys[pygame.K_UP]:
             playery-=playeryspeed*dt
        if keys[pygame.K_DOWN]:
             playery+=playeryspeed*dt
        if keys[pygame.K_SPACE]:
             fire_bullet(playerx,playery)
      

        if playerx<=0:
             playerx=0
        elif playerx+100>=800:
            playerx=800-100  
        if playery<=0:
             playery=0
        elif playery+60>=600:
             playery=600-60

        #bullet movement
        if bullet_state is 'fire':
             fire_bullet(playerx,bullety)
        player(playerx,playery)
        pygame.display.update()