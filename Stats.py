import sys

import pygame

from Button import Button


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
                        if i == "reload":
                            p.reload -= 0.1
                            p.reload = round(p.reload*10)/10
                        p.pts -= 1

            pygame.display.update()
            pygame.time.Clock().tick(30)
