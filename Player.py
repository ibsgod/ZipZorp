import math

import pygame

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

    def tick(self):
        for i in self.stats.enemies:
            if self.coll.colliderect(i.coll):
                print("ouch")

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
                if key == pygame.K_SPACE:
                    self.__eggs.append(Egg(self.__cx, self.__cy, self.__rotate, self))
        if mouse and event.type == pygame.MOUSEBUTTONDOWN:
            self.__eggs.append(Egg(self.__cx-7, self.__cy-7, self.__rotate, self))

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



