import pygame as pg
import pygame.font


class DrawInputboxes:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.SysFont("Arial", 14).render(text, True, self.color)
        self.active = False

