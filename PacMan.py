# PacMan from scratch

import copy
from pacman_board_design import boards #importing board from the other file #pyhton file name cannot have space else cannot import
import pygame
import math   # to draw arcs of walls (corners)

pygame.init()

# Game dimensions
WIDTH = 700
HEIGHT = 750

# Display 
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('MaZe NaViGaToR')        #to set name of window
pygame.display.set_icon(pygame.image.load(f'window_icon/game_icon.png'))     #changed window ion/picture also 

# timer to control speed of game 
timer = pygame.time.Clock()

fps=60 # max speed game can run on any device

# for score display and game over etc..
font = pygame.font.Font('freesansbold.ttf', 20)  #freesanshold cuz standard on windows installation of python

level = copy.deepcopy(boards)  #creating levels of the game #copy original board so that source stay intact when restart elso pellets dont appear back 
colour = 'blue' # lvl 1 everything basically blue , can change for other level 

PI = math.pi # like height and width wont be changing

#player images list
player_images = []
for i in range(1,5): # 1 inclusive 5 not inclusive so run 1-4
    player_images.append(pygame.transform.scale(pygame.image.load(f'player_images/{i}.png'), ( 30, 30)))    # append obv to add to the list #transform load image #scale scale img as it is 1 square larger #load specifying the file to load in #f string to use the i in the for loop to load in the right img #named img in num for that reason (i) #30,30 size to scale down to

blinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/red.png'), ( 30, 30))          #blinky name of red ghost in the game
pinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/pink.png'), ( 30, 30))           #pink one
inky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/blue.png'), ( 30, 30))            #blue one
clyde_img = pygame.transform.scale(pygame.image.load(f'ghost_images/orange.png'), ( 30, 30))     #clyde orange one name
spooked_img = pygame.transform.scale(pygame.image.load(f'ghost_images/powerup.png'), ( 30, 30))      #blue when power up is active
dead_img = pygame.transform.scale(pygame.image.load(f'ghost_images/dead.png'), ( 30, 30))       #eyes only cuz theyve been eaten

player_x = 325   #player x,y coordinates starting position by trial and error
player_y = 375 
direction = 0

blinky_x = 330           # ghosts initial position
blinky_y = 245
blinky_direction = 0

pinky_x = 290
pinky_y = 308
pinky_direction = 2

inky_x = 370
inky_y = 308
inky_direction = 2

clyde_x = 330
clyde_y = 308
clyde_direction = 2


counter = 0
flicker = False
# Right, Left, UP, Down
turns_allowed = [False, False, False, False] 
direction_command = 0
player_speed = 2

score = 0
high_score = 0
powerup = False
power_counter = 0

eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y),]           #tile ghosts are searching for

blinky_dead = False     # variable to track their death
pinky_dead = False
inky_dead= False 
clyde_dead = False 

blinky_box = False     # variable to track if they're in box
pinky_box = False
inky_box= False 
clyde_box = False 

ghost_speeds = [3, 2, 2, 2] 


moving = False
startup_counter = 0
lives = 3

game_over = False
game_won = False

power_soundplay = False

