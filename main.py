import pygame as pg

class Render:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1200, 720
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def draw(self):
        self.screen.fill(pg.Color('Black'))
        # pg.draw.circle(self.screen, pg.Color("white"), [200, 200], 200)
        pg.draw.line(self.screen, pg.Color("white"), [100, 100], [200, 200])
        pg.draw.rect(self.screen, pg.Color("white"), [100, 200, 200, 200], 1, 50)

    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = Render()
    app.run()
