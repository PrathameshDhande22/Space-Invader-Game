import pygame


class Enemy:
    def __init__(self, image: pygame.Surface, x, y, display: pygame.Surface) -> None:
        self.img = image
        self.display = display
        self.x = x
        self.y = y
        self.velocity = 0.25

    def draw(self):
        self.enemyrect = pygame.Rect(self.x+10, self.y+10, 60, 60)
        self.display.blit(self.img, (self.x, self.y))

    def getRect(self) -> pygame.Rect:
        return self.enemyrect

    def move(self):
        self.y += self.velocity

    def screenCollide(self, height):
        if self.y >= height-80:
            return True
        else:
            return False

    def playercollide(self, prect: pygame.Rect):
        if prect.colliderect(self.enemyrect):
            return True
        else:
            return False
