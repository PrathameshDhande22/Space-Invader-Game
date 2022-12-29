import pygame
from .Images import *

class EntryScreen():
    
    def __init__(self,display:pygame.Surface,height,width) -> None:
        self.display=display
        self.height=height
        self.width=width
        self.__showscreen()
    
    def __showscreen(self):
        self.img1=pygame.image.load(INTROPNG)
        self.img1=pygame.transform.scale(self.img1,(self.width,self.height))
        self.display.blit(self.img1,(0,0))
        self.img2=pygame.image.load(PLAYBTN)
        self.img2=pygame.transform.scale(self.img2,(150,150))
        self.display.blit(self.img2,(280,430))
        
        
    def hover(self):
        self.img3=pygame.image.load(PLAYBTNDARK)
        self.img3=pygame.transform.scale(self.img3,(150,150))
        
        ms=pygame.mouse.get_pos()
        if 280 <= ms[0] and ms[0] <= 280+150 and 430 <= ms[1] and ms[1] <= 430+150:
            self.display.blit(self.img3,(280,430))