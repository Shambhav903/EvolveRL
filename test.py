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
    #code here
    index = axial_x + (axial_y+int(axial_x/2))*79
    return index

def main():
    print(list_to_axial(79*38 -1 -79))
    print(axial_to_list(0,-1))
    
if __name__ == "__main__":
    main()
