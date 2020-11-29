import math

import pygame
from pygame.color import Color

from Egg import Egg

class Player:
    def __init__(self, stats):
        self.stats = stats
        self.__x = 0
        self.__y = 0
        self.__xspd = 0
        self.__yspd = 0
        self.__accel = 5
        self.__speed = 10
        self.__left = False
        self.__right = False
        self.__up = False
        self.__down = False
        self.__cwise = False
        self.__ccwise = False
        self.__rotate = 0
        self.__size = 70
        self.__cx = self.__x + self.__size/2
        self.__cy = self.__y + self.__size/2
        self.__img = pygame.image.load('ufo.png')
        self.__eggs = []
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.__hp = 10
        self.__maxhp = 10
        self.ammo = 10
        self.maxammo = 10

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
        hpLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(str(self.__hp) + " / " + str(self.__maxhp), 1, (255, 255, 255))
        hpWord = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("HP:", 1, (255, 255, 255))
        pygame.draw.rect(screen, (min(255, int((self.__maxhp - self.__hp) * 255 / (self.__maxhp - 1))), max(0, int(255 - (self.__maxhp - self.__hp) * 255 / (self.__maxhp - 1))), 0), (screen.get_width()/2-450, 20, max(0, 200 / self.__maxhp * self.__hp), 20))
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


    def move(self):
        if self.__left:
            self.__xspd = max(self.__xspd - self.__accel, -self.__speed)
        if self.__right:
            self.__xspd = min(self.__xspd + self.__accel, self.__speed)
        if self.__up:
            self.__yspd = max(self.__yspd - self.__accel, -self.__speed)
        if self.__down:
            self.__yspd = min(self.__yspd + self.__accel, self.__speed)
        if self.__ccwise:
            self.__rotate += 20
        if self.__cwise:
            self.__rotate -= 20
        if not (self.__up or self.__down) and self.__yspd != 0:
            self.__yspd -= self.__yspd / abs(self.__yspd)
        if not (self.__left or self.__right) and self.__xspd != 0:
            self.__xspd -= self.__xspd / abs(self.__xspd)
        self.__x = max(min(self.__x + self.__xspd, 1200-self.__size), 0)
        self.__y = max(min(self.__y + self.__yspd, 650-self.__size), 0)
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.__cx = self.__x + self.__size / 2
        self.__cy = self.__y + self.__size / 2

    def takeDamage(self, dmg):
        self.__hp = max(0, self.__hp - dmg)

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
                    self.__eggs.append(Egg(self.__cx, self.__cy, self.__rotate, self))
                    self.ammo -= 1

        if mouse and event.type == pygame.MOUSEBUTTONDOWN and self.ammo > 0:
            self.__eggs.append(Egg(self.__cx-7, self.__cy-7, self.__rotate, self))
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



