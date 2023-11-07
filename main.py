from typing import List
from typing import Tuple
import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
import random 
import time


honey_color = tuple([255,195,11])
honey_color_border = tuple([181,101,29])
col = tuple([137,207,240])
rosso_corsa = tuple([212,0,0])
light_red = tuple([215,95,86])
green = tuple([0,86,63])


SIZEOFGRID = (79,39)
PREDATORCOLOR = tuple([212,0,0])
PREYCOLOR = tuple([0,86,63])


# LIST OF LENGTH 79 * 39 = 3081

"""
list of agents(type)
1. predator agents [list] stores 3-tuple (x,y,z) where x,y represents axial coordinates and 
   z represents direction
2. prey agents [list] stores 2-tuple (x,y) where x,y represent axial coordinates
"""
predatorAgents = []
preyAgents = []


def initializeAgent(noOfPredator,noOfPrey):
    """
    initializes agents and returns them
    """
    predatorAgents = []
    preyAgents = []
    for agent in range(noOfPrey):
        temp = list_to_axial(random.randint(0,3081))
        preyAgents.append((temp[0],temp[1],0))

    for agent in range(noOfPredator):
        temp = list_to_axial(random.randint(0,3081))
        predatorAgents.append((temp[0],temp[1],random.randint(0,7),0))
        
    return preyAgents,predatorAgents

def renderAgents(preyAgents,predatorAgents,hexagon):
    for prey in preyAgents:
        hexagon[axial_to_list((prey[0],prey[1]))].colour = PREYCOLOR
        print('current coordinate',(prey[0],prey[1]))
        print('rendering prey')
    for predator in predatorAgents:
        hexagon[axial_to_list((predator[0],predator[1]))].colour = PREDATORCOLOR
        print('current coordinate',(predator[0],predator[1]))
        print('rendering predator')

def predatorBehaviourCheck(preyAgents,predatorAgents):
    """if predator overlaps then prey is dead
    """
    for predator in predatorAgents:
        for prey in preyAgents:
            if (predator[0],predator[1]) == (prey[0],prey[1]):
                preyAgents.remove(prey)
    pass

def randomMovement(preyAgents,predatorAgents,hexagon):
    """ randomly moves predator and prey agents
    """
    for agentIndex,agent in enumerate(preyAgents):
        x,y = direction_generator(agent[0],agent[1])
        hexagon[axial_to_list((agent[0],agent[1]))].colour = honey_color
        hexagon[axial_to_list((x,y))].colour = PREYCOLOR
        newAgent = (x,y,agent[2])
        preyAgents[agentIndex] = newAgent

        # print('current coordinate',axial_x,axial_y)
        # print('new coordinate',x,y)
    
    for agentIndex,agent in enumerate(predatorAgents):
        x,y = direction_generator(agent[0],agent[1])
        hexagon[axial_to_list((agent[0],agent[1]))].colour = honey_color
        hexagon[axial_to_list((x,y))].colour = PREDATORCOLOR
        newAgent = (x,y,agent[2],agent[3])
        agent = newAgent
        predatorAgents[agentIndex] = newAgent
        # print('current coordinate',axial_x,axial_y)
        # print('new coordinate',x,y)




def list_to_axial(index):
    """from list/index to axial coordinates
    """
    x = 0
    y = 0
    #code here
    quotient = int(index/79)
    index = index % 79
    x = index
    y = -1 * int(index/2) + quotient
    return (x,y)

def axial_to_list(axial):
    """axial to list/index 
    """
    index = axial[0] + (axial[1]+int(axial[0]/2))*79
    index = index % (79*39-1)  
    return index


#for test
def ranpos (hexa = []):
    num  = random.randint(0,79*39-1)
    hexa[num].colour = rosso_corsa
    return 0 
def prey (hexa = []):
    num  = random.randint(0,79*39-1)
    hexa[num].colour = green
    return 0 
def agent(x= 1,y= 1,hexa = []):
    index = x*1 +y*79
    x,y = list_to_axial(index)
    hexa[index].colour = rosso_corsa
    return 0    



def create_hexagon(position, radius=10, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=honey_color)

def init_hexagons(num_x=78, num_y=39, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(10,10), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons

def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill(honey_color)
    for hexagon in hexagons:
        hexagon.render(screen)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in hexagons:
        hexagon.render_highlight(screen, border_colour=honey_color_border)
    for hexagon in colliding_hexagons:
        # for neighbour in hexagon.compute_neighbours(hexagons):
        #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        hexagon.render_highlight(screen, border_colour=(255, 255, 255))
        
    pygame.display.flip()


def direction_generator(currentx,currenty):
    """given current x and y returns nexy x and y in random direction
      """
    dir = random.randint(1,7)
    x = currentx
    y = currenty
    if (dir == 1):
        x = x
        y = y - 1
    elif (dir == 2):
        x=x+1
        y=y-1
    elif (dir == 3):
        x=x+1
        y=y
    elif (dir == 4):
        x=x
        y=y+1
    elif (dir == 5):
        x=x-1
        y=y+1
    elif (dir == 6):
        x=x-1
        y=y
    elif (dir==7):
        x=x
        y=y
    return x,y

def predator_vision(axialCoordinate, dir_vec):
    """ given axial coordinate and direction returns all axial coordinates that predetor can see
    """
    axial_x , axial_y = axialCoordinate
    initial_posx, initial_posy = axial_x , axial_y
    a,b,c,d = 0,0,0,0
    predVis = []
    if (dir_vec == 1):
        a=1
        b=-1
        c=-1
        d=0
    elif (dir_vec == 2):
        a=1
        b=0
        c=0
        d=-1
    elif (dir_vec == 3):
        a=0
        b=1
        c=1
        d=-1
    elif (dir_vec == 4):
        a=-1
        b=1
        c=1
        d=0
    elif (dir_vec == 5):
        a=-1
        b=0
        c=0
        d=1
    elif (dir_vec == 6):
        a=0
        b=-1
        c=-1
        d=1
    for i in range(0,3):
        for j in range(0,3):
            check_x, check_y = (initial_posx + j*c), (initial_posy +j*d) #rightshift 
            predVis.append((check_x,check_y))
        initial_posx, initial_posy= initial_posx + a, initial_posy+ b  #leftshift
        
    return predVis
def prey_vision(axialCoordinate):
    pass


def reset_env ():
    return 0

        
def coordinate_movement(axial_x, axial_y,hexa,color):
    """ given axial coordinates, moves the prosthetic agent """
    x,y = direction_generator(axial_x,axial_y)
    hexa[axial_to_list(axial_x,axial_y)].colour = honey_color
    hexa[axial_to_list(x,y)].colour = color
    print('current coordinate',axial_x,axial_y)
    print('new coordinate',x,y)
    return x,y

def main():
    """Main function"""
    a = 0
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    # x = [i for i in range(10,20)]
    # y = [i for i in range(5,15)]
    preyAgents,predatorAgents = initializeAgent(150,150)

    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        # for hexagon in hexagons:
        #     hexagon.update()

        
        randomMovement(preyAgents,predatorAgents,hexagons)
        predatorBehaviourCheck(preyAgents,predatorAgents)

        renderAgents(preyAgents,predatorAgents,hexagons)

        render(screen, hexagons)
        
        time.sleep(.05)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()

