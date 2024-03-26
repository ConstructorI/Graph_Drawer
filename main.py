import pygame as pg
import pygame.font

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pygame.font.SysFont("Arial", 14)
RES = WIDTH, HEIGHT = 1200, 720
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


class DrawScreen:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def send_to_draw(self):
        self.active = False
        self.color = COLOR_INACTIVE
        draw_scale(self.text)
        self.text = ''

    def draw_text(self):
        pg.draw.rect(screen, pg.Color('black'), self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def draw_scale(minutes):
    try:
        int(minutes)
        screen.fill(pg.Color('black'))

        # Graf's space
        pg.draw.rect(screen, pg.Color("#0f0f0f"), [200, 50, 950, 620])

        # Lines
        pg.draw.line(screen, pg.Color("white"), [200, 670], [1150, 670])
        pg.draw.line(screen, pg.Color("white"), [200, 50], [200, 675])

        # Last line
        pg.draw.line(screen, pg.Color("white"), [1150, 680], [1150, 660])
        pg.draw.line(screen, pg.Color("#2c2c2c"), [1150, 50], [1150, 660])
        if ((int(minutes) % 10) > 5) or (int(minutes) < 100):
            text = FONT.render(str(int(minutes)), False, pg.Color("white"), None)
            screen.blit(text, [1145, 690])

        # Scale
        for i in range(1, int(minutes)):
            cur = 200 + (950 / int(minutes)) * i
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
        print("done")
    except ValueError:
        print("no")


def main():
    input_box1 = DrawScreen(50, 50, 30, 25)
    # input_box2 = DrawScreen(50, 150, 25, 25)
    # input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        input_box1.draw_text()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box1.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    input_box1.active = not input_box1.active
                else:
                    input_box1.active = False
                # Change the current color of the input box.
                input_box1.color = COLOR_ACTIVE if input_box1.active else COLOR_INACTIVE

            if event.type == pg.KEYDOWN:
                if input_box1.active is True:
                    if event.key == pg.K_RETURN:
                        screen.fill(pg.Color('black'))
                        input_box1.send_to_draw()
                    elif event.key == pg.K_BACKSPACE:
                        input_box1.text = ''
                        input_box1.draw_text()
                    else:
                        input_box1.text += event.unicode
                        input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                        input_box1.draw_text()

        [exit() for i in pg.event.get() if i.type == pg.QUIT]
        pg.display.set_caption(str(clock.get_fps()))
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
