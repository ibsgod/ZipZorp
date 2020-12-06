import sys

import pygame

from Button import Button
from Item import Item


class Stats:
    enemies = []
    food = []

    def statMenu(self, screen, p):
        mousePos = None
        buttDict = {}
        click = False
        buttDict["atk"] = Button(330, 174, 40, 40, screen, color=(0, 205, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("+", 1, (255, 255, 255)))
        buttDict["hp"] = Button(330, 222, 40, 40, screen, color=(0, 205, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("+", 1, (255, 255, 255)))
        buttDict["regen"] = Button(330, 270, 40, 40, screen, color=(0, 205, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("+", 1, (255, 255, 255)))
        buttDict["speed"] = Button(330, 318, 40, 40, screen, color=(0, 205, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("+", 1, (255, 255, 255)))
        buttDict["reload"] = Button(330, 366, 40, 40, screen, color=(0, 205, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("+", 1, (255, 255, 255)))
        buttDict["reset"] = Button(140, 434, 120, 50, screen, color=(205, 0, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("Reset", 1, (255, 255, 255)))
        buttDict["back"] = Button(30, 550, 200, 70, screen, color=(180, 50, 0), label=pygame.font.SysFont("Microsoft Yahei UI Light", 45).render("Back", 1, (255, 255, 255)))
        itemDict = {}
        itemDict["vampeggs"] = Item(410, 70, 180, 200, screen, p.items["vampeggs"], 50, label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("VampEggs", 1, (255, 255, 255)), description="Heal for 25% of egg damage", img="vampeggicon.png")
        itemDict["eggpen"] = Item(600, 70, 180, 200, screen, p.items["eggpen"], 40, label=pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("EggPen", 1, (255, 255, 255)), description="Eggs pierce through enemies", img="eggpenicon.png")
        myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 70)
        shopLbl = myFont.render("Shop", 1, (255, 255, 255))
        while True:
            screen.fill((100, 100, 150))
            mousePos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                click = False
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return
            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 40)
            pygame.draw.rect(screen, (75, 75, 200), (0, 0, 400, 100))
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 100), 10)
            skillLbl = myFont.render("Skill Points: " + str(p.pts), 1, (255, 255, 255))
            screen.blit(skillLbl, (10, 10))
            screen.blit(myFont.render("Gold: " + str(p.gold), 1, (255, 255, 255)), (10, 20 + skillLbl.get_height()))

            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 60)
            pygame.draw.rect(screen, (75, 75, 200), (0, 100, 400, 400))
            pygame.draw.rect(screen, (0, 0, 0), (0, 100, 400, 400), 10)
            statsLbl = myFont.render("Stats", 1, (255, 255, 255))
            screen.blit(statsLbl, (int(200 - statsLbl.get_width() / 2), 110))
            myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 40)
            screen.blit(myFont.render("Attack: " + str(p.atk) + " (+1)", 1, (255, 255, 255)), (10, 182))
            screen.blit(myFont.render("Health: " + str(p.maxhp) + " (+4)", 1, (255, 255, 255)), (10, 230))
            screen.blit(myFont.render("Regen: " + str(p.regen) + " (-0.5)", 1, (255, 255, 255)), (10, 278))
            screen.blit(myFont.render("Speed: " + str(p.speed) + " (+3)", 1, (255, 255, 255)), (10, 326))
            screen.blit(myFont.render("Reload: " + str(p.reload) + " (-0.1)", 1, (255, 255, 255)), (10, 374))

            screen.blit(shopLbl, (800 - shopLbl.get_width()/2, 10))
            pygame.draw.rect(screen, (75, 75, 200), (400, 500, 800, 150))
            pygame.draw.rect(screen, (0, 0, 0), (400, 500, 800, 150), 10)

            for i in buttDict:
                val = buttDict[i].tick(mousePos, click)
                if val:
                    if i == "reset":
                        p.pts += p.atk - 1
                        p.atk = 1
                        p.pts += (p.maxhp - 10) / 4
                        p.hp -= p.maxhp - 10
                        p.maxhp = 10
                        p.pts += (5 - p.regen) * 2
                        p.regen = 5
                        p.pts += (p.speed - 9) / 3
                        p.speed = 9
                        p.pts += (1 - p.reload) * 10
                        p.reload = 1
                        p.pts = int(round(p.pts))
                    elif i == "back":
                        return
                    elif p.pts > 0:
                        if i == "atk":
                            p.atk += 1
                        if i == "hp":
                            p.hp += 4
                            p.maxhp += 4
                        if i == "regen":
                            p.regen -= 0.5
                        if i == "speed":
                            p.speed += 3
                        if i == "reload" and p.reload > 0.1:
                            p.reload -= 0.1
                            p.reload = round(p.reload*10)/10
                        elif i == "reload":
                            p.pts += 1
                        p.pts -= 1
                    click = False
            for i in itemDict:
                val = itemDict[i].tick(mousePos, click)
                if val >= 1:
                    screen.blit(myFont.render(itemDict[i].description, 1, (255, 255, 255)), (410, 510))
                    if val == 2 and not p.items[i] and p.gold >= itemDict[i].price:
                        itemDict[i].bought = True
                        p.items[i] = True
                        p.gold -= itemDict[i].price

            pygame.display.update()
            pygame.time.Clock().tick(30)
