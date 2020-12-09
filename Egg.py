import math

import pygame

class Egg:
    def __init__(self, x, y, angle, player, vamp=False, split=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.__rotate = 0
        self.__speed = 20
        self.__size = 15
        self.__player = player
        self.__img = pygame.image.load('egg.png')
        self.vamp = vamp
        self.split = split
        if vamp:
            self.__img = pygame.image.load('vampegg.png')
        self.coll = pygame.Rect(self.x, self.y, self.__size, self.__size)

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self, screen):
        tup = self.rot_center(self.__img, self.__rotate)
        screen.blit(tup[0], tup[1])

    def tick(self):
        self.x += math.cos(math.radians(90+self.angle)) * self.__speed
        self.y -= math.sin(math.radians(90+self.angle)) * self.__speed
        self.__rotate += 10
        self.coll = pygame.Rect(self.x, self.y, self.__size, self.__size)
        if self.x < 0 or self.y < 0 or self.x - 15 > 1200 or self.y - 15 > 650:
            self.__player.getEggs().remove(self)

