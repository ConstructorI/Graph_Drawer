import numpy as np
import pandas as pd
import pygame as pg
import pygame.font
import openpyxl as op
import random

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pygame.font.SysFont("Arial", 14)
FONT2 = pygame.font.SysFont("Arial", 16)
RES = WIDTH, HEIGHT = 1200, 720
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()
steps = [200]


def initialize_steps():
    steps = [200]
    return steps





class DrawLines:
    def __init__(self):
        self.lines_coord = []
        self.graf_space = pg.Rect(200, 50, 1000, 620)
        self.prev_step = steps[0]
        self.prev_pos = (200, 670)
        self.temp = 0
        self.count = 1

    def draw_lines(self, pos):
        try:
            if pos[0] > steps[0]:
                self.lines_coord.append((steps[0], pos[1]))
                pg.draw.line(screen, pg.Color("white"), [self.prev_step, self.prev_pos[1]], [steps[0], pos[1]])
                self.prev_step = steps[0]
                self.prev_pos = pos
                steps.pop(0)
                print(self.lines_coord)
        except IndexError:
            pass

    def save(self):
        wb = op.load_workbook("Test.xlsx")
        sheet = wb.active
        i = 0
        for y in self.lines_coord:
            i += 1
            sheet.cell(row=i+1, column=1).value = i
            sheet.cell(row=i+1, column=self.count + 1).value = (670 - y[1]) * (int(self.temp) / 620)
        sheet.cell(row=1, column=1).value = 0
        sheet.cell(row=2, column=1).value = 1
        sheet.cell(row=1, column=self.count + 1).value = random.uniform(18, 20)
        self.count += 1
        wb.save("Test.xlsx")

    def load_from_excel(self):
        df = pd.read_excel("Test.xlsx")
        data_array = df.to_numpy()
        transposed_array = data_array.transpose()
        transposed_array = transposed_array[1:]
        transposed_array = transposed_array.tolist()
        print(transposed_array)
        for i in transposed_array:
            n = 0
            for y in i:
                try:
                    if n == 0:
                        pg.draw.line(screen, pg.Color("gray"), [200, 670], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.temp))])
                    n += 1
                    pg.draw.line(screen, pg.Color("gray"), [200 + (n - 1) * len(transposed_array) / 950, (670 - float(i.index(y - 1))) * (620 / int(self.temp))], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.temp))])
                    print([200 + (n - 1) * len(transposed_array) / 950, (670 - float(i.index(y - 1))) * (620 / int(self.temp))], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.temp))])
                except ValueError:
                    pass

    def update(self):
        steps = initialize_steps()
        self.prev_step = steps[0]
        self.prev_pos = (200, 670)
        self.lines_coord = []


class DrawInputboxes:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def send_to_draw_hor(self, text2, text3):
        self.active = False
        self.color = COLOR_INACTIVE
        draw_scale_hor(self.text, text2, text3)
        self.text = ''

    def draw_text(self):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def draw_scale_vert(temperature, limit):
    try:
        int(temperature)
        int(limit)

        # Last line
        pg.draw.line(screen, pg.Color("white"), [190, 50], [210, 50])
        pg.draw.line(screen, pg.Color("#2c2c2c"), [200, 50], [1150, 50])
        text = FONT.render(str(int(temperature)), False, pg.Color("white"), None)
        screen.blit(text, [165, 43])

        # Scale
        for i in range(0, int((int(temperature) / 10)) + 1):
            cur = 670 - (620 / (int(temperature) / 10)) * i
            if i % 1 == 0:
                pg.draw.line(screen, pg.Color("white"), [195, cur], [205, cur])
                pg.draw.line(screen, pg.Color("#2c2c2c"), [200, cur], [1150, cur])
            if i == 0:
                text = FONT.render("0", False, pg.Color("white"), None)
            else:
                if i % 10 == 0:
                    pg.draw.line(screen, pg.Color("white"), [190, cur], [210, cur])
                    text = FONT.render(str(i) + "0", False, pg.Color("white"), None)
                    screen.blit(text, [165, cur - 7])

        # Lines
        pg.draw.line(screen, pg.Color("white"), [200, 50], [200, 675])
        pg.draw.line(screen, pg.Color("white"), [200, 670], [1150, 670])

        # Limit line
        limit_line = 670 - (620 / int(temperature)) * int(limit)
        pg.draw.line(screen, pg.Color("#640000"), [200, limit_line], [1150, limit_line])

        print("done")
        print(steps)
    except ValueError:
        print("no")


def draw_scale_hor(minutes, temperature, limit):
    try:
        int(minutes)
        int(temperature)
        int(limit)

        # Last line
        pg.draw.line(screen, pg.Color("white"), [1150, 680], [1150, 660])
        pg.draw.line(screen, pg.Color("#2c2c2c"), [1150, 50], [1150, 660])
        if ((int(minutes) % 10) > 5) or (int(minutes) < 100):
            text = FONT.render(str(int(minutes)), False, pg.Color("white"), None)
            screen.blit(text, [1145, 690])

        steps.clear()
        # Scale
        for i in range(1, int(minutes)):
            cur = 200 + (950 / int(minutes)) * i
            steps.append(cur)
            pg.draw.line(screen, pg.Color("white"), [cur, 675], [cur, 665])
        for i in range(0, int((int(minutes) / 10)) + 1):
            cur = 200 + (950 / (int(minutes) / 10)) * i
            pg.draw.line(screen, pg.Color("white"), [cur, 680], [cur, 660])
            pg.draw.line(screen, pg.Color("#2c2c2c"), [cur, 50], [cur, 660])
            if i == 0:
                text = FONT.render("0", False, pg.Color("white"), None)
            else:
                text = FONT.render(str(i) + "0", False, pg.Color("white"), None)
            screen.blit(text, [cur - 5, 690])

        steps.append(1150)
        # Lines
        pg.draw.line(screen, pg.Color("white"), [200, 670], [1150, 670])
        draw_scale_vert(temperature, limit)
        print("done")
        print(steps)
    except ValueError:
        print("no")


