import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800 # size of window width in pixels
WINDOWHEIGHT = 600 # size of window height in pixels
# width and height of single sector
SECTORWIDTH=20 
SECTORHEIGHT=30
UNITWIDTH = SECTORWIDTH/6

# joshua body propotions
HEADCENTERX = SECTORWIDTH/2
HEADCENTERY = SECTORHEIGHT/8
SHOULDERHEIGHT = SECTORHEIGHT/9
HANDHEIGHT=SECTORHEIGHT/4
HANDWIDTH=SECTORWIDTH/6
BODYHANDWIDTH= SECTORWIDTH/30
LEGWIDTH=SECTORWIDTH/5
BLEGWIDTH=SECTORWIDTH/5
LEGHEIGHT=SECTORHEIGHT*3/8


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# directions constants
LEFT = 'left'
RIGHT='right'
UP='up'
DOWN = 'down'

# display settings initiation
global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode ((WINDOWWIDTH, WINDOWHEIGHT))
    
# ground and walls sprites
groundImg = pygame.image.load('grasstitle.png')
wallImg = pygame.image.load('walltitle.png')

#player sprites
playerImg= pygame.image.load('char.png').convert_alpha()

def main():


    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.set_colorkey(WHITE)
    # character start point
    jx=0
    jy=0
    mazeReal=generateMaze(0, 0)    
           
    while True:

        DISPLAYSURF.fill(WHITE)
        
        drawMaze(DISPLAYSURF, mazeReal)
        joshua (DISPLAYSURF, jx, jy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                #get movement
                if event.key in (K_LEFT, K_a) and possibMove(jx, jy, mazeReal, LEFT):
                    jx -=SECTORWIDTH
                elif event.key in (K_RIGHT, K_d) and possibMove(jx, jy, mazeReal, RIGHT):
                    jx +=SECTORWIDTH
                elif event.key in (K_UP, K_w) and possibMove(jx, jy, mazeReal, UP):
                    jy -=SECTORHEIGHT
                elif event.key in (K_DOWN, K_s) and possibMove(jx, jy, mazeReal, DOWN):
                    jy +=SECTORHEIGHT

        if winSituation (jx, jy, mazeReal):
            DISPLAYSURF.fill(WHITE)
            # character start point
            jx=0
            jy=0
            mazeReal=generateMaze(0, 0)                
                    
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# joshua - scalable character
def joshua(surf, jx, jy):
    
    surf.blit(playerImg, (jx, jy, SECTORWIDTH, SECTORHEIGHT))
        
   # pygame.draw.polygon (surf, color, ((jx, jy+2*HEADCENTERY+SHOULDERHEIGHT), (jx+SHOULDERHEIGHT, jy+2*HEADCENTERY), (jx+SECTORWIDTH-SHOULDERHEIGHT, jy+2*HEADCENTERY),
   #                                    (jx+SECTORWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT), (jx+SECTORWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT+HANDHEIGHT),
   #                                    (jx+SECTORWIDTH-HANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT+HANDHEIGHT), (jx+SECTORWIDTH-HANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT),
   #                                    (jx+SECTORWIDTH-HANDWIDTH - BODYHANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT), (jx+SECTORWIDTH-HANDWIDTH - BODYHANDWIDTH, jy+SECTORHEIGHT),
   #                                    (jx+SECTORWIDTH-HANDWIDTH - BODYHANDWIDTH-LEGWIDTH, jy+SECTORHEIGHT), (jx+SECTORWIDTH-HANDWIDTH - BODYHANDWIDTH-LEGWIDTH, jy+SECTORHEIGHT-LEGHEIGHT),
   #                                    (jx+HANDWIDTH + BODYHANDWIDTH+LEGWIDTH, jy+SECTORHEIGHT-LEGHEIGHT), (jx+HANDWIDTH + BODYHANDWIDTH+LEGWIDTH, jy+SECTORHEIGHT),
   #                                    (jx+HANDWIDTH + BODYHANDWIDTH, jy+SECTORHEIGHT), (jx+HANDWIDTH + BODYHANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT),
   #                                    (jx+HANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT), (jx+HANDWIDTH, jy+2*HEADCENTERY+SHOULDERHEIGHT+HANDHEIGHT), (jx, jy+2*HEADCENTERY+SHOULDERHEIGHT+HANDHEIGHT)))
   #
   # pygame.draw.circle (surf, color, (jx+HEADCENTERX, jy+HEADCENTERY), HEADCENTERY)

def generateMaze(sx, sy):
    maze={}
    visits={}
    currentStack=[]
    currentCell=(sx, sy)
    maxStackLen=0
    finish=()
    nextCell=()
    mazeWalls=[]

    # setting unvisited, full of walls maze

    for k in range (WINDOWWIDTH/SECTORWIDTH):
        for v in range (WINDOWHEIGHT/SECTORHEIGHT):
            maze[k, v]='1'
            visits[k, v]='0'

    #maze generation loop
    while unVisited(visits):
        neighbours=getUnvisitedNeighbours(currentCell, visits) #get set of neighbors
        maze[currentCell]='0' #set current cell as empty in maze
        visits[currentCell]='1' # set current sell as visited
        
        if neighbours!=[]: #while there are univisited neighbours
            nextCell= randomCell(neighbours)
            maze[((currentCell[0]+nextCell[0])/2), ((currentCell[1]+nextCell[1])/2)] = '0' # make a hole in the wall
            currentStack.append(currentCell) # append current cell to satck
            currentCell=nextCell # choose random univisited neighbour
            if len(currentStack)>maxStackLen:
                maxStackLen=len(currentStack)
                finish=currentCell
            
        elif currentStack !=[]: # if stack not empty
            currentCell=currentStack.pop()
           

        else: #if no univisited neighbours and stack is empty
                currentCell=randomCell(unVisited(visits))

    # find a set of walls
    for cell in maze.keys():
        if maze[cell]=='1': mazeWalls.append(cell) 
    # small additiional crash of walls
    for k in range(20):
        maze[mazeWalls[random.randint(0, len(mazeWalls)-1)]]='0'

    maze[sx, sy] = '3' # jx, jy - start
    maze[finish] = '4' # set the finish
    return maze     

def possibMove(x, y, maze, direction):

    if direction=='left':
        return ((x>0) and (maze[((x/SECTORWIDTH)-1, y/SECTORHEIGHT)]!='1'))
    elif direction =='right':
        return ((x<WINDOWWIDTH-SECTORWIDTH) and(maze[((x/SECTORWIDTH)+1, y/SECTORHEIGHT)]!='1'))
    elif direction =='up':
        return ((y>0) and (maze[(x/SECTORWIDTH, y/SECTORHEIGHT-1)]!='1'))
    elif direction =='down':
        return ((y<WINDOWHEIGHT-SECTORHEIGHT) and (maze[(x/SECTORWIDTH, y/SECTORHEIGHT+1)]!='1'))

def winSituation (x, y, maze):

    return (maze[(x/SECTORWIDTH, y/SECTORHEIGHT)]=='4')    
                
                

def getUnvisitedNeighbours (cell, visits):

    neighbours=[]
    if (cell[1]-2)>=0: # check for boundaries of display surface
        if visits[(cell[0], cell[1]-2)]=='0':
            neighbours.append((cell[0], cell[1]-2))

    if (cell[0]+2)<= (WINDOWWIDTH/SECTORWIDTH-1): # check for boundaries of display surface
        if visits[(cell[0]+2, cell[1])] =='0':
            neighbours.append((cell[0]+2, cell[1]))

    if (cell[1]+2)<= (WINDOWHEIGHT/SECTORHEIGHT-1): # check for boundaries of display surface
        if visits[(cell[0], cell[1]+2)] =='0':
            neighbours.append((cell[0], cell[1]+2))

    if (cell[0]-2)>=0: # check for boundaries of display surface
        if visits[(cell[0]-2, cell[1])] =='0':
            neighbours.append((cell[0]-2, cell[1]))

    return neighbours

def unVisited(visits):

    unvCellSet=[]
    for key in visits.keys():
        if (visits[key]== '0') and (key[0] % 2 == 0) and (key[1]%2==0) :
            unvCellSet.append(key)

    return unvCellSet

def randomCell(cellSet):
    if cellSet==[]:
        return[]
    x=random.randint(0, len(cellSet)-1)
    return cellSet[x]

def drawMaze (surf, maze, colorStart= ORANGE, colorFinish=BLUE):

    for (k, v) in maze.keys():
        if maze[k ,v]=='1':
            surf.blit(wallImg, (k*SECTORWIDTH, v*SECTORHEIGHT, SECTORWIDTH, SECTORHEIGHT))
        
        if maze[k ,v]=='0':
            surf.blit(groundImg, (k*SECTORWIDTH, v*SECTORHEIGHT, SECTORWIDTH, SECTORHEIGHT))
        if maze[k,v] == '3':
            pygame.draw.rect(surf, colorStart, (k*SECTORWIDTH, v*SECTORHEIGHT, SECTORWIDTH, SECTORHEIGHT))
        if maze[k,v] == '4':
            pygame.draw.rect(surf, colorFinish, (k*SECTORWIDTH, v*SECTORHEIGHT, SECTORWIDTH, SECTORHEIGHT))



if __name__== '__main__':
    main()
