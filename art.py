import pygame as pg
import cv2


class ArtConverter:
    def __init__(self, path='img/1.jpg', font_size=12):
        pg.init()
        self.path = path
        self.img = self.get_img()
        self.RES = self.WIDTH, self.HEIGHT = self.img.shape[0], self.img.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def draw_conv_img(self):
        char_indic = self.img // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indic[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def get_img(self):
        self.cv2_img = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_img)
        gray_img = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2GRAY)
        return gray_img

    def drawCv2(self):
        resize = cv2.resize(self.cv2_img, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resize)

    def draw(self):
        self.surface.fill('black')
        self.draw_conv_img()
        self.drawCv2()

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()


if __name__ == '__main__':
    app = ArtConverter()
    app.run()
