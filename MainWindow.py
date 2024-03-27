import pygame as pg
import pygame.font


class MainWindow:
    def __init__(self):
        pg.init()
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.FONT = pygame.font.SysFont("Arial", 14)
        self.FONT2 = pygame.font.SysFont("Arial", 16)
        self.WIDTH = 1200
        self.HEIGHT = 720
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()