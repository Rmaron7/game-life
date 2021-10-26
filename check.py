import pygame
import pygame as p
import random
from pygame.locals import *
from pygame_gui.ui_manager import UIManager
import pygame_gui

clock = p.time.Clock()
pygame.init()
pygame.font.init()
fps = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
KRASIVOE = (0, 255, 255)
screen = p.display.set_mode((1920, 1080))
manager = pygame_gui.UIManager((1920, 1080))
text = pygame_gui.elements.UITextEntryLine(relative_rect=p.Rect(700, 0, 100, 20), manager=manager)
height = screen.get_height() // 20
width = screen.get_width() // 20
cells = [[random.choice([0, 1]) for j in range(width)] for i in range(height)]
gens = [[[random.choice([0, 0]) for z in range(9)] for j in range(width)] for i in range(height)]
gensn = [[[random.choice([0, 0]) for z in range(9)] for j in range(width)] for i in range(height)]
alive = False
for i in range(height):
    for j in range(width):
        if cells[i][j] == 1:
            gens[i][j] = [random.choice([0, 1, 2, 3]) for counter in range(9)]
            for counter in range(9):
                if gens[i][j][counter] != 1:
                    gens[i][j][counter] = 0
                gens[i][j][2] = 1
                gens[i][j][3] = 1


def near(pos: list, cellaround=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]):
    counternear = 0
    for i in cellaround:
        counternear += cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])]
    return counternear


work = True
while work:
    for event in p.event.get():
        if event.type == p.QUIT:
            work = False

    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
            red = 85 * (gens[i][j][1] + gens[i][j][2] + gens[i][j][0])
            green = 85 * (gens[i][j][7] + gens[i][j][8] + gens[i][j][6])
            blue = 85 * (gens[i][j][4] + gens[i][j][5] + gens[i][j][3])
            cellcolor = (red, green, blue)
            p.draw.rect(screen, (cellcolor), [j * 20, i * 20, 20, 20])

    p.display.update()

    cellsn = cells.copy()
    gensn = gens.copy()

    for i in range(len(cells)):
        for j in range(len(cells[0])):
            print(near([i, j]), cells[i][j]);
            if cells[i][j] == 1:
                for counter in range(9):
                    if gens[i][j][counter] == 1:
                        if near([i, j]) == counter:
                            alive = True
                if alive:
                    cellsn[i][j] = cells[i][j]
                    gensn[i][j] = gens[i][j]
                if not alive:
                    cellsn[i][j] = 0
                    gensn[i][j] = [0] * 9
                alive = False

            if cells[i][j] == 0:
                if near([i, j]) == 3:
                    cellsn[i][j] = 1
                    gensn[i][j] = [random.choice([0, 1, 2, 3]) for counter in range(9)]
                    for counter in range(9):
                        if gensn[i][j][counter] != 1:
                            gensn[i][j][counter] = 0
                        gens[i][j][2] = 1
                        gens[i][j][3] = 1

    cells = cellsn
    gens = gensn
    clock.tick(fps)
































