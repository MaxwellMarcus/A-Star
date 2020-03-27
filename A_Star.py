import math

#Class that contains information about a particular spot on the map
class Node:
    def __init__(self):
        #1: Empty Space
        #2: Start Location
        #3: End Location
        #4: Wall
        self.type = 1

def sort(l):
    '''
    l - list containing unsorted numbers

    returns sorted list
    '''
    sorted = []

    for i in range(len(l)):
        added = False
        for j in range(len(sorted)):
            #Add the value in front of the first element of the sorted list that the value is less than
            if l[i] < sorted[j]:
                sorted.insert(j,l[i])
                added = True
                break

        #If the value hasn't been added yet, add it at the end
        if not added:
            sorted.append(l[i])

    #Return the sorted list
    return sorted

def get_dist(x1,y1,x2,y2):
    '''
    x1 - x value of first coordinate
    y1 - y value of first coordinate
    x2 - x value of second coordinate
    y2 - y value of second coordinate

    returns euclidean distance between two coordinates
    '''
    
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def get_values(location):
    global map,width,height
    values = []
    node = map[location[0]+1][location[1]]
    if location[0]+1 < width and node.type == 1 or node.type == 3:
        score =
        values.append({'x':location[0]+1,'y':location[1],'score':})

#Create empty list that will contain every node
map = []

#Initialize values for the width & height of the map
width = 4
height = 4

#Add node to every spot within the width & height
for x in range(width):
    l = []
    for y in range(height):
        l.append(Node())

    map.append(l)

#Set the start location for the algorithm
map[0][0].type = 2

#Set the end location for the algorithm
map[3][3].type = 3

location = [0,0]
