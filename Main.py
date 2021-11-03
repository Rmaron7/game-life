import pygame
import random
from pygame.locals import *
from pygame_gui.ui_manager import UIManager
import pygame_gui

fps_counter = 0

clock = pygame.time.Clock()
pygame.init()
fps = 120
fps_2 = int(5)
screen = pygame.display.set_mode((1920, 1080))

manager = pygame_gui.UIManager((1920, 1080))

alive = False
started = False

buttonstart = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(800, 600, 320, 60),
    manager=manager,
    text='старт'
    )

textwidth = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(300, 500, 200, 600),
    manager=manager
    )

textheight = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(1420, 500, 200, 600),
    manager=manager
    )

buttonpause = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(1800, 0, 120, 60),
    manager=manager,
    text='пауза'
    )

buttonrestart = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(1800, 150, 120, 60),
    manager=manager,
    text='сброс'
    )


buttonquit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(1800, 60, 120, 60),
    manager=manager,
    text='выйти'
    )

sliderfps = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(1800, 120, 120, 30),
    start_value=12,
    value_range=(0, 25),
    manager=manager
    )

sliderfps.hide()
buttonpause.hide()
buttonrestart.hide()

started = int(0)

field_updated = False


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#функция для генерации рандомных генов

def gensrandom():
    gensr =  [ random.choice([ 0, 1, 2, 3 ]) for z in range(9) ]
    for i in range (9):
        if gensr[i] != 1:
            gensr[i] = 0
            gensr[3] = 0
            gensr[2] = 0
            gensr[4] = 0
    return gensr
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# функция для проверки всех клеток вокруг

def near(pos: list,
         cellaround=[ [ -1, -1 ], [ -1, 0 ], [ -1, 1 ], [ 0, -1 ], [ 0, 1 ], [ 1, -1 ], [ 1, 0 ], [ 1, 1 ] ]):
    counternear = 0
    for i in cellaround:
        counternear += cells[ (pos[ 0 ] + i[ 0 ]) % len(cells) ][ (pos[ 1 ] + i[ 1 ]) % len(cells[ 0 ]) ]
    return counternear

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def gennear(pos: list,
            cellaround=[ [ -1, -1 ], [ -1, 0 ], [ -1, 1 ], [ 0, -1 ], [ 0, 1 ], [ 1, -1 ], [ 1, 0 ], [ 1, 1 ] ]):
    gensparents = [0] * 9
    parents = [[0]*2 for i in range(3)]
    j = int(0)
    for i in cellaround:
        if cells[ (pos[ 0 ] + i[ 0 ]) % len(cells) ][ (pos[ 1 ] + i[ 1 ]) % len(cells[ 0 ]) ] == 1:

            parents[j][0] = (pos[ 0 ] + i[ 0 ]) % len(cells)
            parents[j][1] = (pos[ 1 ] + i[ 1 ]) % len(cells[ 0 ])
            j += 1
    for i in range (9):
        j = random.choice([0, 1, 2])
        gensparents[i] = gens[parents[j][0]][parents[j][1]][i]
        if random.randrange(1000) == 0:
            gensparents[i] = 1
    return gensparents


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


