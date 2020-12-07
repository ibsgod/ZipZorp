import random

import pygame

from goodstuff.Bacon import Bacon


class Enemy:
    def __init__(self, x, y, player):
        self.__x = x
        self.__y = y
        self.__speed = random.randint(1,4)
        self.__player = player
        self.__size = 70
        self.normimg = pygame.image.load('pig.png')
        self.hurtimg = pygame.image.load('pighurt.png')
        self.__img = self.normimg
        self.__hp = 13
        self.__maxhp = 13
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.hitEggs = []

    def draw(self, screen):
        maxbar = pygame.Surface((50, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.__x + (self.__size - maxbar.get_width()) / 2, self.__y - 15)), 1, (255, 255, 255)
        pygame.draw.rect(screen, (min(255, int((self.__maxhp - self.__hp) * 255 / (self.__maxhp - 1))), max(0, int(255 - (self.__maxhp - self.__hp) * 255 / (self.__maxhp - 1))), 0), (self.__x + (self.__size - maxbar.get_width()) / 2, self.__y - 15, max(0, maxbar.get_width() / self.__maxhp * self.__hp), 5))
        screen.blit(self.__img, (int(self.__x), int(self.__y)))

    def tick(self):
        if self.__x != self.__player.getX():
            self.__x += (self.__player.getX() - self.__x) / abs(self.__player.getX() - self.__x) * min(self.__speed, abs(self.__player.getX() - self.__x))
        if self.__y != self.__player.getY():
            self.__y += (self.__player.getY() - self.__y) / abs(self.__player.getY() - self.__y) * min(self.__speed, abs(self.__player.getY() - self.__y))
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        if self.coll.colliderect(self.__player.coll):
            self.__player.takeDamage(1)
            self.die()
            return
        hit = False
        for i in self.__player.getEggs()[:]:
            if self.coll.colliderect(i.coll):
                self.__img = self.hurtimg
                hit = True
                if not self.__player.items['eggpen']:
                    self.__player.getEggs().remove(i)
                if i not in self.hitEggs:
                    self.__hp -= self.__player.atk
                    if self.__player.items['vampeggs']:
                        self.__player.hp = min(self.__player.maxhp, self.__player.hp + self.__player.atk / 4)
                self.hitEggs.append(i)
                if self.__hp <= 0:
                    self.die()
                return
        if not hit:
            self.__img = self.normimg

    def die(self):
        self.__player.score += 1
        r = random.randint(1, 10)
        r1 = max(0, random.randint(0, 10) - 7)
        if r1 >= 1:
            self.__player.stats.food.append(Bacon(self.__player, self.__x, self.__y, r1))
        self.__player.gain(int(self.__x), int(self.__y), 0, r)
        self.__player.stats.enemies.remove(self)