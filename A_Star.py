import math
from tkinter import *
import time
import random

dt = time.time()

screen_width = 500
screen_height = 500

root = Tk()
canvas = Canvas(root,width=screen_width,height=screen_height)
canvas.pack()

mouse_pressed = False
mouse_x = 0
mouse_y = 0

#Class that contains information about a particular spot on the map
class Node:
    def __init__(self,x,y):
        #1: Empty Space
        #2: Start Location
        #3: End Location
        #4: Wall
        self.type = 1
        self.x = x
        self.y = y

        self.prev_node = None

        self.path_length = 0
        self.end_dist = 0

    def get_score(self):
        return self.end_dist + self.path_length

    def duplicate(self):
        new = Node(self.x,self.y)
        new.type = self.type

        return new

class Button:
    def __init__(self,x,y,width,height,function,text='',fill='white',outline='black',text_size=10,shape='square'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fill = fill
        self.outline = outline

        self.text = text
        self.text_size = text_size

        self.function = function

        self.shape = shape

    def update(self):
        global mouse_pressed
        if mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height and mouse_pressed:
            mouse_pressed = False
            self.function()

        self.render()

    def render(self):
        if self.shape == 'square':
            canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill=self.fill,outline=self.outline)
        elif self.shape == 'circle':
            canvas.create_oval(self.x,self.y,self.x+self.width,self.y+self.height,fill=self.fill,outline=self.outline)
        else:
            print('invalid shape')

        canvas.create_text(self.x+self.width/2,self.y+self.height/2,anchor=CENTER,text=self.text,font=('TkTextFont',self.text_size))


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
            if l[i].get_score() < sorted[j].get_score():
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

def evaluate_new_node(x,y,n):
    global nodes
    #check that position is on the map
    k = None
    in_list = False
    for i in nodes:
        if x == i.x and y == i.y:
            in_list = True
            k = i
            break

    if not in_list:
        for i in final_nodes:
            if x == i.x and y == i.y:
                in_list = True
                break
    if x >= 0 and y >= 0 and x < width and y < height:
        #create a node containing the same values as node in that spot
        nn = map[x][y].duplicate()
        #check if node is not a wall
        if not nn.type == 4:
            #check if not backtracking
            if not nn.x == n.prev_node.x or not nn.y == n.prev_node.y:
                #set values of node
                nn.path_length = n.path_length + 1
                nn.end_dist = get_dist(x,y,end_node[0],end_node[1])
                nn.prev_node = n

                #add node to the list of nodes
                c = False
                if not in_list:
                    c = True
                if k:
                    if nn.get_score() < k.get_score():
                        nodes.remove(k)
                        c = True
                if c:
                    nodes.append(nn)


def mouse_press(event):
    global mouse_pressed
    mouse_pressed = True

def mouse_release(event):
    global mouse_pressed
    mouse_pressed = False

def motion(event):
    global mouse_x,mouse_y
    mouse_x = event.x
    mouse_y = event.y

def key_press(event):
    global placing_nodes
    if start_node and end_node and event.keysym == 'Return':
        placing_nodes = False

def increase_width():
    global width
    width += 1

def decrease_width():
    global width
    width -= 1

def increase_height():
    global height
    height += 1

def decrease_height():
    global height
    height -= 1

def stop_choosing_size():
    global choosing_size
    choosing_size = False



root.bind('<Button-1>',mouse_press)
root.bind('<ButtonRelease-1>',mouse_release)
root.bind('<Motion>',motion)
root.bind('<KeyPress>',key_press)

#Create empty list that will contain every node
map = []

#Initialize values for the width & height of the map
width = 20
height = 20

choosing_size = True

increase_x = Button(285,110,30,30,increase_width,text='+',outline='',fill='',text_size=20)
decrease_x = Button(185,110,30,30,decrease_width,text='-',outline='',fill='',text_size=20)
increase_y = Button(285,285,30,30,increase_height,text='+',outline='',fill='',text_size=20)
decrease_y = Button(185,285,30,30,decrease_height,text='-',outline='',fill='',text_size=20)

start = Button(150,375,200,100,stop_choosing_size,text='Start!',outline='green',fill='green',text_size=50)

