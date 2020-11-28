import math

import pygame


class Egg:
    def __init__(self, x, y, angle, parent):
        self.__x = x
        self.__y = y
        self.__angle = angle
        self.__rotate = 0
        self.__speed = 20
        self.__parent = parent
        self.__img = pygame.image.load('egg.png')

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.__x, new_rect[1] + self.__y)

    def draw(self, screen):
        tup = self.rot_center(self.__img, self.__rotate)
        screen.blit(tup[0], tup[1])

    def tick(self):
        self.__x += math.cos(math.radians(90+self.__angle)) * self.__speed
        self.__y -= math.sin(math.radians(90+self.__angle)) * self.__speed
        self.__rotate += 10
        if (self.__x < 0 or self.__y < 0 or self.__x - 15 > 1200 or self.__y - 15 > 650):
            self.__parent.getEggs().remove(self)
