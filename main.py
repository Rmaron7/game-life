import pygame as pg

def main():
    screen = pg.display.set_mode((1920, 1080))
    font = pg.font.SysFont('Comic Sans MS', 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    x = int()
    y = int()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    counter = int(10)
    messageh = font.render("Введите высоту поля в клетках(0-100). Если вы введете число больше, оно округлится до 100", 1, WHITE, BLACK)
    messagew = font.render("Введите ширину поля в клетках(0-150). Если вы введете число больше, оно округлится до 150", 1, WHITE, BLACK)


    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            while counter > 5:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = GREEN if active else RED
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            height = int(text)
                            text = ''
                            if height > 100:
                                height = 100
                            if height<= 100:
                                counter = 1
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                            height = int(text)
                        else:
                            text += event.unicode
                            height = int(text)


        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)



        for x in range(width):
            pg.draw.aaline(screen, WHITE, [width * 8, 0], [width * 8, height*8], 1)
            pg.draw.aaline(screen, WHITE, [width * 8+1, 0], [width * 8+1, height * 8], 1)

        for x in range(height):
            pg.draw.aaline(screen, WHITE, [0, height*8], [width * 8, height*8], 1)
            pg.draw.aaline(screen, WHITE, [0, height*8+1], [width * 8, height * 8+1], 1)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
