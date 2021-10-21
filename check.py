import pygame
import pygame as p
import random
from pygame.locals import *
from pygame_gui.ui_manager import UIManager
import pygame_gui
clock = p.time.Clock()
pygame.init()
pygame.font.init()
fps = 10
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
root = p.display.set_mode((1500 , 800))
manager = pygame_gui.UIManager((1500 , 800))
text = pygame_gui.elements.UITextEntryLine(relative_rect=p.Rect(700, 0, 100, 20), manager=manager)
height = root.get_height()//20
width = root.get_width()//20
cells = [[random.choice([0 , 1]) for j in range(width)] for i in range(height)]
#gens = [[[random.choice([0 , 0]) for j in range 9] for x in range(width)] for i in range(height)]
#for i in range (width):
#for j in range (height):
#if cells[i][j] == 1:
#gens[i][j] =  [random.choice([0 , 1]) for j in range 9]


def near(pos: list , system=[[-1 , -1] , [-1 , 0] , [-1 , 1] , [0 , -1] , [0 , 1] , [1 , -1] , [1 , 0] , [1 , 1]]):
    count = 0
    for i in system:
        if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])]:
            count += 1
    return count

work = True
while work:
    manager.draw_ui(root)
    for event in p.event.get():
        if event.type == p.QUIT:
            work = False
        elif event.type == p.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
               if event.ui_element == text:
                   width = int(text)
                   height = int(text)
                   cells = [[random.choice([0, 1]) for j in range(width)] for i in
                            range(height)]
    #if width != 0:
    #run = false
    #game = on
    #start = start
    #while  run == false:
    #if game == on:
    #run = true
    #while run == true:

    for i in range(0 , height):
        p.draw.line(root , BLACK , (0 , i * 20) , (width, i * 20))
    for j in range(0 , width// 20):
        p.draw.line(root , BLACK , (j * 20 , 0) , (j * 20 , height))
    for i in p.event.get():
        if i.type == QUIT:
            quit()


    for i in range(0 , len(cells)):
        for j in range(0 , len(cells[i])):
            print(cells[i][j],i,j)
            p.draw.rect(root , (0, 255 * cells[i][j] % 256  , 0) , [i * 20 , j * 20 , 20 , 20])
    p.display.update()
    cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if cells[i][j]:
                if near([i , j]) not in (2 , 3):
                    cells2[i][j] = 0
                    continue
                cells2[i][j] = 1
                continue
            if near([i , j]) == 3:
                cells2[i][j] = 1
                continue
            cells2[i][j] = 0
    cells = cells2
    clock.tick(fps)