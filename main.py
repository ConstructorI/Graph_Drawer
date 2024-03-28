import pandas as pd
import pygame as pg
import numpy as np
from MainWindow import MainWindow
from InputBoxesClass import DrawInputboxes
from LinesClass import DrawLines


class RunAction:
    def __init__(self):
        self.ScreenMain = MainWindow()

        # Переменные, записывающие исходные данные
        self.steps = [200]
        self.temperature = 0
        self.time = 0
        self.limit = 0
        self.limit_2 = 0
        self.average = []

        # Объекты
        self.temperature_input = DrawInputboxes(55, 50, 50, 25, '250')
        self.limit_input = DrawInputboxes(20, 125, 50, 25, '180')
        self.limit_input_2 = DrawInputboxes(90, 125, 50, 25, '200')
        self.time_input = DrawInputboxes(55, 200, 50, 25)

        self.clear_button = DrawInputboxes(32, 645, 95, 25)
        self.add_line_button = DrawInputboxes(32, 300, 95, 25)
        self.add_avg_button = DrawInputboxes(32, 350, 95, 25)

        self.lines = DrawLines(0, [200])

    def run(self):

        # Бэкграунд
        self.ScreenMain.screen.fill(pg.Color('black'))

        # Поле графика
        pg.draw.rect(self.ScreenMain.screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

        # Подписи кнопок и полей ввода
        text = self.ScreenMain.FONT2.render("Температура", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [38, 25])
        text = self.ScreenMain.FONT2.render("Вылет", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [23, 100])
        text = self.ScreenMain.FONT2.render("Время", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [58, 175])
        text = self.ScreenMain.FONT2.render("Вылет 2", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [89, 100])
        text = self.ScreenMain.FONT2.render("Добавить ТП", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [36, 302])
        text = self.ScreenMain.FONT2.render("Средняя", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [50, 352])
        text = self.ScreenMain.FONT2.render("Очистить", False, pg.Color("white"), None)
        self.ScreenMain.screen.blit(text, [49, 648])

        # Для рабочих циклов
        done = False
        time_inp_check = False
        temp_inp_check = False
        lim_inp_check = False
        lim_2_inp_check = False

        # Основной цикл
        while not done:

            # Отображает введённые данные и поле ввода
            self.draw_text(self.time_input)
            self.draw_text(self.temperature_input)
            self.draw_text(self.clear_button)
            self.draw_text(self.limit_input)
            self.draw_text(self.limit_input_2)

            self.draw_text(self.add_line_button)
            self.draw_text(self.add_avg_button)
            self.draw_text(self.clear_button)

            # Все тыки пользователя направляются сюда
            for event in pg.event.get():

                # Если хочет уйти - пусть идёт
                if event.type == pg.QUIT:
                    done = True

                # Если зажал кнопку мыши на поле графика - рисует линию
                if pg.mouse.get_pressed()[0]:
                    try:
                        if self.lines.graf_space.collidepoint(event.pos):
                            pos = pg.mouse.get_pos()
                            pg.time.delay(1)
                            self.draw_lines(pos)
                    except AttributeError:
                        pass

                # Если нажал кнопку мыши на полях - делает их активными
                # Ну и функции кнопочек
                if event.type == pg.MOUSEBUTTONDOWN:

                    if self.time_input.rect.collidepoint(event.pos):
                        self.time_input.active = not self.time_input.active
                        self.temperature_input.active = False
                        self.limit_input.active = False
                        self.limit_input_2.active = False

                    elif self.temperature_input.rect.collidepoint(event.pos):
                        self.temperature_input.active = not self.temperature_input.active
                        self.time_input.active = False
                        self.limit_input.active = False
                        self.limit_input_2.active = False

                    elif self.limit_input.rect.collidepoint(event.pos):
                        self.limit_input.active = not self.limit_input.active
                        self.time_input.active = False
                        self.temperature_input.active = False
                        self.limit_input_2.active = False

                    elif self.limit_input_2.rect.collidepoint(event.pos):
                        self.limit_input_2.active = not self.limit_input_2.active
                        self.time_input.active = False
                        self.temperature_input.active = False
                        self.limit_input.active = False

                    elif self.add_line_button.rect.collidepoint(event.pos):
                        self.lines.save()
                        self.load_lines_from_excel()
                        self.lines_update()

                    elif self.add_avg_button.rect.collidepoint(event.pos):
                        self.draw_avr()

                    elif self.clear_button.rect.collidepoint(event.pos):
                        self.lines_update()
                        done = True
                        self.lines.lines_coord_2 = []
                        self.lines.count = 1
                        self.lines.count_of_saves += 1
                        self.run()
                    else:
                        self.time_input.active = False
                        self.temperature_input.active = False
                        self.limit_input.active = False
                        self.limit_input_2.active = False

                    # Перекрашивает поля ввода когда надо
                    self.time_input.color = self.ScreenMain.COLOR_ACTIVE \
                        if self.time_input.active else self.ScreenMain.COLOR_INACTIVE
                    self.temperature_input.color = self.ScreenMain.COLOR_ACTIVE \
                        if self.temperature_input.active else self.ScreenMain.COLOR_INACTIVE
                    self.limit_input.color = self.ScreenMain.COLOR_ACTIVE \
                        if self.limit_input.active else self.ScreenMain.COLOR_INACTIVE
                    self.limit_input_2.color = self.ScreenMain.COLOR_ACTIVE \
                        if self.limit_input_2.active else self.ScreenMain.COLOR_INACTIVE

                # Если клаву тыкает
                if event.type == pg.KEYDOWN:

                    if self.time_input.active is True:

                        # это надо чтоб не было всякой непотребщины
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.time_input.rect)

                        # Энтер он нажал и график появился
                        if event.key == pg.K_RETURN:
                            self.ScreenMain.screen.fill(pg.Color('black'))
                            pg.draw.rect(self.ScreenMain.screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])
                            text = self.ScreenMain.FONT2.render("Температура", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [38, 25])
                            text = self.ScreenMain.FONT2.render("Вылет", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [23, 100])
                            text = self.ScreenMain.FONT2.render("Время", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [58, 175])
                            text = self.ScreenMain.FONT2.render("Вылет 2", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [89, 100])
                            text = self.ScreenMain.FONT2.render("Добавить ТП", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [36, 302])
                            text = self.ScreenMain.FONT2.render("Средняя", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [50, 352])
                            text = self.ScreenMain.FONT2.render("Очистить", False, pg.Color("white"), None)
                            self.ScreenMain.screen.blit(text, [49, 648])
                            self.lines.temp = str(self.temperature_input.text)
                            self.temperature = str(self.temperature_input.text)
                            self.time = str(self.time_input.text)
                            self.limit = str(self.limit_input.text)
                            self.limit_2 = str(self.limit_input_2.text)
                            self.time_input.active = False
                            self.time_input.color = pg.Color('lightskyblue3')
                            self.draw_scale_hor(self.time, self.temperature, self.limit, self.limit_2)
                            self.draw_text(self.time_input)
                            self.time_input.text = ''

                        elif event.key == pg.K_BACKSPACE:
                            pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.time_input.rect)
                            self.time_input.text = ''
                            self.draw_text(self.time_input)
                            time_inp_check = True
                        else:
                            time_inp_check = False
                            self.time_input.text += event.unicode
                            self.time_input.txt_surface = self.ScreenMain.FONT.render(
                                self.time_input.text, True, self.time_input.color)
                            self.draw_text(self.time_input)

                    # В остальных функционал поменьше - максимум на следующий по порядку инпут отправить после тыка
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
                            temp_inp_check = True
                        else:
                            temp_inp_check = False
                            self.temperature_input.text += event.unicode
                            self.temperature_input.txt_surface = self.ScreenMain.FONT.render(
                                self.temperature_input.text, True, self.temperature_input.color)
                            self.draw_text(self.temperature_input)

                    elif self.limit_input.active is True:
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.limit_input.rect)

                        if event.key == pg.K_RETURN:
                            self.limit_input_2.active = True
                            self.limit_input_2.color = self.ScreenMain.COLOR_ACTIVE
                            self.draw_text(self.limit_input)
                            self.limit_input.color = self.ScreenMain.COLOR_INACTIVE
                            self.limit_input.active = False

                        elif event.key == pg.K_BACKSPACE:
                            self.limit_input.text = ''
                            self.draw_text(self.limit_input)
                            lim_inp_check = True
                        else:
                            lim_inp_check = False
                            self.limit_input.text += event.unicode
                            self.limit_input.txt_surface = self.ScreenMain.FONT.render(self.limit_input.text,
                                                                                       True, self.limit_input.color)
                            self.draw_text(self.limit_input)

                    elif self.limit_input_2.active is True:
                        pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), self.limit_input_2.rect)

                        if event.key == pg.K_RETURN:
                            self.time_input.active = True
                            self.time_input.color = self.ScreenMain.COLOR_ACTIVE
                            self.draw_text(self.limit_input_2)
                            self.limit_input_2.color = self.ScreenMain.COLOR_INACTIVE
                            self.limit_input_2.active = False

                        elif event.key == pg.K_BACKSPACE:
                            self.limit_input_2.text = ''
                            self.draw_text(self.limit_input_2)
                            lim_2_inp_check = True
                        else:
                            lim_2_inp_check = False
                            self.limit_input_2.text += event.unicode
                            self.limit_input_2.txt_surface = self.ScreenMain.FONT.render(self.limit_input_2.text,
                                                                                       True, self.limit_input_2.color)
                            self.draw_text(self.limit_input_2)

            # Самая кривая реализация Backspace что я видел
            if time_inp_check:
                pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), [57, 202, 46, 22])
            if temp_inp_check:
                pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), [57, 52, 46, 22])
            if lim_inp_check:
                pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), [22, 127, 46, 22])
            if lim_2_inp_check:
                pg.draw.rect(self.ScreenMain.screen, pg.Color('black'), [92, 127, 46, 22])

            # Снова выход
            [exit() for i in pg.event.get() if i.type == pg.QUIT]

            # FPS вверху окошка по приколу))
            pg.display.set_caption(str(self.ScreenMain.clock.get_fps()))

            # флип
            pg.display.flip()

            # часики по FPS
            self.ScreenMain.clock.tick(self.ScreenMain.FPS)

    def draw_lines(self, pos):

        # Рисуем линии
        try:
            if pos[0] > self.lines.line_steps[0]:
                self.lines.lines_coord.append([self.steps[0], pos[1]])
                self.lines.lines_coord_2.append([[[self.lines.prev_step, self.lines.prev_pos[1]],
                                                  [self.lines.line_steps[0], pos[1]]]])
                self.lines.lines_coord_3.append([[self.lines.prev_step, self.lines.prev_pos[1]],
                                                 [self.lines.line_steps[0], pos[1]]])
                pg.draw.line(self.ScreenMain.screen, pg.Color("white"),
                             [self.lines.prev_step, self.lines.prev_pos[1]],
                             [self.lines.line_steps[0], pos[1]])
                self.lines.prev_step = self.lines.line_steps[0]
                self.lines.prev_pos = pos
                self.lines.line_steps.pop(0)

        except IndexError:
            pass

    def load_lines_from_excel(self):

        # Рисуем серые линии
        try:
            self.draw_scale_hor(self.time, self.temperature, self.limit, self.limit_2)
            for u in self.lines.lines_coord_2:
                for i in u:
                    pg.draw.line(self.ScreenMain.screen, pg.Color("#404040"), i[0], i[1])
        except (IndexError, FileNotFoundError, ZeroDivisionError, ValueError):
            pass

    def draw_avr(self):

        # Рисуем средние линии (Тоже серые. Мне лень нормально прописывать обновление экрана)
        try:
            df = pd.read_excel("Test" + str(self.lines.count_of_saves) + ".xlsx")
            data_array = df.to_numpy()
            trans_data = data_array.transpose()
            trans_data = trans_data[1:]
            self.average = np.average(trans_data, axis=0)

            for i in range(len(self.steps)):
                if i == 0:
                    pg.draw.line(self.ScreenMain.screen, pg.Color("red"),
                                 [200, 670],
                                 [self.steps[0], (670 - (int(self.average[0]) * 620 / int(self.temperature)))])
                else:
                    pg.draw.line(self.ScreenMain.screen, pg.Color("red"),
                                 [self.steps[i - 1], (670 - (int(self.average[i - 1]) * 620 / int(self.temperature)))],
                                 [self.steps[i], (670 - (int(self.average[i]) * 620 / int(self.temperature)))])

        except (IndexError, FileNotFoundError, ZeroDivisionError, ValueError):
            pass

    def lines_update(self):

        # Обновнение переменных
        self.lines.prev_step = 200
        self.lines.prev_pos = (200, 670)
        self.lines.lines_coord = []

    def draw_text(self, obj):

        # Пишем текст объекта класса InputBoxes
        self.ScreenMain.screen.blit(obj.txt_surface, (obj.rect.x+5, obj.rect.y+5))
        pg.draw.rect(self.ScreenMain.screen, obj.color, obj.rect, 2)

    def draw_scale_vert(self, temperature, limit, limit_2):

        # Магия вертикальной разлинейки
        try:
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [190, 50], [210, 50])
            pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [200, 50], [1150, 50])
            text = self.ScreenMain.FONT.render(str(int(temperature)), False, pg.Color("white"), None)
            self.ScreenMain.screen.blit(text, [165, 43])

            for i in range(0, int((int(temperature) / 10)) + 1):
                cur = 670 - (620 / (int(temperature) / 10)) * i
                if i % 1 == 0:
                    pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [195, cur], [205, cur])
                    pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [200, cur], [1150, cur])
                if i == 0:
                    pass
                else:
                    if i % 10 == 0:
                        pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [190, cur], [210, cur])
                        text = self.ScreenMain.FONT.render(str(i) + "0", False, pg.Color("white"), None)
                        self.ScreenMain.screen.blit(text, [165, cur - 7])

            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 50], [200, 675])
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 670], [1150, 670])

            limit_line = 670 - (620 / int(temperature)) * int(limit)
            pg.draw.line(self.ScreenMain.screen, pg.Color("#640000"), [200, limit_line], [1150, limit_line])

            if limit_2 == '':
                pass
            else:
                limit_line_2 = 670 - (620 / int(temperature)) * int(limit_2)
                pg.draw.line(self.ScreenMain.screen, pg.Color("#640000"), [200, limit_line_2], [1150, limit_line_2])

            print("done")
        except ValueError:
            print("no")

    def draw_scale_hor(self, minutes, temperature, limit, limit_2):

        # Магия горизонтальной разлинейки
        try:
            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [1150, 680], [1150, 660])
            pg.draw.line(self.ScreenMain.screen, pg.Color("#2c2c2c"), [1150, 50], [1150, 660])
            if ((int(minutes) % 10) > 5) or (int(minutes) < 100):
                text = self.ScreenMain.FONT.render(str(int(minutes)), False, pg.Color("white"), None)
                self.ScreenMain.screen.blit(text, [1145, 690])
            self.lines.line_steps.clear()
            self.steps.clear()

            for i in range(1, int(minutes)):
                cur = 200 + (950 / int(minutes)) * i
                self.steps.append(cur)
                self.lines.line_steps.append(cur)
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
            self.lines.line_steps.append(1150)

            pg.draw.line(self.ScreenMain.screen, pg.Color("white"), [200, 670], [1150, 670])
            self.draw_scale_vert(temperature, limit, limit_2)

            print("done")
        except ValueError:
            print("no")


if __name__ == '__main__':
    app = RunAction()
    app.run()