mainrun = True
while mainrun:

    fps_counter += 1

    time_delta = clock.tick(60) / 1000.0
    #while started == 0:

    # обработка событий интерфейса

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainrun = False

        if event.type == pygame.MOUSEBUTTONDOWN and started == -1:
            if event.button == 1:

                if event.pos[0] < width*20 and event.pos[1] < height*20:
                    eventwidth = int(event.pos[0]//20)
                    eventheight = int(event.pos[1]//20)
                    cellsn[eventheight][eventwidth] = 1
                    gensn[eventheight][eventwidth] = gensrandom()
                    field_updated = True

            if event.button == 3:
                if event.pos[0] < width*20 and event.pos[1] < height*20:
                    eventwidth = int(event.pos[0]//20)
                    eventheight = int(event.pos[1]//20)
                    cellsn[eventheight][eventwidth] = 0
                    gensn[eventheight][eventwidth] = [0]*9
                    field_updated = True

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttonquit:
                    mainrun = False

                if event.ui_element == buttonpause:
                    started = -started
                    fps = 120

                if event.ui_element == buttonrestart:
                    cells = [[0 for j in range(width)] for i in range(height)]
                    cellsn = [[0 for j in range(width)] for i in range(height)]
                    gens = [[[0 for z in range(9)] for j in range(width)] for i in range(height)]
                    gensn = [[[0 for z in range(9)] for j in range(width)] for i in range(height)]

                    cells = [[random.choice([0, 1]) for j in range(width)] for i in range(height)]
                    for i in range(len(cells)):
                        for j in range(len(cells[0])):
                            if cells[i][j] == 1:
                                gens[i][j] = gensrandom()

                    for i in range(len(cells)):
                        for j in range(len(cells[ 0 ])):
                            if cells[ i ][ j ] == 1:
                                gens[ i ][ j ] = gensrandom()

                if event.ui_element == buttonstart:
                    if textwidth.get_text().isdigit():
                        width = int(textwidth.get_text())
                        if width > 90:
                            width = 90

                    if textheight.get_text().isdigit():
                        height = int(textheight.get_text())
                        if height > 54:
                            height = 54

                    if textwidth.get_text().isdigit() and textheight.get_text().isdigit():
                        if started == 0:
                            started = 1

                        buttonstart.hide()
                        buttonpause.show()
                        textwidth.hide()
                        textheight.hide()
                        sliderfps.show()
                        buttonrestart.show()

                        fps = 5

                        screen.fill('#000000')

                        print("width=", width)
                        print("height=", height)

                        cells = [ [ random.choice([ 0, 1 ]) for j in range(width) ] for i in range(height) ]
                        gens = [ [ [ 0 for z in range(9) ] for j in range(width) ] for i
                                 in range(height) ]
                        for i in range(len(cells)):
                            for j in range(len(cells[0])):
                                if cells[i][j] == 1:
                                    gens[i][j] = gensrandom()

                        gensn = [ [ [ 0 for z in range(9) ] for j in range(width) ] for i
                                  in range(height) ]
                        cellsn = [ [ 0 for j in range(width) ] for i in range(height) ]

                        field_updated = True

        manager.process_events(event)

# конец обработки событий интерфейса

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

    if mainrun:

        if field_updated:
            for i in range(0, len(cells)):
                for j in range(0, len(cells[ i ])):
                    red = 85 * (gens[ i ][ j ][ 1 ] + gens[ i ][ j ][ 2 ] + gens[ i ][ j ][ 0 ])
                    blue = 85 * (gens[ i ][ j ][ 7 ] + gens[ i ][ j ][ 8 ] + gens[ i ][ j ][ 6 ])
                    green = 85 * (gens[ i ][ j ][ 4 ] + gens[ i ][ j ][ 5 ] + gens[ i ][ j ][ 3 ])
                    cellcolor = (red, green, blue)
                    pygame.draw.rect(screen, (cellcolor), [ j * 20, i * 20, 20, 20 ])
                # отрисовка

            pygame.display.update()
            field_updated = False

        if started == 1 and not (fps_counter % fps_2): #работа

            field_updated = True


            for i in range(len(cells)):
                for j in range(len(cells[ 0 ])):
                    print(near([ i, j ]), cells[ i ][ j ]);
                    if cells[ i ][ j ] == 1:
                        current_cell_near = near([ i, j ])
                        for counter in range(9):
                            if gens[ i ][ j ][ counter ] == 1:
                                if current_cell_near == counter:
                                    alive = True
                        if alive:
                            cellsn[ i ][ j ] = 1
                            gensn[ i ][ j ] = gens[ i ][ j ]
                        if not alive:
                            cellsn[ i ][ j ] = 0
                            gensn[ i ][ j ] = [ 0 ] * 9
                        alive = False
                        # перепись живых и мертвых на живых

                    if cells[ i ][ j ] == 0:
                        if near([ i, j ]) == 3:
                            cellsn[ i ][ j ] = 1
                            gensn[ i ][ j ] = gennear([i, j])
            # перепись живых и мертвых на мертвых
            cells = cellsn
            gens = gensn

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

        if started ==-1 : #пауза
            started = started

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    if started != 0:
        fps_2 = 26 - sliderfps.get_current_value()
    #clock.tick(fps)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()
