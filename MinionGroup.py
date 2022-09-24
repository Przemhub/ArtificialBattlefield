import sys

from Minion import Minion
import json

class MinionGroup:
    def __init__(self,minion_num,load=False,grp_name = ""):
        self.minionList = []
        self.minionDict = {}
        if load == True:
            self.load(grp_name)
        else:
            for i in range(0,minion_num):
                self.minionList.append(Minion())
    def reset_wins(self):
        for m in self.minionList:
            m.temp_wins = 0
            m.temp_loses = 0

    def save(self,group_name):
        minion = {}
        for i in range(0,len(self.minionList)):
            minion[i] = {"NAME":"","HEALTH":self.minionList[i].health,"DMG":self.minionList[i].damage,"ATK SPEED":self.minionList[i].attack_speed,
                               "SPELL SPEED":self.minionList[i].spell_speed,"ATK PROB":self.minionList[i].attack_prob,"DOG PROB":self.minionList[i].dodge_prob,
                                "DEF PROB":self.minionList[i].defend_prob,"SPELL PROB":self.minionList[i].spell_prob,"WINS":self.minionList[i].wins,"LOSSES":self.minionList[i].loses}

        self.minionDict[group_name] = minion
        with open("my_minions.json", 'a') as f:
            json.dump(self.minionDict,f)

    def load(self,group_name):
        dicts = {}
        with open("my_minions.json", 'r') as f:
            dict = json.load(f)

        self.minionDict = dict[group_name]
        for key in self.minionDict.keys():
            temp = Minion()
            temp.name = self.minionDict[key]["NAME"]
            temp.health = self.minionDict[key]["HEALTH"]
            temp.damage = self.minionDict[key]["DMG"]
            temp.attack_speed = self.minionDict[key]["ATK SPEED"]
            temp.spell_speed = self.minionDict[key]["SPELL SPEED"]
            temp.attack_prob = self.minionDict[key]["ATK PROB"]
            temp.dodge_prob = self.minionDict[key]["DOG PROB"]
            temp.defend_prob = self.minionDict[key]["DEF PROB"]
            temp.spell_prob = self.minionDict[key]["SPELL PROB"]
            temp.wins = self.minionDict[key]["WINS"]
            temp.loses = self.minionDict[key]["LOSSES"]
            self.minionList.append(temp)
