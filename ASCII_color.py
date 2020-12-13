import pygame as pg
import cv2
import numpy as np


class ArtConverter:
    def __init__(self, path='img/5.jpg', font_size=12, color_lvl=8):
        pg.init()
        self.path = path
        self.COLOR_LVL = color_lvl
        self.img, self.gray_img = self.get_img()
        self.RES = self.WIDTH, self.HEIGHT = self.img.shape[0], self.img.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.ASCII_CHARS = ' ixzao*#MW&8%B@$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def draw_conv_img(self):
        char_indic = self.gray_img // self.ASCII_COEFF
        color_indic = self.img // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indic[x, y]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indic[x, y])
                    self.surface.blit(self.PALETTE[char][color], (x, y))

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def get_img(self):
        self.cv2_img = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_img)
        img = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        gray_img = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2GRAY)
        return img, gray_img

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
