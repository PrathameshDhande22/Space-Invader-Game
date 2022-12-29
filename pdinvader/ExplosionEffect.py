import pygame
from .Images_loader import ImgLoader


class Explosion:
    def __init__(self, x: int, y: int, display: pygame.Surface) -> None:
        self.display = display
        self.xpos = x
        self.ypos = y
        self.index = 0
        self.imgs = ImgLoader(0, 0)
        self.explosion = self.imgs.explosion

    def update(self, xpos, ypos):
        try:
            if self.index > 2.7:
                self.index = 0
            self.index += 0.01
            # print(self.index)
            self.display.blit(self.explosion[int(self.index)], (xpos, ypos))
        except IndexError:
            self.index = 0

    def getindex(self):
        return self.index
