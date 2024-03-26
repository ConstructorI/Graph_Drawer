import pygame as pg
import pygame.font


class Render:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1200, 720
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)

    def draw(self):
        self.screen.fill(pg.Color('Black'))
        # Пространство графика
        pg.draw.rect(self.screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

        # Горизонтальная линия
        pg.draw.line(self.screen, pg.Color("white"), [200, 670], [1150, 670])

        # Вертикальная линия
        pg.draw.line(self.screen, pg.Color("white"), [200, 50], [200, 675])

        # Конечная линия
        pg.draw.line(self.screen, pg.Color("white"), [1150, 680], [1150, 660])
        pg.draw.line(self.screen, pg.Color("#2c2c2c"), [1150, 50], [1150, 660])
        text = self.font.render(str(int(minutes)), False, pg.Color("white"), None)
        self.screen.blit(text, [1145, 690])

        # Линейка
        for i in range(1, int(minutes)):
            cur = 200 + (950 / int(minutes)) * i
            pg.draw.line(self.screen, pg.Color("white"), [cur, 675], [cur, 665])

        for i in range(0, int((int(minutes) / 10)) + 1):
            cur = 200 + (950 / (int(minutes) / 10)) * i
            pg.draw.line(self.screen, pg.Color("white"), [cur, 680], [cur, 660])
            pg.draw.line(self.screen, pg.Color("#2c2c2c"), [cur, 50], [cur, 660])
            if i == 0:
                text = self.font.render("0", False, pg.Color("white"), None)
            else:
                text = self.font.render(str(i) + "0", False, pg.Color("white"), None)
            self.screen.blit(text, [cur - 5, 690])

    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    minutes = input("введите количество минут: ")
    app = Render()
    app.run()
