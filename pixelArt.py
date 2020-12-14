import pygame as pg
import cv2
import numpy as np
import pygame.gfxdraw

class ArtConverter:
    def __init__(self, path='img/1.jpg', pixel_size=6, color_lvl=8):
        pg.init()
        self.path = path
        self.PIXEL_SIZE=pixel_size
        self.COLOR_LVL = color_lvl
        self.img = self.get_img()
        self.RES = self.WIDTH, self.HEIGHT = self.img.shape[0], self.img.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def draw_conv_img(self):
        color_indic = self.img // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color_key=tuple(color_indic[x,y])
                if sum(color_key):
                    color=self.PALETTE[color_key]
                    pygame.gfxdraw.box(self.surface,(x,y,self.PIXEL_SIZE,self.PIXEL_SIZE),color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_img(self):
        self.cv2_img = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_img)
        img = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        return img

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
