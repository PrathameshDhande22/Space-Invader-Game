import pygame
from pdinvader import Images


class Missile:
    def __init__(self, x: int, y: int, display: pygame.Surface, img: pygame.Surface) -> None:
        self.xpos = x
        self.ypos = y
        self.display = display
        self.img = img
        self.velocity = 0.2
        self.bulletcount = 0
        self.mrect = pygame.Rect(self.xpos, self.ypos, 30, 50)

    def draw(self):
        self.mrect = pygame.Rect(self.xpos, self.ypos, 30, 50)
        self.display.blit(self.img, (self.xpos, self.ypos))

    def move(self):
        self.ypos += self.velocity

    def playercollide(self, playerrect: pygame.Rect):
        if self.mrect.colliderect(playerrect):
            return True
        else:
            return False

    def bulletcollide(self, bulletrect: pygame.Rect):
        if bulletrect.colliderect(self.mrect):
            self.bulletcount += 1
            return True
        else:
            return False

    @property
    def getcount(self):
        return self.bulletcount
