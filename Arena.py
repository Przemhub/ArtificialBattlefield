import random
import sys
import time

import pygame

from FireBall import Fireball
from NPC import NPC

class Arena:
    def __init__(self,image1=None,image2=None):
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()

        self.init_sounds()
        self.clk = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 300))
        self.npc1 = NPC(160, 100, 10,1)
        self.npc2 = NPC(300, 100, 10,2)
        if image1 != None:
            self.npc1.image = pygame.image.load("Favourite/" + image1)
        if image2 != None:
            self.npc2.image = pygame.image.load("Favourite/" + image2)
        self.ball = Fireball()
        self.draw_wall = False
        self.hp1 = 0
        self.hp2 = 0
        self.init_images()
        self.init_text()
        self.init_actions()

    def draw(self):
        self.screen.fill((255,255,255))
        self.screen.blit(self.arena,(0,0))
        self.screen.blit(self.npc1.image, self.npc1.block)
        self.screen.blit(self.npc2.image, self.npc2.block)
        self.screen.blit(self.text,self.text_block)
        pygame.draw.rect(self.screen,(255,20,20),self.hp1_bar_block)
        pygame.draw.rect(self.screen, (255, 20, 20), self.hp2_bar_block)
        self.screen.blit(self.hp1_text,self.hp1_bar_block)
        self.screen.blit(self.hp2_text, self.hp2_bar_block)
        self.screen.blit(self.ball.image,self.ball.block)
        self.screen.blit(self.npc1_status,self.npc_status_block)
        self.screen.blit(self.npc2_status,self.npc_status_block.move(150,0))
        if self.draw_wall == True:
            self.screen.blit(self.firewall,self.firewall_block)
        pygame.display.flip()
    def init_actions(self):
        self.ATTACK = 0
        self.DODGE = 1
    def init_images(self):
        self.arena = pygame.image.load("Arena/arena1.png")

        self.hp1_bar_block = pygame.Rect(50,40,self.hp1,40)
        self.hp2_bar_block = pygame.Rect(350, 40,self.hp2,40)
        self.firewall = pygame.image.load("Fireball/firewall.png")
        self.firewall_block = pygame.Rect(160,100,1,1)
    def init_sounds(self):
        self.battles = ["Soundtrack/gothic.mp3","Soundtrack/battle2.mid",
                            "Soundtrack/battle4.mid","Soundtrack/battle5.mid"]
        self.dodge_sound = pygame.mixer.Sound("Soundtrack/dodge.ogg")
        self.attack_sound = pygame.mixer.Sound("Soundtrack/atk.ogg")
        self.def_sound = pygame.mixer.Sound("Soundtrack/def.ogg")
        self.spell1_sound = pygame.mixer.Sound("Soundtrack/spell1.ogg")
        self.spell2_sound = pygame.mixer.Sound("Soundtrack/spell2.ogg")

    def init_text(self):
        self.font = pygame.font.SysFont("Calibri", 24, True)
        self.text = self.font.render("", True, (255, 255, 255), (0, 0, 0))
        self.text_block = pygame.Rect(90, 240, 1, 1)
        self.hp1_text = self.font.render("HP",True,(255,255,255))
        self.hp2_text = self.font.render("HP",True,(255,255,255))
        self.npc1_status = self.font.render("",True,(255,255,255))
        self.npc2_status = self.font.render("", True, (255, 255, 255))
        self.npc_status_block = pygame.Rect(140,170,1,1)
    def move(self,npc,action=0):
        time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if action == self.ATTACK:
                if time == 10:
                    self.attack_sound.play()
                if npc.id == 2:
                    npc.move("X-80W0.5,X80W0.7")
                elif npc.id == 1:
                    npc.move("X80W0.1,X-80W0.7")
            elif action == self.DODGE:
                if time == 6:
                    self.dodge_sound.play()
                npc.move("Y-25W0.7")
            else:
                npc.move("Y25W0.7")
            self.draw()
            self.clk.tick(30)
            if time > 35:
                npc.reset()
                if npc.id == 1:
                    self.npc1.block = pygame.Rect(160, 100, 1,1)
                elif npc.id == 2:
                    self.npc2.block = pygame.Rect(300, 100, 1,1)
                break
            time+=1
    def spell(self,npc):
        time = 0
        if npc.id == 1:
            self.firewall_block.x = npc.x + 150
        else:
            self.firewall_block.x = npc.x - 150
        self.ball.block.x = npc.x
        self.ball.block.y = npc.y
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if npc.id == 1:
                self.ball.shoot("X-200W0.1")
            else:
                self.ball.shoot("X200W0.1")
            if time == 2:
                self.spell1_sound.play()
            if time == 13:
                self.spell2_sound.play()
            self.draw()
            self.clk.tick(30)
            if time > 6 and time < 12:
                self.ball.reset()
                self.draw_wall = True
            elif time > 30:
                self.draw_wall = False
                self.ball.reset()
                break
            time += 1
    def min1_turn(self,min1,min2,name1,name2):
        hp = min2.health
        min1.roll_move(min2)

        if min1.get_status() == "attacked":
            self.text = self.font.render(name1 + " strikes " + name2 + " for " + str(hp - min2.health) + " HP", True, (255, 255, 255))
            print(name1 + " strikes " + name2 + " for", hp - min2.health, "HP")
            self.move(self.npc1, action=self.ATTACK)
        elif min1.get_status() == "dodged":
            self.text = self.font.render(name1 + " chooses dodging stance", True, (255, 255, 255))
            print(name1 + " chooses dodging stance")
            self.move(self.npc1, action=self.DODGE)
            self.npc1_status = self.font.render("DOD", True, (255, 255, 255))
        elif min1.get_status() == "defended":
            self.text = self.font.render(name1 + " chooses defence stance", True, (255, 255, 255))
            print(name1 + " chooses defence stance")
            self.def_sound.play()
            self.draw()
            self.npc1_status = self.font.render("DEF", True, (255, 255, 255))
            pygame.time.delay(1000)
        elif min1.get_status() == "spelled":
            self.text = self.font.render(name1 + " throws spell on " + name2 + " for " + str(hp - min2.health) + " HP", True,
                                         (255, 255, 255))
            print(name1 + " throws spell on " + name2 + " for", hp - min2.health, "HP")
            self.spell(self.npc1)
        self.hp2 = min2.health * (min2.health > 0)
        self.hp2_text = self.font.render(str(min2.health) + "HP", True, (255, 255, 255))
        self.hp2_bar_block.width = self.hp2
    def min2_turn(self,min1,min2,name1,name2):
        hp = min1.health
        min2.roll_move(min1)
        if min2.get_status() == "attacked":
            self.text = self.font.render(name2 + " strikes " + name1 + " for " + str(hp - min1.health) + " HP", True,
                                         (255, 255, 255))
            print(name2 + " strikes " + name1 + "for", hp - min1.health, "HP")
            self.move(self.npc2, action=self.ATTACK)
        elif min2.get_status() == "dodged":
            self.text = self.font.render(name2 + " chooses dodging stance", True, (255, 255, 255))
            print(name2 + " chooses dodging stance")
            self.move(self.npc2, action=self.DODGE)
            self.npc2_status = self.font.render("DOD", True, (255, 255, 255))
        elif min2.get_status() == "defended":
            self.text = self.font.render(name2 + " chooses defence stance", True, (255, 255, 255))
            print(name2 + " chooses defence stance")
            self.def_sound.play()
            self.draw()
            self.npc2_status = self.font.render("DEF", True, (255, 255, 255))
            pygame.time.delay(2000)
        elif min2.get_status() == "spelled":
            self.text = self.font.render(name2 + " throws spell on " + name1 + " for " + str(hp - min1.health) + " HP", True,
                                         (255, 255, 255))
            print(name2 + " throws spell on " + name1 + "for", hp - min1.health, "HP")
            self.spell(self.npc2)
        self.hp1 = min1.health * (min1.health > 0)
        self.hp1_text = self.font.render(str(min1.health) + "HP", True, (255, 255, 255))
        self.hp1_bar_block.width = self.hp1
    def fight(self,m1,m2):
        min1 = m1.copy()
        min2 = m2.copy()
        name1 = "Minion1"
        name2 = "Minion2"
        rand = random.Random()
        pygame.mixer.music.load(self.battles[rand.randint(0,3)])
        pygame.mixer.music.play()
        if min1.name != "":
            name1 = min1.name
        if min2.name != "":
            name2 = min2.name
        moves = 0
        self.hp1 = min1.health
        self.hp2 = min2.health
        self.hp1_text = self.font.render(str(min1.health) + "HP",True,(255,255,255))
        self.hp2_text = self.font.render(str(min2.health) + "HP", True, (255, 255, 255))
        self.hp2_bar_block.width = self.hp2
        self.hp1_bar_block.width = self.hp1
        turn_list = [self.min1_turn,self.min2_turn]
        i = 0
        while min1.is_dead() == False and min2.is_dead() == False and moves < 10:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            turn_list[i](min1,min2,name1,name2)
            turn_list[i+1](min1,min2,name1,name2)
            self.text = self.font.render(name1 + " HP= "+str(min1.health) + "        " + name2 + " HP= " + str(min2.health),True,(255,255,255))
            print(name1 + " HP=",min1.health)
            print(name2 + " HP=",min2.health)
            print()
            self.draw()
            pygame.time.delay(3000)
            if moves % 2 == 0:
                i = 0
            else:
                i= -1
            moves += 1
            self.clk.tick(30)
            self.npc1_status = self.font.render("", True, (255, 255, 255))
            self.npc2_status = self.font.render("", True, (255, 255, 255))
        if min2.health > min1.health:
            m1.loses += 1
            m2.wins += 1
            print(name2 + " wins!")
        elif min1.health > min2.health:
            m2.loses += 1
            m1.wins += 1
            print(name1 + " wins!")
        return

