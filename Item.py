import pygame


class Item:
    def __init__(self, x, y, width, height, screen, bought, price, color=(0, 0, 205), img=None, label=None, description=None):
        self.coll = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__screen = screen
        self.__label = label
        self.img = pygame.image.load(img)
        self.description = description
        self.price = price
        self.bought = bought
        self.pricestr = ""
    def tick(self, mousePos, click):
        if self.bought:
            self.priceLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("Bought", 1, (200, 0, 0))
        else:
            self.priceLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render(str(self.price) + "g", 1, (200, 200, 0))
        if self.coll.collidepoint(mousePos[0], mousePos[1]):
            pygame.draw.rect(self.__screen, (min(255, self.__color[0]+30), min(255, self.__color[1]+30), min(255, self.__color[2]+30)), self.coll)
            self.__screen.blit(self.__label, (self.coll.x + (self.coll.width - self.__label.get_width()) / 2, self.coll.y + self.coll.height/3 - self.__label.get_height()/2))
            self.__screen.blit(self.priceLbl, (self.coll.x + (self.coll.width - self.priceLbl.get_width()) / 2, self.coll.y + 2*self.coll.height/3 - self.priceLbl.get_height()/2))
            if self.bought:
                pygame.draw.rect(self.__screen, (150, 150, 150), self.coll)
                self.__screen.blit(self.__label, (self.coll.x + (self.coll.width - self.__label.get_width()) / 2, self.coll.y + self.coll.height / 3 - self.__label.get_height() / 2))
                self.__screen.blit(self.priceLbl, (self.coll.x + (self.coll.width - self.priceLbl.get_width()) / 2,self.coll.y + 2 * self.coll.height / 3 - self.priceLbl.get_height() / 2))
            if click:
                return 2
            else:
                return 1
        else:
            pygame.draw.rect(self.__screen, self.__color, self.coll)
            self.__screen.blit(self.img, (self.coll.x + 15, self.coll.y + 25))
        return 0

    def changeLabel(self, label):
        self.__label = label

