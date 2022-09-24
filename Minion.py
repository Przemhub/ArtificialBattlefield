import json
from math import fabs
from random import Random

class Minion:
    def __init__(self):
        self.random = Random()
        self.init_params()
        self.init_probabilities()
        self.init_stats()
        self.init_state()

    def init_probabilities(self):
        self.attack_prob = self.random.randint(0,10)
        self.defend_prob = self.random.randint(0,(10 - self.attack_prob))
        self.spell_prob = self.random.randint(0,10 - (self.defend_prob + self.attack_prob))
        self.dodge_prob = 10 - (self.attack_prob + self.defend_prob + self.spell_prob)
    def init_params(self):
        self.health = self.random.randint(1, 200)
        self.damage = self.random.randint(1, 50)
        self.attack_speed = self.random.randint(10, 50)
        self.spell_speed = self.random.randint(0, 40)
        self.double_attack = 0
        self.spell_energy = 0
        self.ATTACK_LIMIT = 100
        self.SPELL_LIMIT = 100

    def init_stats(self):
        self.name = ""
        self.wins = 0
        self.loses = 0
        self.temp_wins = 0
        self.temp_loses = 0

    def init_state(self):
        self.dodged = False
        self.attacked = False
        self.defended = False
        self.spelled = False

    def show_params(self):
        print("---------------PARAMETERS------------------")
        print()
        print("NAME:   ",self.name)
        print("HEALTH:   ",self.health)
        print("DAMAGE:   ",self.damage)
        print("ATTACK SPEED:   ",self.attack_speed)
        print("SPELL SPEED:   ",self.spell_speed)
        print("\n\n---------------PROBABILITIES------------------")
        print()
        print("ATTACK:   ",self.attack_prob)
        print("DODGE:   ",self.dodge_prob)
        print("DEFEND:   ",self.defend_prob)
        print("SPELL:   ",self.spell_prob)
        print("WINS:   ",self.wins)
        print("LOSSES:   ",self.loses)

    def set_status(self,status):
        self.dodged = False
        self.attacked = False
        self.defended = False
        self.spelled = False
        if status == "dodged":
            self.dodged = True
        elif status == "attacked":
            self.attacked = True
        elif status == "defended":
            self.defended = True
        elif status == "spelled":
            self.spelled = True
        else:
            print("No such status as: ",status)

    def get_status(self):
        if self.dodged == True:
            return "dodged"
        elif self.attacked == True:
            return "attacked"
        elif self.defended == True:
            return "defended"
        elif self.spelled == True:
            return "spelled"

    def attack(self, enemy):
        repeat = 0
        if self.double_attack >= self.ATTACK_LIMIT:
            repeat = 1
            self.double_attack -= self.ATTACK_LIMIT
        for i in range(0,repeat + 1):
            if enemy.get_status() == "defended":
                enemy.health -= int(self.damage/2)
            elif enemy.get_status() != "dodged":
                enemy.health -= self.damage
        self.set_status("attacked")

    def defend(self):
        self.set_status("defended")

    def throw_spell(self, enemy):
        if self.spell_energy >= self.SPELL_LIMIT:
            if enemy.get_status() == "dodged":
                enemy.health -= self.damage*2
            elif enemy.get_status() == "defended":
                enemy.health -= (self.damage)
            else:
                enemy.health -= (self.damage + int(self.damage/2))
            self.spell_energy -= self.SPELL_LIMIT
        self.set_status("spelled")


    def dodge(self):
        self.set_status("dodged")
    def load(self,grp_name,key):

        with open("my_minions.json", 'r') as f:
            dict = json.load(f)

        self.minionDict = dict[grp_name]
        self.name = self.minionDict[key]["NAME"]
        self.health = self.minionDict[key]["HEALTH"]
        self.damage = self.minionDict[key]["DMG"]
        self.attack_speed = self.minionDict[key]["ATK SPEED"]
        self.spell_speed = self.minionDict[key]["SPELL SPEED"]
        self.attack_prob = self.minionDict[key]["ATK PROB"]
        self.dodge_prob = self.minionDict[key]["DOG PROB"]
        self.defend_prob = self.minionDict[key]["DEF PROB"]
        self.spell_prob = self.minionDict[key]["SPELL PROB"]
        self.wins = self.minionDict[key]["WINS"]
        self.loses = self.minionDict[key]["LOSSES"]

    def roll_move(self,enemy):
        temp_rand = Random()
        roll = temp_rand.randint(1,10)
        if roll < self.dodge_prob:
            self.dodge()
        elif roll < (self.spell_prob + self.dodge_prob):
            self.throw_spell(enemy)
        elif roll <= (self.dodge_prob + self.spell_prob + self.defend_prob):
            self.defend()
        else:
            self.attack(enemy)
        self.post_move_adjustments()


    def post_move_adjustments(self):
        self.spell_energy += self.spell_speed
        self.double_attack += self.attack_speed
    def is_dead(self):
        if self.health <= 0:
            return True
        return False
    def copy(self):
        minion = Minion()
        minion.health = self.health
        minion.temp_loses = self.temp_loses
        minion.temp_wins = self.temp_wins
        minion.wins = self.wins
        minion.loses = self.loses
        minion.damage = self.damage
        minion.attack_speed= self.attack_speed
        minion.spell_speed = self.spell_speed
        minion.name = self.name
        minion.spell_prob = self.spell_prob
        minion.defend_prob = self.defend_prob
        minion.attack_prob = self.attack_prob
        minion.dodge_prob = self.dodge_prob
        return minion