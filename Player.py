import math

import pygame
from pygame.color import Color

from Egg import Egg

class Player:
    def __init__(self, stats, x=0, y=0):
        self.stats = stats
        self.__x = x
        self.__y = y
        self.__xspd = 0
        self.__yspd = 0
        self.__accel = 3
        self.speed = 9
        self.__left = False
        self.__right = False
        self.__up = False
        self.__down = False
        self.__cwise = False
        self.__ccwise = False
        self.__cspd = 0
        self.__rotate = 0
        self.__size = 70
        self.__cx = self.__x + self.__size/2
        self.__cy = self.__y + self.__size/2
        self.__img = pygame.image.load('ufo.png')
        self.__eggs = []
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.hp = 10
        self.maxhp = 10
        self.ammo = 10
        self.maxammo = 10
        self.score = 0
        self.exp = 0
        self.level = 1
        self.gaintext = []
        self.gold = 50
        self.pts = 1
        self.atk = 1
        self.regen = 5
        self.reload = 1
        self.items = {}
        self.items["vampeggs"] = False
        self.items["eggpen"] = False
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getEggs(self):
        return self.__eggs

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.__x, new_rect[1] + self.__y)

    def draw(self, screen):
        tup = self.rot_center(self.__img, self.__rotate)
        screen.blit(tup[0], tup[1])
        maxhpbar = pygame.Surface((200, 20))
        maxhpbar.set_alpha(80)
        maxhpbar.fill((0, 0, 0))
        screen.blit(maxhpbar, (screen.get_width()/2 - 450, 20))
        hpLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(str(self.hp) + " / " + str(self.maxhp), 1, (255, 255, 255))
        hpWord = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("HP:", 1, (255, 255, 255))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp - 1))), max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp - 1))), 0), (screen.get_width()/2-450, 20, max(0, 200 / self.maxhp * self.hp), 20))
        screen.blit(hpLbl, ((screen.get_width() - hpLbl.get_width()) / 2 -350, 24))
        screen.blit(hpWord, (screen.get_width() / 2 - 450 - hpWord.get_width() - 10, 20))

        maxammobar = pygame.Surface((200, 20))
        maxammobar.set_alpha(80)
        maxammobar.fill((0, 0, 0))
        screen.blit(maxammobar, (screen.get_width() / 2 - 100, 20))
        ammoLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(str(self.ammo) + " \ " + str(self.maxammo),
                                                                           1, (0, 0, 0))
        ammoWord = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Ammo:", 1, (255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255),
                         (screen.get_width() / 2 - 100, 20, max(0, int(200 / self.maxammo * self.ammo)), 20))
        screen.blit(ammoLbl, (screen.get_width() / 2 - 100 + maxammobar.get_width() / 2 - ammoLbl.get_width() / 2, 24))
        screen.blit(ammoWord, (screen.get_width() / 2 - 100 - ammoWord.get_width() - 10, 20))

        maxexpbar = pygame.Surface((200, 20))
        maxexpbar.set_alpha(80)
        maxexpbar.fill((0, 0, 0))
        screen.blit(maxexpbar, (screen.get_width() / 2 + 250, 20))
        expLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(str(self.exp) + " \ 50",
                                                                             1, (0, 0, 0))
        expWord = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Level " + str(self.level), 1, (255, 255, 255))
        pygame.draw.rect(screen, (0, 255, 255),
                         (screen.get_width() / 2 + 250, 20, min(max(0, int(200 / 50 * self.exp)), 200), 20))
        screen.blit(expLbl, (screen.get_width() / 2 + 250 + maxexpbar.get_width() / 2 - expLbl.get_width() / 2, 24))
        screen.blit(expWord, (screen.get_width() / 2 + 250 - expWord.get_width() - 10, 20))


    def move(self):
        self.__accel = round(self.speed * 10 / 3) / 10
        if self.__left:
            self.__xspd = max(self.__xspd - self.__accel, -self.speed)
        if self.__right:
            self.__xspd = min(self.__xspd + self.__accel, self.speed)
        if self.__up:
            self.__yspd = max(self.__yspd - self.__accel, -self.speed)
        if self.__down:
            self.__yspd = min(self.__yspd + self.__accel, self.speed)
        if self.__ccwise:
            self.__cspd = max(4, min(self.__cspd + 4, 20))
        if self.__cwise:
            self.__cspd = min(-4, max(self.__cspd - 4, -20))
        if not (self.__up or self.__down) and self.__yspd != 0:
            self.__yspd -= self.__yspd / abs(self.__yspd)
        if not (self.__left or self.__right) and self.__xspd != 0:
            self.__xspd -= self.__xspd / abs(self.__xspd)
        if not (self.__cwise or self.__ccwise):
            self.__cspd = 0
        self.__x = max(min(self.__x + self.__xspd, 1200-self.__size), 0)
        self.__y = max(min(self.__y + self.__yspd, 650-self.__size), 0)
        self.__rotate += self.__cspd
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.__cx = self.__x + self.__size / 2
        self.__cy = self.__y + self.__size / 2

    def takeDamage(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def register(self, event, mouse):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_a:
                self.__left = True
            elif key == pygame.K_d:
                self.__right = True
            if key == pygame.K_w:
                self.__up = True
            elif key == pygame.K_s:
                self.__down = True
            if not mouse:
                if key == pygame.K_LEFT:
                    self.__ccwise = True
                if key == pygame.K_RIGHT:
                    self.__cwise = True
                if key == pygame.K_SPACE and self.ammo > 0:
                    self.__eggs.append(Egg(self.__cx, self.__cy, self.__rotate, self, vamp=self.items["vampeggs"]))
                    self.ammo -= 1

        if mouse and event.type == pygame.MOUSEBUTTONDOWN and self.ammo > 0:
            self.__eggs.append(Egg(self.__cx-7, self.__cy-7, self.__rotate, self, vamp=self.items["vampeggs"]))
            self.ammo -= 1

        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_a:
                self.__left = False
            elif key == pygame.K_d:
                self.__right = False
            if key == pygame.K_w:
                self.__up = False
            elif key == pygame.K_s:
                self.__down = False
            if key == pygame.K_LEFT:
                self.__ccwise = False
            if key == pygame.K_RIGHT:
                self.__cwise = False

    def accelerate(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_a:
                self.__left = True
            elif key == pygame.K_d:
                self.__right = True
            if key == pygame.K_w:
                self.__up = True
            elif key == pygame.K_s:
                self.__down = True
        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_a:
                self.__left = False
            elif key == pygame.K_d:
                self.__right = False
            if key == pygame.K_w:
                self.__up = False
            elif key == pygame.K_s:
                self.__down = False

    def mouseSpin(self, mousePos):
        mx = mousePos[0]
        my = mousePos[1]
        if mx-self.__cx != 0:
            self.__rotate = -90 - math.degrees(math.atan((my-self.__cy) / (mx-self.__cx)))
            if mx < self.__cx:
                self.__rotate += 180

    def gain(self, x, y, gold, exp):
        if x is None:
            x = self.__x
            y = self.__y
        self.gold += gold
        self.exp += exp
        if exp > 0:
            expLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render("+" + str(exp) + " exp", 1, (255, 255, 255))
            self.gaintext.append([expLbl, int(x), int(y), 30])
        if gold > 0:
            goldLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render("+" + str(gold) + " gold", 1, (220, 220, 0))
            self.gaintext.append([goldLbl, int(x), int(y-20), 30])
        if self.exp >= 50:
            self.level += 1
            self.exp -= 50
            self.pts += 1



