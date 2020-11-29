import pygame


class Button:
    def __init__(self, x, y, width, height, screen, color=(255, 0, 0), label=None):
        self.coll = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__screen = screen
        self.__label = label

    def tick(self, mousePos, click):
        if self.coll.collidepoint(mousePos[0], mousePos[1]):
            pygame.draw.rect(self.__screen, (min(255, self.__color[0]+50), min(255, self.__color[1]+50), min(255, self.__color[2]+50)), self.coll)
            self.__screen.blit(self.__label, (self.coll.x + (self.coll.width - self.__label.get_width()) / 2, self.coll.y + (self.coll.height - self.__label.get_height()) / 2))
            if click:
                return True
        else:
            pygame.draw.rect(self.__screen, self.__color, self.coll)
            self.__screen.blit(self.__label, (self.coll.x + (self.coll.width - self.__label.get_width()) / 2, self.coll.y + (self.coll.height - self.__label.get_height()) / 2))
        return False

    def changeLabel(self, label):
        self.__label = label

