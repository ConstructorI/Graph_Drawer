import numpy as np
import pandas as pd
import pygame as pg
import pygame.font
import openpyxl as op
import random
from MainWindow import MainWindow
from InputBoxesClass import DrawInputboxes
from LinesClass import DrawLines


class RunAction:
    def __init__(self):
        self.ScreenMain = MainWindow()
        self.steps = [200]
        self.temperature = 0
        self.time = 0
        self.limit = 0

        self.temperature_input = DrawInputboxes(20, 50, 50, 25)
        self.limit_input = DrawInputboxes(20, 125, 50, 25)
        self.time_input = DrawInputboxes(20, 200, 50, 25)
        self.clear_button = DrawInputboxes(20, 645, 62, 25)
        self.add_line_button = DrawInputboxes(20, 275, 85, 25)

        self.lines = DrawLines(0, self.steps)

    def run(self):
        self.initialize_steps()
        self.ScreenMain.screen.fill(pg.Color('black'))

        pg.draw.rect(self.ScreenMain.screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

        text = self.ScreenMain.FONT2.render("Температура", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [20, 25])
        text = self.ScreenMain.FONT2.render("Вылет", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [20, 100])
        text = self.ScreenMain.FONT2.render("Время", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [20, 175])
        text = self.ScreenMain.FONT2.render("Добавить ТП", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [23, 278])
        text = self.ScreenMain.FONT2.render("Очистить", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [23, 648])

        done = False

        while not done:
            self.draw_text(self.time_input)
            self.draw_text(self.temperature_input)
            self.draw_text(self.clear_button)
            self.draw_text(self.limit_input)
            self.draw_text(self.add_line_button)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if pg.mouse.get_pressed()[0]:
                    if self.lines.graf_space.collidepoint(event.pos):
                        pos = pg.mouse.get_pos()
                        pg.time.delay(1)
                        self.draw_lines(pos)

                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if self.time_input.rect.collidepoint(event.pos):
                        self.time_input.active = not self.time_input.active
                        self.temperature_input.active = False
                        self.limit_input.active = False

                    elif self.temperature_input.rect.collidepoint(event.pos):
                        self.temperature_input.active = not self.temperature_input.active
                        self.time_input.active = False
                        self.limit_input.active = False

                    elif self.limit_input.rect.collidepoint(event.pos):
                        self.limit_input.active = not self.limit_input.active
                        self.time_input.active = False
                        self.temperature_input.active = False

                    elif self.add_line_button.rect.collidepoint(event.pos):
                        self.lines.save()
                        self.lines.load_from_excel()
                        self.lines_update()

                    elif self.clear_button.rect.collidepoint(event.pos):
                        self.initialize_steps()
                        self.lines_update()
                        done = True
                    else:
                        self.time_input.active = False
                        self.temperature_input.active = False
                        self.limit_input.active = False
                    # Change the current color of the input box.
                    self.time_input.color = self.ScreenMain.COLOR_ACTIVE if self.time_input.active else self.ScreenMain.COLOR_INACTIVE
                    self.temperature_input.color = self.ScreenMain.COLOR_ACTIVE if self.temperature_input.active else self.ScreenMain.COLOR_INACTIVE
                    self.limit_input.color = self.ScreenMain.COLOR_ACTIVE if self.limit_input.active else self.ScreenMain.COLOR_INACTIVE

                if event.type == pg.KEYDOWN:
                    if self.time_input.active is True:
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.time_input.rect)
                        if event.key == pg.K_RETURN:
                            self.ScreenMain.screen.fill(pg.Color('black'))
                            pg.draw.rect(self.ScreenMain.screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

                            text = self.ScreenMain.FONT2.render("Температура", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [20, 25])
                            text = self.ScreenMain.FONT2.render("Вылет", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [20, 100])
                            text = self.ScreenMain.FONT2.render("Время", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [20, 175])
                            text = self.ScreenMain.FONT2.render("Добавить ТП", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [23, 278])
                            text = self.ScreenMain.FONT2.render("Очистить", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [23, 648])

                            self.send_to_draw_hor(self.temperature_input.text, self.limit_input.text, self.time_input)
                            self.lines.temp = str(self.temperature_input.text)
                            self.temperature_input.text = ''
                        elif event.key == pg.K_BACKSPACE:
                            pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.time_input.rect)
                            self.time_input.text = ''
                            self.draw_text(self.time_input)
                        else:
                            self.time_input.text += event.unicode
                            self.time_input.txt_surface = self.ScreenMain.FONT.render(self.time_input.text, True, self.time_input.color)
                            self.draw_text(self.time_input)

                    elif self.temperature_input.active is True:
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.temperature_input.rect)
                        if event.key == pg.K_RETURN:
                            self.limit_input.active = True
                            self.limit_input.color = self.ScreenMain.COLOR_ACTIVE
                            self.draw_text(self.temperature_input)
                            self.temperature_input.color = self.ScreenMain.COLOR_INACTIVE
                            self.temperature_input.active = False
                        elif event.key == pg.K_BACKSPACE:
                            self.temperature_input.text = ''
                            self.draw_text(self.temperature_input)
                        else:
                            self.temperature_input.text += event.unicode
                            self.temperature_input.txt_surface = self.ScreenMain.FONT.render(self.temperature_input.text, True,
                                                                                            self.temperature_input.color)
                            self.draw_text(self.temperature_input)

                    elif self.limit_input.active is True:
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.limit_input.rect)
                        if event.key == pg.K_RETURN:
                            self.time_input.active = True
                            self.time_input.color = self.ScreenMain.COLOR_ACTIVE
                            self.draw_text(self.limit_input)
                            self.limit_input.color = self.ScreenMain.COLOR_INACTIVE
                            self.limit_input.active = False
                        elif event.key == pg.K_BACKSPACE:
                            self.limit_input.text = ''
                            self.draw_text(self.limit_input)
                        else:
                            self.limit_input.text += event.unicode
                            self.limit_input.txt_surface = self.ScreenMain.FONT.render(self.limit_input.text, True, self.limit_input.color)
                            self.draw_text(self.limit_input)

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.ScreenMain.clock.get_fps()))
            pg.display.flip()
            self.ScreenMain.clock.tick(self.ScreenMain.FPS)

    def draw_lines(self, pos):
        try:
            if pos[0] > self.lines.steps[0]:
                self.lines.lines_coord.append((self.steps[0], pos[1]))
                pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [self.lines.prev_step, self.lines.prev_pos[1]], [self.lines.steps[0], pos[1]])
                self.lines.prev_step = self.lines.steps[0]
                self.lines.prev_pos = pos
                self.lines.steps.pop(0)
                print(self.lines.lines_coord)
        except IndexError:
            pass

    def load_lines_from_excel(self):
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
                        pg.draw.line(self.ScreenMain.screen, pg.Color("gray"), [200, 670], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.lines.temp))])
                    n += 1
                    pg.draw.line(self.ScreenMain.screen, pg.Color("gray"), [200 + (n - 1) * len(transposed_array) / 950, (670 - float(i.index(y - 1))) * (620 / int(self.lines.temp))], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.lines.temp))])
                    print([200 + (n - 1) * len(transposed_array) / 950, (670 - float(i.index(y - 1))) * (620 / int(self.lines.temp))], [200 + n * len(transposed_array) / 950, (670 - float(y)) * (620 / int(self.lines.temp))])
                except ValueError:
                    pass

    def lines_update(self):
        self.lines.steps = self.initialize_steps()
        self.lines.prev_step = self.lines.steps[0]
        self.lines.prev_pos = (200, 670)
        self.lines.lines_coord = []

    def initialize_steps(self):
        self.ScreenMain.steps = [200]
        return self.ScreenMain.steps

    def send_to_draw_hor(self, text2, text3, obj):
        obj.active = False
        obj.color = pg.Color('lightskyblue3')
        self.draw_scale_hor(obj.text, text2, text3)
        obj.text = ''

    def draw_text(self, obj):
        self.ScreenMain.screen.blit(obj.txt_surface, (obj.rect.x+5, obj.rect.y+5))
        pg.draw.rect(self.ScreenMain.screen, obj.color, obj.rect, 2)

    def draw_scale_vert(self, temperature, limit):
        try:
            int(temperature)
            int(limit)

            # Last line
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [190, 50], [210, 50])
            pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [200, 50], [1150, 50])
            text = self.ScreenMain.FONT.render(str(int(temperature)), False, pg.Color("white"), None)
            self.ScreenMain.screen.blit(text, [165, 43])

            # Scale
            for i in range(0, int((int(temperature) / 10)) + 1):
                cur = 670 - (620 / (int(temperature) / 10)) * i
                if i % 1 == 0:
                    pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [195, cur], [205, cur])
                    pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [200, cur], [1150, cur])
                if i == 0:
                    text = self.ScreenMain.FONT.render("0", False, pg.Color("white"), None)
                else:
                    if i % 10 == 0:
                        pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [190, cur], [210, cur])
                        text = self.ScreenMain.FONT.render(str(i) + "0", False, pg.Color("white"), None)
                        self.ScreenMain.screen.blit(text, [165, cur - 7])

            # Lines
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 50], [200, 675])
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 670], [1150, 670])

            # Limit line
            limit_line = 670 - (620 / int(temperature)) * int(limit)
            pg.draw.line(self.ScreenMain.screen, pg.Color("#640000"), [200, limit_line], [1150, limit_line])

            print("done")
            print(self.steps)
        except ValueError:
            print("no")

    def draw_scale_hor(self, minutes, temperature, limit):
        try:
            int(minutes)
            int(temperature)
            int(limit)

            # Last line
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [1150, 680], [1150, 660])
            pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [1150, 50], [1150, 660])
            if ((int(minutes) % 10) > 5) or (int(minutes) < 100):
                text = self.ScreenMain.FONT.render(str(int(minutes)), False, pg.Color("white"), None)
                self.ScreenMain.screen.blit(text, [1145, 690])

            self.steps.clear()
            # Scale
            for i in range(1, int(minutes)):
                cur = 200 + (950 / int(minutes)) * i
                self.steps.append(cur)
                pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [cur, 675], [cur, 665])
            for i in range(0, int((int(minutes) / 10)) + 1):
                cur = 200 + (950 / (int(minutes) / 10)) * i
                pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [cur, 680], [cur, 660])
                pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [cur, 50], [cur, 660])
                if i == 0:
                    text = self.ScreenMain.FONT.render("0", False, pg.Color("white"), None)
                else:
                    text = self.ScreenMain.FONT.render(str(i) + "0", False, pg.Color("white"), None)
                self.ScreenMain.screen.blit(text, [cur - 5, 690])

            self.steps.append(1150)
            # Lines
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 670], [1150, 670])
            self.draw_scale_vert(temperature, limit)
            print("done")
            print(self.steps)
        except ValueError:
            print("no")


if __name__ == '__main__':
    app = RunAction()
    app.run()
