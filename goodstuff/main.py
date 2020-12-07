import random
import sys

from pygame.rect import Rect

from goodstuff.Button import Button
from goodstuff.Enemy import Enemy
from goodstuff.Player import Player
import os
import pygame

from goodstuff.Stats import Stats


pygame.mixer.init()
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1200
height = 650
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 50))
stats = Stats()
p = Player(stats, x = width/2, y = height/2)
click = False
mouse = False
mousePos = None
buttDict = {}
enemySpawnTimer = pygame.time.get_ticks()
enemySpawnSpeed = 1000
reloadTimer = pygame.time.get_ticks()
regenTimer = pygame.time.get_ticks()
def play():
    global mouse
    global mousePos
    global enemySpawnTimer
    global reloadTimer
    global regenTimer
    while True:
        screen.fill((200, 30, 150))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause()
                break
            p.register(event, mouse)
        p.move()
        for i in p.getEggs():
            i.tick()
        for i in stats.enemies:
            i.tick()
        for i in stats.food:
            i.tick()
        if mouse:
            p.mouseSpin(mousePos)
        if pygame.time.get_ticks() - reloadTimer > p.reload * 1000 and p.ammo < p.maxammo:
            p.ammo += 1
            reloadTimer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - regenTimer > p.regen * 1000:
            p.hp = min(p.hp + 1, p.maxhp)
            regenTimer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - enemySpawnTimer > enemySpawnSpeed:
            r = random.randint(0, 3)
            rx = None
            ry = None
            if r == 0:
                rx = -70
                ry = random.randint(0, 650)
            if r == 1:
                rx = random.randint(0, 1200)
                ry = -70
            if r == 2:
                rx = 1270
                ry = random.randint(0, 650)
            if r == 3:
                rx = random.randint(0, 1200)
                ry = 720
            stats.enemies.append(Enemy(rx, ry, p))
            enemySpawnTimer = pygame.time.get_ticks()
        for i in p.getEggs():
            i.draw(screen)
        for i in stats.enemies:
            i.draw(screen)
        for i in stats.food:
            i.draw(screen)
        p.draw(screen)
        for i in p.gaintext[:]:
            surf = pygame.Surface(i[0].get_size()).convert_alpha()
            surf.fill((255, 255, 255, 245))
            i[0].blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(i[0], (i[1], i[2]))
            i[3] -= 1
            i[2] -= 1
            if i[3] <= 0:
                p.gaintext.remove(i)
        pygame.display.update()
        pygame.time.Clock().tick(30)

def pause():
    global mouse
    global click
    global buttDict
    global mousePos
    buttDict.clear()
    buttDict["control"] = Button(int(width / 2) + 15, int(height / 2) - 40, 250, 50, screen, label=pygame.font.SysFont("Microsoft Yahei UI Light", 35).render("Mouse & Click" if mouse else "Arrows & Spacebar", 1, (255, 255, 255)))
    buttDict["stats"] = Button(int(width / 2) - 125, int(height / 2) + 40 , 250, 50, screen, label=pygame.font.SysFont("Microsoft Yahei UI Light", 35).render("Stats ", 1, (255, 255, 255)))
    while True:
        screen.fill((200, 30, 150))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            click = False
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return
        for i in p.getEggs():
            i.draw(screen)
        for i in stats.enemies:
            i.draw(screen)
        for i in stats.food:
            i.draw(screen)
        p.draw(screen)
        pygame.draw.rect(screen, (200, 200, 200), (int(width / 2) - 300, int(height / 2) - 162, 600, 325))
        myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 80)
        pauseLbl = myFont.render("Paused", 1, (255, 0, 0))
        screen.blit(pauseLbl, (int(width / 2) - 100, int(height / 3)))
        myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 40)
        spinLbl = myFont.render("Shooting control: ", 1, (255, 0, 0))
        screen.blit(spinLbl, (int(width / 2) - 245, int(height / 2) - 30))
        for i in buttDict:
            val = buttDict[i].tick(mousePos, click)
            if i == "control" and val:
                mouse = not mouse
                buttDict["control"].changeLabel(pygame.font.SysFont("Microsoft Yahei UI Light", 35).render("Mouse & Click" if mouse else "Arrows & Spacebar", 1, (255, 255, 255)))
                click = False
            if i == "stats" and val:
                stats.statMenu(screen, p)
                click = False
        pygame.display.update()
        pygame.time.Clock().tick(30)
    p.register(event, mouse)


play()
