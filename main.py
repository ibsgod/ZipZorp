import sys

from pygame.rect import Rect

from Player import Player
import os
import pygame

class Main:
    pygame.mixer.init()
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    width = 1200
    height = 650
    screen = pygame.display.set_mode((width, height))
    screen.fill((244, 0, 0))
    p = Player()
    pause = False
    mouseOver = False
    mouse = False
    mousePos = None
    contRect = None
    while True:
        screen.fill((0, 0, 0))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if mouseOver and event.type == pygame.MOUSEBUTTONDOWN:
                mouse = not mouse
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = not pause
                break
            p.register(event, mouse)
        if not pause:
            p.move()
            for i in p.getEggs():
                i.tick()
            if mouse:
                p.mouseSpin(mousePos)
        for i in p.getEggs():
            i.draw(screen)
        p.draw(screen)
        if pause:
            contRect = Rect(int(width / 2) + 15, int(height / 2) - 40, 250, 50)
            if contRect.collidepoint(mousePos):
                mouseOver = True
            else:
                mouseOver = False
            pygame.draw.rect(screen, (200, 200, 200), (int(width/2)-300, int(height/2)-162, 600, 325))
            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 80)
            pauseLbl = myFont.render("Paused", 1, (255, 0, 0))
            screen.blit(pauseLbl, (int(width/2)-100, int(height/3), 200, 200))
            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 40)
            spinLbl = myFont.render("Shooting control: ", 1, (255, 0, 0))
            screen.blit(spinLbl, (int(width/2)-245, int(height/2)-30, 200, 200))
            pygame.draw.rect(screen, (200, 20+mouseOver*100, 20+mouseOver*100), contRect)
            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 35)
            mouseLbl = myFont.render("Mouse & Click" if mouse else "Arrows & Spacebar", 1, (255, 255, 255))
            screen.blit(mouseLbl, (int(width/2)+25+30*mouse, int(height/2)-28, 150, 50))
        else:
            mouseOver = False
        pygame.display.update()
        pygame.time.Clock().tick(30)