while choosing_size:
    canvas.delete(ALL)

    canvas.create_text(250,50,anchor=CENTER,text='width',font=('TkTextFont',30))
    canvas.create_text(250,125,anchor=CENTER,text=width,font=('TkTextFont',30))

    canvas.create_text(250,225,anchor=CENTER,text='height',font=('TkTextFont',30))
    canvas.create_text(250,300,anchor=CENTER,text=height,font=('TkTextFont',30))

    increase_x.update()
    decrease_x.update()
    increase_y.update()
    decrease_y.update()

    start.update()

    root.update()


pixel_x = screen_width/width
pixel_y = screen_height/height

#Add node to every spot within the width & height
for x in range(width):
    l = []
    for y in range(height):
        n = Node(x,y)
        l.append(n)
    map.append(l)

placing_nodes = True

start_node = None
end_node = None

while placing_nodes:
    canvas.delete(ALL)
    for x in range(width):
        for y in range(height):
            x1 = x*pixel_x
            y1 = y*pixel_y

            canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y)

            if start_node:
                if x == start_node[0] and y == start_node[1]:
                    canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='blue')
            if end_node:
                if x == end_node[0] and y == end_node[1]:
                    canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='orange')

            if map[x][y].type == 4:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='gray')


    root.update()

    if mouse_pressed:
        x = int(mouse_x/pixel_x)
        y = int(mouse_y/pixel_y)
        print(x,y)
        if not start_node:
            mouse_pressed = False
            start_node = (x,y)
            map[start_node[0]][start_node[1]].type = 2

        elif not end_node:
            mouse_pressed = False
            end_node = (x,y)
            map[end_node[0]][end_node[1]].type = 3

        else:
            map[x][y].type = 4


nodes = [map[start_node[0]][start_node[1]]]
nodes[0].prev_node = nodes[0]

final_nodes = []

dt = time.time()
while not nodes[0].x == end_node[0] or not nodes[0].y == end_node[1]:
    n = nodes[0]
    if True:
        mouse_pressed = False
        nodes.remove(n)
        in_list = False
        for i in final_nodes:
            if i.x == n.x and i.y == n.y:
                in_list = True
        if not in_list:
            final_nodes.append(n)

            #position of node next to the current node
            x = n.x + 1
            y = n.y
            evaluate_new_node(x,y,n)

            x = n.x - 1
            y = n.y
            evaluate_new_node(x,y,n)

            x = n.x
            y = n.y + 1
            evaluate_new_node(x,y,n)

            x = n.x
            y = n.y - 1
            evaluate_new_node(x,y,n)

        nodes = sort(nodes)

    canvas.delete(ALL)
    for x in range(width):
        for y in range(height):
            x1 = x*pixel_x
            y1 = y*pixel_y

            in_list = False
            for i in final_nodes:
                if i.x == x and i.y == y:
                    canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='red')
                    in_list = True
            for i in nodes:
                if i.x == x and i.y == y:
                    canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='green')
                    in_list = True
            if x == n.x and y == n.y:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='purple')
            if x == start_node[0] and y == start_node[1]:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='blue')
            elif x == end_node[0] and y == end_node[1]:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='orange')
            elif map[x][y].type == 4:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='gray')
            elif not in_list:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y)


    root.update()



path = [nodes[0]]
prev_node = nodes[0].prev_node
while not prev_node.x == start_node[0] or not prev_node.y == start_node[1]:
    path.append(prev_node)
    prev_node = prev_node.prev_node



path.reverse()
for i in path:
    print(i.x,i.y)

print('Finished in ' + str(int(time.time()-dt)) + ' seconds')

canvas.delete(ALL)
for x in range(width):
    for y in range(height):
        x1 = x*pixel_x
        y1 = y*pixel_y
        in_list = False
        for i in path:
            if x == i.x and y == i.y:
                canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='cyan')
                in_list = True
        if x == start_node[0] and y == start_node[1]:
            canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='blue')
        elif x == end_node[0] and y == end_node[1]:
            canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='orange')
        elif map[x][y].type == 4:
            canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y,fill='gray')
        elif not in_list:
            canvas.create_rectangle(x1,y1,x1+pixel_x,y1+pixel_y)

root.mainloop()
