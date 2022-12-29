import sys
import pygame
from pdinvader import Images
from .Entry import EntryScreen
from .Images_loader import ImgLoader
import math
from .Bullet import Bullet
from .Enemy import Enemy
import random
from .ExplosionEffect import Explosion
import numpy
from .Missile import Missile


class Game():

    def __init__(self) -> None:
        self.game = pygame.init()
        self.Screen_Height = 700
        self.Screen_Width = 700
        self.display = pygame.display.set_mode(
            (self.Screen_Width, self.Screen_Height))
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load(Images.ICON)
        pygame.display.set_icon(icon)
        self.gameover = False
        self.gamestart = True
        self.imgs = ImgLoader(self.Screen_Width, self.Screen_Height)
        self.Player_x = math.floor(self.Screen_Width/2)-50
        self.Player_y = self.Screen_Height-110
        self.velocity = 0.9
        self.clck = pygame.time.Clock()
        self.fps = 1000
        self.life = 0
        self.repeat = False
        self.checking = 0
        self.tobeexploded = False
        self.level = 1
        self.bulletlist = []
        self.enemylist = list()
        self.score = 0
        self.enemyshow = 0
        self.explode = Explosion(self.Player_x, self.Player_y, self.display)
        self.enemyexplosion = Explosion(None, None, self.display)
        self.lastenemyxpos = 0
        self.lastenemyypos = 0

        self.gameoverscreen = False
        self.enemytobeexploded = False
        self.overscreen = False
        self.gamewinscreen = True
        self.missileshow = False
        self.enemy = 0
        self.counter = 0
        self.missile = Missile(0, 0, self.display, self.imgs.missileimg)
        pygame.mixer.init()
        pygame.mixer.music.load(Images.MAINSOUND)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
        self.startcreen()

    def startcreen(self):
        while self.gamestart:
            em = EntryScreen(self.display, self.Screen_Height,
                             self.Screen_Width)
            em.hover()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        ms = pygame.mouse.get_pos()
                        if 280 <= ms[0] and ms[0] <= 280+150 and 430 <= ms[1] and ms[1] <= 430+150:
                            self.gamestart = False
                            self.gamescreen()
            pygame.display.update()

    def gamescreen(self):
        while not self.gameover:
            if self.overscreen:
                self.gameoverScreen()
            else:
                self.levels()
                self.settinggameover()

                self.clck.tick(self.fps)
                pygame.mouse.set_visible(False)
                self.screenplace(self.imgs.img1, 0, 0)
                self.playerrect = pygame.Rect(
                    self.Player_x+10, self.Player_y+10, 80, 80)
                self.screenplace(self.imgs.img2, self.Player_x, self.Player_y)
                self.screenplace(self.imgs.scoreimg, 8, 2)
                self.scoretext = self.imgs.scorefont.render(
                    str(self.score), True, (255, 255, 255))
                self.screenplace(self.scoretext, 40, 5)
                self.screenplace(self.imgs.lifeimages[self.life], 590, 10)
                self.levelupfont = self.imgs.levelfont.render(
                    f"Level : {str(self.level)}", True, (255, 255, 255))
                self.screenplace(self.levelupfont, 300, 10)
                if self.missileshow:
                    self.counter = self.backup+1
                else:
                    self.counter += 1
                    self.backup = self.counter
                if self.counter % 20 == 0 and self.level >= 2:
                    self.missile = Missile(random.randint(
                        0, self.Screen_Width-30), 0, self.display, self.imgs.missileimg)
                    self.missileshow = True
                elif self.missileshow:
                    self.showmissile()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bulletx = self.Player_x+46
                            self.bullety = self.Player_y-10
                            if self.tobeexploded == False:
                                self.imgs.shootsound.play(0)
                                self.bullet = Bullet(
                                    self.imgs.bulletimg, self.display, self.bulletx-5, self.bullety)
                                self.bulletlist.append(self.bullet)
                self.showenemies()
                self.firebullets()
                self.keys = pygame.key.get_pressed()
                if self.keys[pygame.K_LEFT] or self.keys[pygame.K_KP4]:
                    self.Player_x -= self.velocity
                elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_KP6]:
                    self.Player_x += self.velocity
                self.showexplosion(self.playerrect.x, self.playerrect.y)
                self.showenemyexplode(self.lastenemyxpos, self.lastenemyypos)
                self.setBoundaries()
                pygame.display.update()

    def winscreen(self):
        pygame.mixer.music.load(Images.VICTORYSOUND)
        pygame.mixer.music.play(-1)
        while self.gamewinscreen:
            self.screenplace(self.imgs.winimg, 0, 0)
            self.screenplace(self.imgs.winfont.render(
                "YOU WIN !", True, (255, 255, 255)), 150, 80)
            self.screenplace(self.imgs.scoreshow.render(
                f"Score : {self.score}", True, (241, 255, 0)), 250, 180)
            self.screenplace(self.imgs.infofont.render(
                "Press 1 For Main Menu", True, (0, 255, 55)), 150, 400)
            self.screenplace(self.imgs.infofont.render(
                "Press 2 To Quit", True, (0, 255, 55)), 150, 460)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        pygame.mouse.set_visible(True)
                        Game()
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self.gamewinscreen = False
                        pygame.quit()
                        sys.exit(0)
            pygame.display.update()

    def playoversound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(Images.OVERSOUND)
        pygame.mixer.music.play(0)

    def gameoverScreen(self):
        self.screenplace(self.imgs.goimg, 200, 30)
        self.screenplace(self.imgs.scoreshow.render(
            f"Score : {self.score}", True, (255, 0, 228), (0, 0, 0)), 260, 300)
        self.screenplace(self.imgs.infofont.render(
            "Press 1 For Main Menu", True, (255, 184, 38)), 180, 370)
        self.screenplace(self.imgs.infofont.render(
            "Press 2 To Quit", True, (255, 184, 38)), 180, 420)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    pygame.mouse.set_visible(True)
                    self.overscreen = False
                    Game()
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    pygame.quit()
                    sys.exit(0)
        pygame.display.update()

    def levels(self):
        if self.level == 1:
            self.enemy = 8
        elif self.level == 2:
            self.enemy = 10
        elif self.level == 3:
            self.enemy = 12
        elif self.level == 4:
            if len(self.enemylist) == 0:
                self.gameover = True
                self.winscreen()

    def firebullets(self):
        try:
            for i in range(len(self.bulletlist)):
                self.bulletlist[i].draw()
                self.bulletlist[i].move()
                if self.bulletlist[i].getyPosition() <= 0:
                    self.bulletlist.pop(i)

        except IndexError:
            pass

    def showenemies(self):
        if self.enemyshow < self.enemy:
            if self.enemyshow == 0:
                self.enemySurface = Enemy(self.imgs.enemyimg, random.randint(
                    0, self.Screen_Width-80), 0, self.display)
                self.enemylist.append(self.enemySurface)
                self.enemyshow += 1
            try:
                if self.enemylist[self.checking].y >= self.Screen_Height//2:
                    self.enemyshow += 1
                    self.repeat = True
                    self.checking += self.enemyshow
            except IndexError:
                self.enemyshow += 1
                self.repeat = True
                self.checking += self.enemyshow
            if self.repeat:
                self.numpyx = numpy.linspace(
                    0, self.Screen_Width-80, num=self.enemyshow, dtype=int)
                for i in range(self.enemyshow):
                    self.enemyposx = random.randint(0, self.Screen_Width-80)
                    self.enemySurface = Enemy(
                        self.imgs.enemyimg, self.numpyx[i], 0, self.display)
                    self.enemylist.append(self.enemySurface)
                self.repeat = False
        else:
            self.level += 1
            if self.level > 4:
                self.level = 4

        for i in range(len(self.enemylist)):
            self.enemylist[i].draw()
            self.enemylist[i].move()

        for index, enemy in enumerate(self.enemylist):
            if enemy.playercollide(self.playerrect):
                self.imgs.explodesound.play(0)
                self.tobeexploded = True
                self.enemylist.remove(enemy)
                self.checking -= 1
            elif enemy.screenCollide(self.Screen_Height):
                self.playoversound()
                self.overscreen = True
            self.shootingtheenemy(enemy.getRect(), index)

    def shootingtheenemy(self, rect, index):
        for bullets in self.bulletlist:
            if bullets.enemycollide(rect):
                self.imgs.explodesound.play(0)
                self.bulletlist.remove(bullets)
                self.checking -= 1
                self.enemylist.pop(index)
                self.score += 10
                self.lastenemyxpos = rect.x
                self.lastenemyypos = rect.y
                self.enemytobeexploded = True
            if self.missile.bulletcollide(bullets.bulletrect):
                self.bulletlist.remove(bullets)
                self.lastenemyxpos = self.missile.mrect.x
                self.lastenemyypos = self.missile.mrect.y
                self.enemytobeexploded = True
                if self.missile.getcount >= 3:
                    self.enemytobeexploded = True
                    self.lastenemyxpos = self.missile.mrect.x
                    self.lastenemyypos = self.missile.mrect.y
                    self.imgs.explodesound.play(0)
                    self.score += 50
                    self.missileshow = False

    def showmissile(self):
        if self.missile.ypos >= self.Screen_Height-50:
            self.missileshow = False
        else:
            self.missile.draw()
            self.missile.move()
            if self.missile.playercollide(self.playerrect):
                self.missileshow = False
                self.imgs.explodesound.play(0)
                self.settinggameover()
                self.tobeexploded = True
                self.showexplosion(self.Player_x, self.Player_y)

    def showenemyexplode(self, x, y):
        if self.enemytobeexploded:
            self.enemyexplosion.update(x, y)
            if self.enemyexplosion.index >= 2.7:
                self.enemytobeexploded = False

    def showexplosion(self, x, y):
        if self.tobeexploded:
            self.explode.update(x, y)
            if self.explode.getindex() > 2.7:
                self.tobeexploded = False
                if self.life+1 == 3:
                    self.playoversound()
                    self.overscreen = True
                else:
                    self.life += 1

    def setBoundaries(self):
        if self.Player_x <= 0:
            self.Player_x = 0
        elif self.Player_x >= self.Screen_Width-90:
            self.Player_x = self.Screen_Width-90

    def settinggameover(self):
        if self.life >= 3:
            self.playoversound()
            self.overscreen = True

    def screenplace(self, images: pygame.Surface, x: int, y: int):
        self.display.blit(images, (x, y))


if __name__ == '__main__':
    g = Game()
