import random

import pygame


class Enemy:
    def __init__(self, x, y, player):
        self.__x = x
        self.__y = y
        self.__speed = random.randint(1,4)
        self.__player = player
        self.__size = 70
        self.__img = pygame.image.load('pig.png')
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)

    def draw(self, screen):
        screen.blit(self.__img, (int(self.__x), int(self.__y)))

    def tick(self):
        if self.__x != self.__player.getX():
            self.__x += (self.__player.getX() - self.__x) / abs(self.__player.getX() - self.__x) * min(self.__speed, abs(self.__player.getX() - self.__x))
        if self.__y != self.__player.getY():
            self.__y += (self.__player.getY() - self.__y) / abs(self.__player.getY() - self.__y) * min(self.__speed, abs(self.__player.getY() - self.__y))
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        if self.coll.colliderect(self.__player.coll):
            self.__player.stats.enemies.remove(self)
            return
        for i in self.__player.getEggs()[:]:
            if self.coll.colliderect(i.coll):
                self.__player.getEggs().remove(i)
                self.__player.stats.enemies.remove(self)
                return