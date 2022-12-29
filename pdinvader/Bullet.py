import pygame

class Bullet:
    def __init__(self,img:pygame.Surface,display:pygame.Surface,x,y) -> None:
        self.img=img
        self.xpos=x
        self.ypos=y
        self.display=display
        self.volocity=-0.7
        self.bulletrect=pygame.Rect(self.xpos,self.ypos,10,30)
    
    def move(self):
        self.ypos=self.ypos+self.volocity
        
    def draw(self):
        self.bulletrect=pygame.Rect(self.xpos,self.ypos,10,30)
        # print(self.bulletrect)
        self.display.blit(self.img,(self.xpos,self.ypos))
        
    def getyPosition(self):
        return self.ypos
    
    def enemycollide(self,enerect:pygame.Rect):
        if self.bulletrect.colliderect(enerect):
            return True