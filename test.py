# def list_to_axial(index):
#     x = 0
#     y = 0
#     #code here
#     quotient = int(index/79)
#     index = index % 79
#     x = index
#     y = -1 * int(index/2) + quotient
#     return x,y

# def axial_to_list(axial_x,axial_y):
#     #code here
#     index = axial_x + (axial_y+int(axial_x/2))*79
#     return index

# def main():
#     print(list_to_axial(79*38 -1 -79))
#     print(axial_to_list(0,-1))
    
# if __name__ == "__main__":
#     main()

def axial_to_cube(axial_x, axial_y):
    cube_s = 0
    cube_q = axial_x
    cube_r = axial_y
    cube_s = - cube_q - cube_r
    return (cube_q, cube_r, cube_s)

def check_prey(x,y):
    return 0



def predator_vision(axial_x, axial_y, dir_vec):
    initial_posx, initial_posy = axial_x , axial_y
    a,b,c,d = 0,0,0,0
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
            check_x, check_y = (initial_posx + j*a), (initial_posy +j*b)
            check_prey (check_x, check_y) #rightshift
            print (check_x,check_y)
        initial_posx, initial_posy= initial_posx + c*i, initial_posy+ d*i  #leftshift
    return 0


predator_vision(1,0,0)
