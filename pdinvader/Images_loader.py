import pygame
from pdinvader import Images


class ImgLoader:
    def __init__(self, width: int, height: int) -> None:
        self.Screen_Width = width
        self.Screen_Height = height
        self.__load()
        self.__loadFonts()

    def __load(self):
        # background image
        self.img1 = pygame.image.load(Images.GAMEBG)
        self.img1 = pygame.transform.scale(
            self.img1, (self.Screen_Width, self.Screen_Height))

        # spaceship images
        self.img2 = pygame.image.load(Images.SPACESHIP)
        self.img2 = pygame.transform.scale(self.img2, (90, 90))

        # bullet image
        self.bulletimg = pygame.image.load(Images.BULLET)
        self.bulletimg = pygame.transform.scale(self.bulletimg, (10, 30))

        # scoreboard image
        self.scoreimg = pygame.image.load(Images.SCOREBOARD)
        self.scoreimg = pygame.transform.scale(self.scoreimg, (100, 60))

        # life image
        self.lifeimages = []
        for a in range(3):
            self.lifeimages.append(pygame.image.load(
                f"pdinvader/Images/Life/life{a+1}.png"))
            self.lifeimages[a] = pygame.transform.scale(
                self.lifeimages[a], (100, 30))

        # enemy
        self.enemyimg = pygame.image.load(Images.ENEMY)
        self.enemyimg = pygame.transform.scale(self.enemyimg, (80, 80))

        # explosion image
        self.explosion = list()
        for i in range(3):
            img = pygame.image.load(f"pdinvader/Images/Explosion/exp{i+1}.png")
            self.explosion.append(pygame.transform.scale(img, (100, 100)))

        # winning background image
        self.winimg = pygame.image.load(Images.WINIMAGWE)
        self.winimg = pygame.transform.scale(
            self.winimg, (self.Screen_Width, self.Screen_Height))

        # gameover image
        self.goimg = pygame.image.load(Images.GAMEOVER)
        self.goimg = pygame.transform.scale(self.goimg, (300, 250))

        # missile image
        self.missileimg = pygame.image.load(Images.MISSILE)
        self.missileimg = pygame.transform.scale(self.missileimg, (30, 90))

        # shoot sound loader
        self.shootsound = pygame.mixer.Sound(Images.SHOOTSOUND)
        self.shootsound.set_volume(0.3)

        # explosion
        self.explodesound = pygame.mixer.Sound(Images.EXPLODESOUND)
        self.explodesound.set_volume(0.7)

    def __loadFonts(self):
        self.scorefont = pygame.font.Font(Images.SCOREFONT, 35)
        self.levelfont = pygame.font.Font(Images.LEVELFONT, 30)
        self.scoreshow = pygame.font.Font(Images.LEVELFONT, 50)
        self.winfont = pygame.font.Font(Images.WINNER, 80)
        self.infofont = pygame.font.Font(Images.INFOFONT, 30)