lines = DrawLines()


def main():
    # df = pd.read_excel("test.xlsx")
    # data_array = df.to_numpy()

    initialize_steps()
    screen.fill(pg.Color('black'))

    temperature_input = DrawInputboxes(20, 50, 50, 25)
    limit_input = DrawInputboxes(20, 125, 50, 25)
    time_input = DrawInputboxes(20, 200, 50, 25)
    clear_button = DrawInputboxes(20, 645, 62, 25)
    add_line_button = DrawInputboxes(20, 275, 85, 25)

    pg.draw.rect(screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])
    text = FONT2.render("Температура", False, pg.Color("white"), None)
    screen.blit(text, [20, 25])
    text = FONT2.render("Вылет", False, pg.Color("white"), None)
    screen.blit(text, [20, 100])
    text = FONT2.render("Время", False, pg.Color("white"), None)
    screen.blit(text, [20, 175])
    text = FONT2.render("Добавить ТП", False, pg.Color("white"), None)
    screen.blit(text, [23, 278])
    text = FONT2.render("Очистить", False, pg.Color("white"), None)
    screen.blit(text, [23, 648])

    done = False

    while not done:
        time_input.draw_text()
        temperature_input.draw_text()
        clear_button.draw_text()
        limit_input.draw_text()
        add_line_button.draw_text()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if pg.mouse.get_pressed()[0]:
                if lines.graf_space.collidepoint(event.pos):
                    pos = pg.mouse.get_pos()
                    pg.time.delay(1)
                    lines.draw_lines(pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if time_input.rect.collidepoint(event.pos):
                    time_input.active = not time_input.active
                    temperature_input.active = False
                    limit_input.active = False

                elif temperature_input.rect.collidepoint(event.pos):
                    temperature_input.active = not temperature_input.active
                    time_input.active = False
                    limit_input.active = False

                elif limit_input.rect.collidepoint(event.pos):
                    limit_input.active = not limit_input.active
                    time_input.active = False
                    temperature_input.active = False

                elif add_line_button.rect.collidepoint(event.pos):
                    lines.save()
                    lines.load_from_excel()
                    lines.update()

                elif clear_button.rect.collidepoint(event.pos):
                    initialize_steps()
                    lines.update()
                    done = True
                    main()
                else:
                    time_input.active = False
                    temperature_input.active = False
                    limit_input.active = False
                # Change the current color of the input box.
                time_input.color = COLOR_ACTIVE if time_input.active else COLOR_INACTIVE
                temperature_input.color = COLOR_ACTIVE if temperature_input.active else COLOR_INACTIVE
                limit_input.color = COLOR_ACTIVE if limit_input.active else COLOR_INACTIVE

            if event.type == pg.KEYDOWN:
                if time_input.active is True:
                    pg.draw.rect(screen, pg.Color('black'), time_input.rect)
                    if event.key == pg.K_RETURN:
                        screen.fill(pg.Color('black'))
                        pg.draw.rect(screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

                        text = FONT2.render("Температура", False, pg.Color("white"), None)
                        screen.blit(text, [20, 25])
                        text = FONT2.render("Вылет", False, pg.Color("white"), None)
                        screen.blit(text, [20, 100])
                        text = FONT2.render("Время", False, pg.Color("white"), None)
                        screen.blit(text, [20, 175])
                        text = FONT2.render("Добавить ТП", False, pg.Color("white"), None)
                        screen.blit(text, [23, 278])
                        text = FONT2.render("Очистить", False, pg.Color("white"), None)
                        screen.blit(text, [23, 648])

                        time_input.send_to_draw_hor(temperature_input.text, limit_input.text)
                        lines.temp = str(temperature_input.text)
                        temperature_input.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        pg.draw.rect(screen, pg.Color('black'), time_input.rect)
                        time_input.text = ''
                        time_input.draw_text()
                    else:
                        time_input.text += event.unicode
                        time_input.txt_surface = FONT.render(time_input.text, True, time_input.color)
                        time_input.draw_text()

                elif temperature_input.active is True:
                    pg.draw.rect(screen, pg.Color('black'), temperature_input.rect)
                    if event.key == pg.K_RETURN:
                        limit_input.active = True
                        limit_input.color = COLOR_ACTIVE
                        temperature_input.draw_text()
                        temperature_input.color = COLOR_INACTIVE
                        temperature_input.active = False
                    elif event.key == pg.K_BACKSPACE:
                        temperature_input.text = ''
                        temperature_input.draw_text()
                    else:
                        temperature_input.text += event.unicode
                        temperature_input.txt_surface = FONT.render(temperature_input.text, True, temperature_input.color)
                        temperature_input.draw_text()

                elif limit_input.active is True:
                    pg.draw.rect(screen, pg.Color('black'), limit_input.rect)
                    if event.key == pg.K_RETURN:
                        time_input.active = True
                        time_input.color = COLOR_ACTIVE
                        limit_input.draw_text()
                        limit_input.color = COLOR_INACTIVE
                        limit_input.active = False
                    elif event.key == pg.K_BACKSPACE:
                        limit_input.text = ''
                        limit_input.draw_text()
                    else:
                        limit_input.text += event.unicode
                        limit_input.txt_surface = FONT.render(limit_input.text, True, limit_input.color)
                        limit_input.draw_text()

        [exit() for i in pg.event.get() if i.type == pg.QUIT]
        pg.display.set_caption(str(clock.get_fps()))
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
