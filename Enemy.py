import random

import pygame

from Bacon import Bacon
from Egg import Egg


class Enemy:
    def __init__(self, x, y, player):
        self.__x = x
        self.__y = y
        self.__speed = random.randint(1,4)
        self.__player = player
        self.__size = 70
        self.__cx = self.__x + self.__size/2
        self.__cy = self.__y + self.__size/2
        self.normimg = pygame.image.load('pig.png')
        self.hurtimg = pygame.image.load('pighurt.png')
        self.__img = self.normimg
        self.__hp = 13
        self.__maxhp = 13
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)
        self.hitEggs = []
        self.hitShields = False

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
        self.__cx = self.__x + self.__size / 2
        self.__cy = self.__y + self.__size / 2
        if self.coll.colliderect(self.__player.coll):
            self.__player.takeDamage(1)
            self.die()
            return
        hit = False
        for i in self.__player.getEggs()[:]:
            if self.coll.colliderect(i.coll):
                self.__img = self.hurtimg
                hit = True
                if i not in self.hitEggs[:]:
                    self.__hp -= self.__player.atk
                    if self.__player.items['vampeggs']:
                        self.__player.hp = min(self.__player.maxhp, self.__player.hp + self.__player.atk / 4)
                    if self.__player.items["eggsplit"] and not i.split:
                        e1 = Egg(self.__cx-7, self.__cy-7, i.angle + 45, self.__player, vamp=self.__player.items["vampeggs"], split=True)
                        e2 = Egg(self.__cx-7, self.__cy-7, i.angle + 135, self.__player, vamp=self.__player.items["vampeggs"], split=True)
                        e3 = Egg(self.__cx-7, self.__cy-7, i.angle - 45, self.__player, vamp=self.__player.items["vampeggs"], split=True)
                        e4 = Egg(self.__cx-7, self.__cy-7, i.angle - 135, self.__player, vamp=self.__player.items["vampeggs"], split=True)
                        self.__player.addEggs(e1)
                        self.hitEggs.append(e1)
                        self.__player.addEggs(e2)
                        self.hitEggs.append(e2)
                        self.__player.addEggs(e3)
                        self.hitEggs.append(e3)
                        self.__player.addEggs(e4)
                        self.hitEggs.append(e4)
                if not self.__player.items['eggpen'] and (not i.split or i not in self.hitEggs[:]):
                    self.__player.getEggs().remove(i)
                self.hitEggs.append(i)
                if self.__hp <= 0:
                    self.die()
                return
            for i in self.hitEggs[:]:
                if i not in self.__player.getEggs():
                    self.hitEggs.remove(i)
        yes = False
        for i in self.__player.shieldEggs:
            if self.coll.colliderect(i.coll):
                self.__img = self.hurtimg
                if not self.hitShields:
                    self.__hp -= self.__player.atk * 3
                self.hitShields = True
                yes = True
        if not yes:
            self.hitShields = False
        else:
            hit = True
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