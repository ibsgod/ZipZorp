import pygame


class Bacon:
    def __init__(self, player, x, y, gold):
        self.__x = x
        self.__y = y
        self.__gold = gold
        self.__player = player
        self.__size = 70
        self.__img = pygame.image.load('BACON.png')
        self.coll = pygame.Rect(self.__x, self.__y, self.__size, self.__size)

    def draw(self, screen):
        screen.blit(self.__img, (int(self.__x), int(self.__y)))

    def tick(self):
        if self.coll.colliderect(self.__player.coll):
            self.__player.gain(self.__x, self.__y, self.__gold, 0)
            self.__player.stats.food.remove(self)
