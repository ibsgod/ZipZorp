import pygame

class ShieldEgg:
    def __init__(self, x, y, radius, dire, player):
        self.x = int(x)
        self.y = int(y)
        self.size = 15
        self.player = player
        self.cx = self.x + self.size/2
        self.cy = self.y + self.size/2
        self.img = pygame.image.load('shieldegg.png')
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        self.dire = dire
        self.radius = radius
        self.xdis = 0

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def tick(self):
        self.x = self.player.cx + self.xdis - 7
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        if self.cx + self.dire*10 >= self.player.cx + self.radius:
            self.dire = -1
        if self.cx + self.dire*10 <= self.player.cx - self.radius:
            self.dire = 1
        self.xdis += self.dire*10
        self.y = self.player.cy + abs(self.radius ** 2 - (self.cx - self.player.cx)  ** 2) ** 0.5 * self.dire
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)