class Ghost:            #class so that fuction works for all ghosts at once
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id ) :   #all have these and give them id to diff them in case need to use anything out of the list
        self.x_pos = x_coord           #so that can use  variable in innit outside also 
        self.y_pos = y_coord

        self.center_x = self.x_pos + 15
        self.center_y = self.y_pos + 15

        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id

        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()                                               # outline of the ghosts collision box to know when player hits a ghost  also draw every single frames for the ghosts

    def draw(self) :                                                       # drawing ghost
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead) :
            screen.blit(self.img, (self.x_pos, self.y_pos))                 #ghost can be based image
        elif powerup and not self.dead and not eaten_ghost[self.id] :     
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else :
            screen.blit(dead_img, (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 10, self.center_y - 10), (25, 25) )            #rectangle thats the ghost hit box when hit ghost and player die #center to start , 36 36 how wide and tall it is

        return ghost_rect
    
    def check_collisions(self) : 
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 8  #fudge factor
    # R, L , U ,D
        self.turns = [False, False, False, False]
        if self.center_x // 30 < 29 :                                         #0 so dont get error going off sreen
            if level [(self.center_y - num3) // num1][self.center_x // num2] == 9:   #going through door. if going up and its ghost door
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead):
                self.turns[1] = True                                             #checking if can go left

            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                or level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead):
                self.turns[0] = True                                       # checking if can go right

            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                or level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead):
                self.turns[3] = True                                            

            if level[(self.center_y - num3)// num1][self.center_x // num2] < 3 \
                or level[(self.center_y - num3)// num1][self.center_x // num2] == 9 and (self.in_box or self.dead):
                self.turns[2] = True 

            if self.direction == 2 or self.direction == 3 :
                if  5 <= self.center_x % num2 <= 16:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[3] = True                             #checkinng to see if we can go down

                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[2] = True                        # checking if can go up

                if  5 <= self.center_y % num1 <= 16:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[1] = True                             #checkinng to see if we can go left

                    if level[self.center_y // num1][min((self.center_x + num2) // num2, 29)] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)) : #min 29 , cuz its getting 31 tiles and ghost crashing tunnel so i'll prevent 3 ghost from using tunnel and the turn around at last index 29 
                        self.turns[0] = True              #checkinng to see if we can go right


            if self.direction == 0 or self.direction == 1 :
                if  5 <= self.center_x % num2 <= 16:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[3] = True                             #checkinng to see if we can go down

                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[2] = True                        # checking if can go up

                if  5 <= self.center_y % num1 <= 16:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[1] = True                             #checkinng to see if we can go left

                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)) :
                        self.turns[0] = True 

        else : 
            self.turns[0] = True
            self.turns[1] = True

        if 250 < self.x_pos < 410 and 280 < self.y_pos < 350 :     #x position and y position bet these values aka ghost box
            self.in_box = True
        else:
            self.in_box = False 

        return self.turns, self.in_box 
    #clyde used for blinky who turns towards player at any opportunity
    def move_clyde(self) :
        # r, l, u, d
        # blinky is going to turn whenever advantageous for pursuit
        if self.direction == 0:                                    # if going right and target is further right 
            if self.target[0] > self.x_pos and self.turns[0]:      
                self.x_pos += self.speed                           #then keep going right (default move) if can
            elif not self.turns[0]:                              # going right but then collide with something on right and target is right
                if self.target[1] > self.y_pos and self.turns[3]:   #target below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:   #target is higher and I just collide on the right
                    self.direction = 2
                    self.y_pos -= self.speed                          # to move up
                elif self.target[0] < self.x_pos and self.turns[1]:   # target behind and allow to go left
                    self.direction = 1  
                    self.x_pos -= self.speed                          #if direct movement allow (all of the above)
                elif self.turns[3]:                            #trying to turn down if cannot (target no direct way)
                    self.direction = 3                 
                    self.y_pos += self.speed
                elif self.turns[2]:                             #try up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:                            #try left  
                    self.direction = 1
                    self.x_pos -= self.speed        # was going right then collide and target is right , so try diff directions
            elif self.turns[0]:                                        #going right, can turn right but target not right
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:       #keep checking if can go up or down based on if target up or below (3 & 2)
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
       
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:    #going left but at anypoint can turn down to go after target then turn down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:   # going left, target left so keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]:                            #want to go left but collide with something
                if self.target[1] > self.y_pos and self.turns[3]:   
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
       
        elif self.direction == 2:                                 #if going up
            if self.target[0] < self.x_pos and self.turns[1]:     # can turn left then go left
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:   # going up terget is up then keep going up 
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:       
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:   #downwards
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed                                      #if target left go left if right go right else keep going up
                else:
                    self.y_pos -= self.speed
        
        elif self.direction == 3:                                   #going down
            if self.target[1] > self.y_pos and self.turns[3]:            #check to see if can continue down
                self.y_pos += self.speed                             # can turn right cuz target right then go
            elif not self.turns[3]:                               #if cannot continue down
                if self.target[0] > self.x_pos and self.turns[0]:  
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  #hit something down cannot left or right then go back up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:   
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #keep going down
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -28:
            self.x_pos = 666
        elif self.x_pos > 666:
            self.x_pos = -28
        return self.x_pos, self.y_pos, self.direction
 #pinky turns towards player on collision
    def move_pinky(self) :
        # r, l, u, d
        # pinky is going to turn whenever colliding with walls and go to target else continue straight 
        if self.direction == 0:                                    # if going right and target is further right 
            if self.target[0] > self.x_pos and self.turns[0]:      
                self.x_pos += self.speed                           #then keep going right (default move) if can
            elif not self.turns[0]:                              # going right but then collide with something on right and target is right
                if self.target[1] > self.y_pos and self.turns[3]:   #target below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:   #target is higher and I just collide on the right
                    self.direction = 2
                    self.y_pos -= self.speed                          # to move up
                elif self.target[0] < self.x_pos and self.turns[1]:   # target behind and allow to go left
                    self.direction = 1  
                    self.x_pos -= self.speed                          #if direct movement allow (all of the above)
                elif self.turns[3]:                            #trying to turn down if cannot (target no direct way)
                    self.direction = 3                 
                    self.y_pos += self.speed
                elif self.turns[2]:                             #try up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:                            #try left  
                    self.direction = 1
                    self.x_pos -= self.speed        # was going right then collide and target is right , so try diff directions
           
            elif self.turns[0]:                                        #if can go right then go right
                    self.x_pos += self.speed
       
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:   # target left behind ghost and going left keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]:                            #else collide on left 
                if self.target[1] > self.y_pos and self.turns[3]:   
                    self.direction = 3                              #check if can go down if can then go
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2                              #check up if can then go
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0                              #same for right   #all to pursue target
                    self.x_pos += self.speed
                elif self.turns[3]:                            #if cannot follow target then 3,2,0
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                    self.x_pos -= self.speed                 #keep going left if can      
        elif self.direction == 2:                                 #if going up
            if self.target[1] < self.y_pos and self.turns[2]:   # going up terget is up then keep going up 
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:   #collide cannot go up check right if can then go    
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #same left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:   #same down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:                 #if collide while going up instead of checking left right,just go back down first
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                    self.y_pos -= self.speed       #otherwise if can up then keep go up
        
        elif self.direction == 3:                                   #going down
            if self.target[1] > self.y_pos and self.turns[3]:            #check to see if can continue down
                self.y_pos += self.speed                             # can turn right cuz target right then go
            elif not self.turns[3]:                               #if cannot continue down
                if self.target[0] > self.x_pos and self.turns[0]:  
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  #hit something down cannot left or right then go back up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1                     # clyde 2,1,0 pinky 2,0,1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                    self.y_pos += self.speed
        if self.x_pos < -28:
            self.x_pos = 666
        elif self.x_pos > 666:
            self.x_pos = -28
        return self.x_pos, self.y_pos, self.direction   
 #right left turn on collision if player on right or left up down turn when can to go after player
    def move_inky(self) :
        # r, l, u, d
        # inky turns up or down at any point to pursue but left and right only on collision
        if self.direction == 0:                                    # if going right and target is further right 
            if self.target[0] > self.x_pos and self.turns[0]:      
                self.x_pos += self.speed                           #then keep going right (default move) if can
            elif not self.turns[0]:                              # going right but then collide with something on right and target is right
                if self.target[1] > self.y_pos and self.turns[3]:   #target below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:   #target is higher and I just collide on the right
                    self.direction = 2
                    self.y_pos -= self.speed                          # to move up
                elif self.target[0] < self.x_pos and self.turns[1]:   # target behind and allow to go left
                    self.direction = 1  
                    self.x_pos -= self.speed                          #if direct movement allow (all of the above)
                elif self.turns[3]:                            #trying to turn down if cannot (target no direct way)
                    self.direction = 3                 
                    self.y_pos += self.speed
                elif self.turns[2]:                             #try up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:                            #try left  
                    self.direction = 1
                    self.x_pos -= self.speed        # was going right then collide and target is right , so try diff directions
            elif self.turns[0]:                                        #going right, can turn right but target not right
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:       #keep checking if can go up or down based on if target up or below (3 & 2)
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
       
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:    #going left but at anypoint can turn down to go after target then turn down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:   # going left, target left so keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]:                            #want to go left but collide with something
                if self.target[1] > self.y_pos and self.turns[3]:   
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
       
        elif self.direction == 2:                                 #if going up
            if self.target[1] < self.y_pos and self.turns[2]:   # going up terget is up then keep going up #removed target[0] found in clyde
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:    #right     
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:   #downwards
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed      #going down and make sense to turn to pursue target,skip and keep going down #change from clyde
        
        elif self.direction == 3:                                   #going down
            if self.target[1] > self.y_pos and self.turns[3]:            #check to see if can continue down
                self.y_pos += self.speed                             # can turn right cuz target right then go
            elif not self.turns[3]:                               #if cannot continue down
                if self.target[0] > self.x_pos and self.turns[0]:  
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  #hit something down cannot left or right then go back up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:                     #change from clyde #going up keep up no matter target on right or left
                self.y_pos += self.speed
        if self.x_pos < -28:
            self.x_pos = 666
        elif self.x_pos > 666:
            self.x_pos = -28
        return self.x_pos, self.y_pos, self.direction
  # blinky used for clyde .. turns left or right whenever can to fllw player turns up or down only on collision
    def move_blinky(self) :
        # r, l, u, d
        # clyde is going to turn left or right whenever advantageous but up or down only on collision
        if self.direction == 0:                                    # if going right and target is further right 
            if self.target[0] > self.x_pos and self.turns[0]:      
                self.x_pos += self.speed                           #then keep going right (default move) if can
            elif not self.turns[0]:                              # going right but then collide with something on right and target is right
                if self.target[1] > self.y_pos and self.turns[3]:   #target below and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:   #target is higher and I just collide on the right
                    self.direction = 2
                    self.y_pos -= self.speed                          # to move up
                elif self.target[0] < self.x_pos and self.turns[1]:   # target behind and allow to go left
                    self.direction = 1  
                    self.x_pos -= self.speed                          #if direct movement allow (all of the above)
                elif self.turns[3]:                            #trying to turn down if cannot (target no direct way)
                    self.direction = 3                 
                    self.y_pos += self.speed
                elif self.turns[2]:                             #try up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:                            #try left  
                    self.direction = 1
                    self.x_pos -= self.speed        # was going right then collide and target is right , so try diff directions
            elif self.turns[0]:                                        #going right, can turn right but target not right
                self.x_pos += self.speed   #change from clyde, continue right
       
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:    #going left but at anypoint can turn down to go after target then turn down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:   # going left, target left so keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]:                            #want to go left but collide with something
                if self.target[1] > self.y_pos and self.turns[3]:   
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:                   #change from clyde
                self.x_pos -= self.speed
       
        elif self.direction == 2:                                 #if going up
            if self.target[0] < self.x_pos and self.turns[1]:     # can turn left then go left
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:   # going up terget is up then keep going up 
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:       
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:   #downwards
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed                                      #if target left go left if right go right else keep going up
                else:
                    self.y_pos -= self.speed
        
        elif self.direction == 3:                                   #going down
            if self.target[1] > self.y_pos and self.turns[3]:            #check to see if can continue down
                self.y_pos += self.speed                             # can turn right cuz target right then go
            elif not self.turns[3]:                               #if cannot continue down
                if self.target[0] > self.x_pos and self.turns[0]:  
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  #hit something down cannot left or right then go back up
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:   
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:   #keep going down
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -28:
            self.x_pos = 666
        elif self.x_pos > 666:
            self.x_pos = -28
        return self.x_pos, self.y_pos, self.direction   

def draw_scoreboard() :
    score_text = font.render(f'Score:{score}', True, 'white')  #f string say score and display {score} variable #true prt smooth out edges 
    screen.blit(score_text, (10,720))                   #blit means block transfer basically put on screen
    highscore_text = font.render(f'High Score:{high_score}', True, 'white')  #f string say score and display {score} variable #true prt smooth out edges 
    screen.blit(highscore_text, (260,710))
    if powerup :                              #powerup active red circle appears next to score
        pygame.draw.circle(screen, 'red', (130,730), 8)

    for i in range (lives) :                                    #lives shown using pacman img
        screen.blit(pygame.transform.scale(player_images[0], (20,20)), (500 + i * 30 , 710))  # scale img 20,20 smaller than character, 450pix x-axis = i for num of lives *30pix spacing bet each img, 715pix down y-axis

    if game_over :
        gameover_text = font.render('GAME OVER !', True, 'red') #red colour true->anti-aliase(smooth edges)
        screen.blit(gameover_text, (277,315))
        spacebar_text = font.render('spacebar to restart', True, 'yellow') 
        screen.blit(spacebar_text, (252,535))

    if game_won :
        gameover_text = font.render('VICTORY !', True, 'green')
        screen.blit(gameover_text, (297,315))
        spacebar_text = font.render('spacebar to continue', True, 'yellow')
        screen.blit(spacebar_text, (241,535))

    if startup_counter < 240 and not game_over and not game_won :  #making ready sign everytime starting from start position
        ready_text = font.render(' READY !', True, 'yellow')
        screen.blit(ready_text, (300,345))

def check_collisions(scor, power, power_count, eaten_ghosts) :
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)

    eat_alt = True    #alternate pellets sound
    eat1 = pygame.mixer.Sound('pacman_eat1.mp3')
    eat1.set_volume(0.2)

    eat2 = pygame.mixer.Sound('pacman_eat2.mp3')
    eat2.set_volume(0.2)

    if 0 < player_x < 670 : 
        if level[center_y // num1] [center_x // num2] == 1 :      #checking where center is cuz center mounth eat food
            level[center_y // num1] [center_x // num2] = 0        #now eaten food 1 turns to black tile 0
            scor += 10
           
            if eat_alt:
                eat1.play()
            else:
                eat2.play()

            eat_alt = not eat_alt  # Switch sound for next pellet

        if level[center_y // num1] [center_x // num2] == 2 :      
            level[center_y // num1] [center_x // num2] = 0 
            scor += 50
            power = True
            power_count = 0  #need to reset everytime eat a powerup so like get full powerup counter like eat a 2nd before 1st one finish
            eaten_ghosts = [False, False, False, False]                #ghost that have been eaten per powerup

            power_sound.stop()        #for sound to play everytime pellets is eaten
            power_sound.play(-1)
            

    return scor, power, power_count, eaten_ghosts 

def draw_board():    
    num1 = ((HEIGHT - 50) // 32)              # -(minus) 50 cuz 50 pixel bottom for score etc.. # //(divide) 32 cuz board in design board thing has 32 vertical 
    num2 = (WIDTH // 30)                      # // (divide) by 30 cuz 30 horizontal in board    # ' // ' is floor division , it divide and gives in integer dirrectly (round up to nearest whole num)
    for i in range(len(level)):               # i in range length of level (iterate through every single row)
        for j in range (len(level[i])):       # iterate through every single column inside that specific row
            if level[i][j] == 1 :             # tile 0 is just black pixel (background already black so skip)
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 4)  # j y-coordinate i x-coordinate centering the dot '4' is size of dot  
            if level[i][j] == 2 and not flicker :             # big dot #so that disappear when power up active
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 10) 
            if level[i][j] == 3 :             # vertical blue line 
                pygame.draw.line(screen, colour, (j * num2 + (0.5*num2), i * num1),(j * num2 + (0.5*num2), i * num1 + num1), 3) #2 times cuz connecting dots top n btom
            if level[i][j] == 4 :             # horizontal blue wall
                pygame.draw.line(screen, colour, (j * num2 , i * num1  + (0.5*num1)),(j * num2 + num2 , i * num1 + (0.5*num1)), 3)

            if level[i][j] == 9 :             # horizontal ghost door
                pygame.draw.line(screen, 'white', (j * num2, i * num1  + (0.5*num1)),(j * num2 + num2 , i * num1 + (0.5*num1)), 3) 

            if level[i][j] == 5 :             # top right corner
                pygame.draw.arc(screen, colour, [(j*num2 - (num2*0.4)-2), (i*num1 + (0.5*num1)), num2, num1], 0, PI/2, 3 )
            if level[i][j] == 6 :             # top left corner
                pygame.draw.arc(screen, colour, [(j*num2 + (num2*0.5)), (i*num1 + (0.5*num1)), num2, num1], PI/2, PI, 3 ) 
            if level[i][j] == 7 :             # bottom left corner
                pygame.draw.arc(screen, colour, [(j*num2 + (num2*0.5)), (i*num1 - (0.4*num1)), num2, num1], PI, 3*PI/2, 3 ) 
            if level[i][j] == 8 :             # bottom right corner
                pygame.draw.arc(screen, colour, [(j*num2 - (num2*0.4)-2), (i*num1 - (0.4*num1)), num2, num1], 3*PI/2, 2*PI, 3 ) 



     
    # nested for loop (need a two-tiered for loop) to go through the entire level

def draw_player(): 
    # 0-right , 1-left , 2-up , 3-down
    if direction == 0 :  #direction variable to check what direc pac is facing
        screen.blit(player_images[counter // 5], (player_x,player_y))   #blit to put img on screen #counter track how fast pac move //5 so it cycles through a byte every 1/3s best for 60fps do all 4 imgs in 20clicks #put pac guy playerx,y for position 
    elif direction == 1 :  
        screen.blit(pygame.transform.flip(player_images[counter // 5],True,False), (player_x,player_y))  # true flip in x direc false in y direc so no flip in y direc
    elif direction == 2 :  
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x,player_y))   #rotate to rotate up or down 90 degree
    elif direction == 3 :  
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x,player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False,] #realised didnt even need to define turns allowed probably, well this will still overight it anyways
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)           # to check if player center position is clear Right, L, U & D
    num3 = 8     #fudge factor since player isnt 30 by 30 #going to be used everywhere  #also so that player goes into wall and not stop and black space in wall tile(before wall)

    if centerx // 30 < 29 :  # Board 30 tiles
        if direction == 0 :
            if level[centery//num1][(centerx - num3)//num2] < 3 :    #what row and column the center is at #going right then checking if tile behind is less than 3 which is black or food
                turns[1] = True
  
        if direction == 1 :
            if level[centery//num1][(centerx + num3)//num2] < 3 :    
                turns[0] = True
 
        if direction == 2 :
            if level[(centery + num3)//num1][centerx // num2] < 3 :    
                turns[3] = True
 
        if direction == 3 :
            if level[(centery - num3) //num1][centerx //num2] < 3 :    
                turns[2] = True                                        #done so that if player hit wall turns back then turns back to wall directly it will not jump wall

        if direction == 2 or direction == 3 :
            if 5 <= centerx % num2 <= 16:    #if x position center of payer divided by num2(how wide tile is) if remainder bet 12-18 then player roughly at mid-point of a tile
                if level[(centery + num3) // num1][centerx // num2] < 3 : #if position directly below is open...
                    turns[3] = True                                       #then can turn down
                if level[(centery - num3) // num1][centerx // num2] < 3 : #same for up
                    turns[2] = True

            if 5 <= centery % num1 <= 16:    
                if level[centery // num1][(centerx - num2) // num2] < 3 : #checking  behind by a full square since this is whie goin up or down9first if 2 directions above) 
                    turns[1] = True                                       #if ttile behind is clear then to left true       
                if level[centery // num1][(centerx + num2) // num2] < 3 : 
                    turns[0] = True                                      # if tile in front clear then to right true


        if direction == 0 or direction == 1 :       #same as above but for right and left thus slight change
            if 5 <= centerx % num2 <= 16:   
                if level[(centery + num1) // num1][centerx // num2] < 3 : 
                    turns[3] = True                                       
                if level[(centery - num1) // num1][centerx // num2] < 3 : 
                    turns[2] = True

            if 5 <= centery % num1 <= 16:    
                if level[centery // num1][(centerx - num3) // num2] < 3 :  
                    turns[1] = True                                             
                if level[centery // num1][(centerx + num3) // num2] < 3 : 
                    turns[0] = True  



    else:
        turns[0] = True
        turns[1] = True    # outside of board can L & R

     
    return turns

def move_player(play_x, play_y):  
    # right, left, up, down
    if direction == 0 and turns_allowed[0]:  #direc 0 (pointing right and allow to go right)
        play_x += player_speed               #speed of pacman
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y          #only thing we change player x n y

def get_targets(blink_x, blink_y, pink_x, pink_y, ink_x, ink_y, clyd_x, clyd_y) :
    if player_x < 350 :          #check where player posi is so can run away if powerup active  
        runaway_x = 700
    else :
        runaway_x = 0

    if player_y < 350 :            
        runaway_y = 700
    else :
        runaway_y = 0
    
    return_target = (330, 310)

    if powerup :
        if not blinky.dead and not eaten_ghost [0]:                                    #if powerup and ghost not dead and eaten
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0] :                   #powerup on not dead and eaten already , make it back to box
            if 250 < blink_x < 410  and 255 < blink_y < 350 :
                blink_target = (330, 245)                      #target to get out box
            else:
                blink_target = (player_x, player_y)           #not in box target player
        
        else:
            blink_target = return_target                      #else get back to box to revive

        if not pinky.dead and not eaten_ghost[1]:                                    
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[1] :                   #powerup on not dead and eaten already , make it back to box
            if 250 < pink_x < 410  and 255 < pink_y < 350 :
                pink_target = (330, 245)                      #target to get out box
            else:
                pink_target = (player_x, player_y)           #not in box target player
        else:
            pink_target = return_target 

        if not inky.dead and not eaten_ghost[2]:                                    
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[2] :                   #powerup on not dead and eaten already , make it back to box
            if 250 < ink_x < 410  and 255 < ink_y < 350 :
                ink_target = (330, 245)                      #target to get out box
            else:
                ink_target = (player_x, player_y)           #not in box target player
        else:
            ink_target = return_target

        if not clyde.dead and not eaten_ghost[3]:                                    
            clyd_target = (350, 350)        #go through middle when die
        elif not clyde.dead and eaten_ghost[3] :                   #powerup on not dead and eaten already , make it back to box
            if 250 < clyd_x < 410  and 255 < clyd_y < 350 :
                clyd_target = (330, 245)                      #target to get out box
            else:
                clyd_target = (player_x, player_y)           #not in box target player
        else:
            clyd_target = return_target 

    else :                                  
        if not blinky.dead:  
            if 250 < blink_x < 410  and 255 < blink_y < 350 :  #in box
                blink_target = (330, 245)                      #target to get out box
            else:
                blink_target = (player_x, player_y)           #not in box target player
        else:
            blink_target = return_target                     #dead then target return box             

        if not pinky.dead:                                    
            if 250 < pink_x < 410  and 255 < pink_y < 350 :  #in box
                pink_target = (330, 245)                      #target to get out box
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target 

        if not inky.dead:                                    
            if 250 < ink_x < 410  and 255 < ink_y < 350 :  #in box
                ink_target = (330, 245)                      #target to get out box
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target

        if not clyde.dead:  
            if 250 < clyd_x < 410  and 255 < clyd_y < 350 :  #in box
                clyd_target = (330, 245)                      #target to get out box
            else:
                clyd_target = (player_x, player_y)                                                   
        else:
            clyd_target = return_target

    return [blink_target, pink_target, ink_target, clyd_target]


pygame.mixer.init()                     
power_sound = pygame.mixer.Sound('pacman_powerup.wav')
power_sound.set_volume(0.5)
eatghost_sound = pygame.mixer.Sound('pacman_eatghost.wav')
eatghost_sound.set_volume(2)
playerdead_sound = pygame.mixer.Sound('pacman_death.wav')
playerdead_sound.set_volume(2)

# game loop to get game window up
run = True
# while game is running these should keep happening/updating
while run: 
    timer.tick(fps)
    if counter < 19 :  #60fps so img 5 times # also used for power up when pac flicks while being big
        counter += 1
        if counter > 3 :
            flicker = False # for power up when pac flicks while being big
    else: 
        counter = 0
        flicker = True #counter refresh 3 times a second and will flicker for only 3s

    if powerup and power_counter < 625 :   # 600 = 10s for a 60fps
        if not power_soundplay:
            power_sound.play(-1)  # Loop forever
            power_soundplay = True
        power_counter += 1
    elif powerup and power_counter >= 625 : 
        power_sound.stop()
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    if startup_counter <= 0 and lives==3:                                  #intro music liv3 cuz only at start
        pygame.mixer.init()
        pygame.mixer.music.load('pacman_beginning.wav')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    if startup_counter < 240 and not game_over and not game_won :     #count down before game starts 180=3s
        moving = False                 #wont be moving so if gameover or game won is true startup counter wont update
        startup_counter += 1
    elif startup_counter >= 240 and game_won :    #stop all movement when win
        moving = False
    elif startup_counter ==0 and game_over:    #stop all movement when gameover broo took so long to find i miss this thats y not stopping after gameover...still no work,ouff just had to startupcounter 0 cuz i remembered gamover reset it
        moving = False
    else:
        moving = True
    

    screen.fill('black') #background
    draw_board()    #drawboard function
    
    center_x = player_x + 15
    center_y = player_y + 16

    if powerup:                      #ghosts speed when powerup on and off and dead eyes
        ghost_speeds = [3,1,1,1]
    else:
        ghost_speeds = [3,2,2,2]
    
    if eaten_ghost[0] :                   #if they just died and revived
        ghost_speeds[0] = 3 
    if eaten_ghost[1] :
        ghost_speeds[1] = 2
    if eaten_ghost[2] :
        ghost_speeds[2] = 2
    if eaten_ghost[3] :
        ghost_speeds[3] = 2

    if blinky_dead :                   #if they dead eyes form going back
        ghost_speeds[0] = 4 
    if pinky_dead :
        ghost_speeds[1] = 4
    if inky_dead :
        ghost_speeds[2] = 4
    if clyde_dead :
        ghost_speeds[3] = 4

    game_won = True                #game is won until it finds pellets( 1 and 2) then = false
    for i in range (len(level)) : 
        if 1 in level[i] or 2 in level[i] :     #i in range leght of level, if there is 1 or 2 in the row 
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 13, 2) #cirlce represent player's hitbox radius 14

    draw_player()  #drawplayer function #center above player circle so center defined first to use in it, then draw player below so circle is drawn behind player

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)   #id is 0                              #creating the ghosts so they appear on board Ghost for class
    pinky = Ghost(pinky_x, pinky_y, targets[1], ghost_speeds[1], pinky_img, pinky_direction, pinky_dead, pinky_box, 1)
    inky = Ghost(inky_x, inky_y, targets[2], ghost_speeds[2], inky_img, inky_direction, inky_dead, inky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)

    draw_scoreboard() #score etc displayed on screen
    targets = get_targets(blinky_x, blinky_y, pinky_x, pinky_y, inky_x, inky_y, clyde_x, clyde_y)

   # pygame.draw.circle(screen, 'white', (center_x,center_y), 2) #--->  #to check center of player if the value + is centering
    turns_allowed = check_position(center_x, center_y) #position checker func check where player is and if action allowed
    if moving :                                              #player movement change only when moving is true aka after 3s
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()     

        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        
        if not clyde_dead and not clyde.in_box:
            clyde_x, clyde_y, clyde_direction = clyde.move_blinky()      #wanted to make clyde op but then realised blinky better be op cuz i start him out box and my fav colour is red so i swap their movement function 
        else:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost) #to check collision against object like food and use for power up too , check_position is for walls


    #collision bet player and ghost    # add to if not powerup to check if eaten ghosts
    if not powerup :
        power_sound.stop() #to cancel powerup sound when player dies while powerup was on
        if (player_circle.colliderect(blinky.rect) and not (blinky.dead)) \
            or (player_circle.colliderect(pinky.rect) and not (pinky.dead)) \
            or (player_circle.colliderect(inky.rect) and not (inky.dead)) \
            or (player_circle.colliderect(clyde.rect) and not (clyde.dead)) :     #player circle hit ghost rectangle
          
            playerdead_sound.play() #dying sound
           
            if lives > 0 :                               
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                powerup = False               #when die powerup ends , eg die while eating powerup
                power_counter = 0 

                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False
                
            else:           #out of lives
                player_x = 330   #return player to starting position so can be separated from  ghost and dead sound stop looping when game is over
                player_y = 412   #i put player inside wall so no chance of contact with ghost
                direction = 0
                direction_command = 0    

                game_over = True
                moving = False
                startup_counter = 0

    #all times could loose a life and pot gameover
    if powerup and player_circle.colliderect(blinky.rect) and  eaten_ghost[0] and not blinky.dead  :
        playerdead_sound.play()
        if lives > 0 :
                powerup = False               
                power_counter = 0                               
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                
                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False

                
        else:                                     #out of lives
            game_over = True
            playerdead_sound.stop()
            moving = False
            startup_counter = 0
            
    if powerup and player_circle.colliderect(pinky.rect) and  eaten_ghost[1] and not pinky.dead  :
        playerdead_sound.play()
        if lives > 0 :  
                powerup = False               
                power_counter = 0                             
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                
                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False
        else:                                     #out of lives
            game_over = True
            playerdead_sound.stop()
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and  eaten_ghost[2] and not inky.dead  :
        playerdead_sound.play()
        if lives > 0 :
                powerup = False               
                power_counter = 0                               
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                
                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False
        else:                                     #out of lives
            game_over = True
            playerdead_sound.stop()
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and  eaten_ghost[3] and not clyde.dead :    #dead cuz collide with eyes no problem
        playerdead_sound.play()
        if lives > 0 : 
                powerup = False               
                power_counter = 0                              
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                
                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False
        else:                                     #out of lives
            game_over = True
            playerdead_sound.stop()
            moving = False
            startup_counter = 0
   
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead : #can only eat blinky 1 time per powerup else add "and not eaten_ghost[0]" in condition 
        eatghost_sound.play()     #sound when eat ghost
        blinky_dead = True         #power up active , they collide so he dies
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 200                     #score = (2^ghost eaten ) * 200 ... 1= 2^1 *200 = 400 -- here x200 cuz blinky op 

    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[1] :
        eatghost_sound.play()     #sound when eat ghost  
        pinky_dead = True         
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100            # (2^ghost eaten ) * 100 ... 1= 2^1 *100 = 200

    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[2] : 
        eatghost_sound.play()     #sound when eat ghost
         
        inky_dead = True         
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100 

    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3] : 
        eatghost_sound.play()     #sound when eat ghost 
        clyde_dead = True         
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100 


# conditions to end loop
    for event in pygame.event.get():  #pygame.event.get is everything that pygame can process(from keyboard etc..)
        if event.type == pygame.QUIT:   # what event type was #pygame.QUIT red cross close tab 
            run = False
        
        if event.type == pygame.KEYDOWN:  #checking anytime a button is pressed on keyboard 
            if event.key == pygame.K_RIGHT :    #right arrow key
                direction_command = 0
            if event.key == pygame.K_LEFT :     #left arrow key
                direction_command = 1 
            if event.key == pygame.K_UP :       # up key
                direction_command = 2
            if event.key == pygame.K_DOWN :     # down key
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won) :
                powerup = False               
                power_counter = 0                               
                lives -= 1
                startup_counter = 0           #lives -1 counter reset then all position of ghosts and player resets
                
                player_x = 325   
                player_y = 375 
                direction = 0
                direction_command = 0       #

                blinky_x = 330           
                blinky_y = 245
                blinky_direction = 0

                pinky_x = 290
                pinky_y = 308
                pinky_direction = 2

                inky_x = 370
                inky_y = 308
                inky_direction = 2

                clyde_x = 330
                clyde_y = 308
                clyde_direction = 2

                #reset are ghosts dead command and reset eaten ghosts , no need reset are they in box cuz fuction check directly
                eaten_ghost = [False, False, False, False]

                blinky_dead = False     # variable to track their death
                pinky_dead = False
                inky_dead= False 
                clyde_dead = False

                if score > high_score and game_won :      #set up highscore when win
                    high_score = score
                score = 0 
                lives = 3
                level = copy.deepcopy(boards)    #reset board by copying source board again
                game_over = False
                game_won = False
            
                
        if event.type == pygame.KEYUP:         # if keyup then direction_command will
            if event.key == pygame.K_RIGHT and direction_command == 0 :     #basically press right for eg then press left at same time then release it cuz actually wanna go right , this ensures it ignores left and go right
                direction_command = 0
            if event.key == pygame.K_LEFT and direction_command == 1 :     
                direction_command = 1 
            if event.key == pygame.K_UP and direction_command == 2 :      
                direction_command = 2
            if event.key == pygame.K_DOWN and direction_command == 3 :     
                direction_command = 3

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:        #player movement feel like joystick
        direction = 3

    if player_x > 666:
        player_x = -28
    elif player_x < -29:
        player_x = 666 

    #return to box and turn back to life
    if blinky.in_box and blinky_dead:   
        blinky_dead = False 
    if pinky.in_box and pinky_dead:
        pinky_dead = False 
    if inky.in_box and inky_dead:
        inky_dead = False 
    if clyde.in_box and clyde_dead:
        clyde_dead = False 

    pygame.display.flip() #to draw more on the screen than just background (in loop)
pygame.quit()

#drawing board onto the screen