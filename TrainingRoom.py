import json
import time
from random import Random

from Arena import Arena
from Minion import Minion


class TrainingRoom:
    def __init__(self,minionGroup):
        self.group = minionGroup
        self.minions = minionGroup.minionList
        self.breed_section = []
        self.best_section = []

    def train(self):
        n=0
        for m1 in self.minions:
            for i2 in range(n,len(self.minions)):
                self.fight(m1,self.minions[i2])
            n+=1

        for m in self.minions:
            if m.temp_wins > int(len(self.minions)*8/10):
                self.best_section.append(m)

            elif m.temp_wins > int(len(self.minions)/2):
                self.breed_section.append(m)
            else:
                self.minions.remove(m)

    def mass_train(self,gen_number):
        for i in range(0,gen_number):
            self.train()
            self.minions.clear()
            for i in range(1,len(self.breed_section)):
                self.breed(self.breed_section[i-1],self.breed_section[i])
                i+=1

            # self.minions += self.best_section
            # self.best_section.clear()
            self.breed_section.clear()
            self.group.reset_wins()
            if len(self.minions) < 8:
                print("training stopped after generation ",gen_number)

                break

    def fight(self,minion1,minion2):
        m1 = minion1.copy()
        m2 = minion2.copy()
        moves = 0
        while m1.is_dead() == False and m2.is_dead() == False and moves < 12:
            m1.roll_move(m2)
            m2.roll_move(m1)
            m2.roll_move(m1)
            m1.roll_move(m2)
            moves+=1
        if m2.health > m1.health:
            minion1.loses += 1
            minion2.wins += 1
            minion1.temp_loses += 1
            minion2.temp_wins += 1
        elif m1.health > m2.health:
            minion2.loses +=1
            minion1.wins +=1
            minion1.temp_loses += 1
            minion2.temp_wins += 1
        else:
            minion1.loses +=1
            minion2.loses +=1

    def breed(self,m1,m2):
        coin = Random()
        child = Minion()
        mutation = Random()
        flip = coin.randint(1, 2)
        #Damage
        if flip == 1:
            child.damage = m1.damage
        else:
            child.damage = m2.damage
        value = mutation.randint(0, 10)
        if value < 2:
            child.damage -= mutation.randint(1, 7)
        elif value > 8:
            child.damage+= mutation.randint(1, 7)
        #Health
        flip = coin.randint(1, 2)
        if flip == 1:
            child.health = m1.health
        else:
            child.health = m2.health
        value = mutation.randint(0, 10)
        if value < 2:
            child.health -= mutation.randint(1, 30)
        elif value > 8:
            child.health += mutation.randint(1, 30)
        #ATK Speed
        flip = coin.randint(1,2)
        if flip == 1:
            child.attack_speed = m1.attack_speed
        else:
            child.attack_speed = m2.attack_speed
        value = mutation.randint(0, 10)
        if value < 2:
            child.attack_speed -= mutation.randint(1, 7)
        elif value > 8:
            child.attack_speed += mutation.randint(1, 7)
        #SPELL Speed
        flip = coin.randint(1, 2)
        if flip == 1:
            child.spell_speed = m1.spell_speed
        else:
            child.spell_speed = m2.spell_speed
        value = mutation.randint(0, 10)
        if value < 2:
            child.spell_speed -= mutation.randint(1, 6)
        elif value > 8:
            child.spell_speed += mutation.randint(1, 6)

        #PROBABILITES
        flip = coin.randint(1, 2)
        if flip == 1:
            child.dodge_prob = m1.dodge_prob
            child.attack_prob = m1.attack_prob
            child.spell_prob = m1.spell_prob
            child.defend_prob = m1.defend_prob
        else:
            child.dodge_prob = m2.dodge_prob
            child.attack_prob = m2.attack_prob
            child.spell_prob = m2.spell_prob
            child.defend_prob = m2.defend_prob
        value = mutation.randint(0, 10)
        if value < 2:
            target = mutation.randint(1,4)
            prob_val = mutation.randint(1,3)
            if target == 1:
                child.attack_prob -= prob_val
            elif target == 2:
                child.defend_prob -= prob_val
            elif target == 3:
                child.spell_prob -= prob_val
            elif target == 4:
                child.dodge_prob -= prob_val
        elif value > 8:
            target = mutation.randint(1, 4)
            prob_val = mutation.randint(1, 3)
            if target == 1:
                child.attack_prob += prob_val
            elif target == 2:
                child.defend_prob += prob_val
            elif target == 3:
                child.spell_prob += prob_val
            elif target == 4:
                child.dodge_prob += prob_val
        self.minions.append(child)

    def save_best(self,group_name):
        minion = {}
        minionDict = {}
        for i in range(0,len(self.best_section)):
            minion[i] = {"NAME":"","HEALTH":self.best_section[i].health,"DMG":self.best_section[i].damage,"ATK SPEED":self.best_section[i].attack_speed,
                               "SPELL SPEED":self.best_section[i].spell_speed,"ATK PROB":self.best_section[i].attack_prob,"DOG PROB":self.best_section[i].dodge_prob,
                                "DEF PROB":self.best_section[i].defend_prob,"SPELL PROB":self.best_section[i].spell_prob,"WINS":self.best_section[i].wins,"LOSSES":self.best_section[i].loses}

        minionDict[group_name] = minion
        with open("best_minions.json", 'w') as f:
            json.dump(minionDict,f)