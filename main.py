from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
import random 
import time




honey_color = tuple([255,195,11])
honey_color_border  =  tuple([181,101,29])
col = tuple([137,207,240])
rosso_corsa = tuple([212,0,0])
light_red = tuple([215,95,86])
green = tuple([0,86,63])


# list of length 79*39 = 3081
# function from list to axial coordinate

def list_to_axial(index):
    x = 0
    y = 0
    #code here
    quotient = int(index/79)
    index = index % 79
    x = index
    y = -1 * int(index/2) + quotient

    return x,y

def axial_to_list(axial_x,axial_y):
    # x = 0
    # y = 0
    #code here
    # quotient = int(index/79)
    index = axial_x + (axial_y+int(axial_x/2))*79

    index = index % (79*38-1)  
    return index

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


# def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
#     """Returns a random RGB colour with each component between min_ and max_"""
#     return tuple(random.choices(list(range(min_, max_)), k=3))


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
    dir = random.randint(1,6)
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
    return x,y

def reset_env ():


    return 0
        
def coordinate_movement(axial_x, axial_y,hexa,color):
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
    x = [i for i in range(10,20)]
    y = [i for i in range(5,15)]

    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        for hexagon in hexagons:
            hexagon.update()

        render(screen, hexagons)

        # agent making function

        # hexagons[axial_to_list(0,-1)].colour = rosso_corsa
        # hexagons[79*39-1].colour = rosso_corsa

        for i in range(0,5):    
            x[i],y[i] = coordinate_movement(x[i],y[i],hexagons,rosso_corsa)
            x[i+5],y[i+5] = coordinate_movement(x[i+5],y[i+5],hexagons,green)
            print('this is running')

        # hexagons[10].colour = rosso_corsa
        # if (a<100):
        #     a+=1
        #     for i in range(10):
        #         prey(hexagons)
        #     for i in range(3):
        #         ranpos(hexagons)

        # print(list_to_axial(4))
        time.sleep(0.2)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()

