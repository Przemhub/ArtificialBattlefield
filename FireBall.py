from math import fabs

from pygame import Rect, time,image


class Fireball:
    def __init__(self):
        self.block = Rect(-80, 0, 80, 80)
        self.pathX_list = []
        self.pathY_list = []
        self.wait_list = []
        self.speed = 5
        self.wait_time = 0
        self.start_time = time.get_ticks()
        self.start_time2 = time.get_ticks()
        self.image = image.load("Fireball/fireball.png").convert_alpha()
        self.direction = 0

    def move(self,x,y):
        self.block = self.block.move(x,y)

    def reset(self):
        self.start_time2 = time.get_ticks() - 1.5 * 1000
        self.speed = 5
        self.bullet = Rect(-80,0,80,80)
        self.pathY_list.clear()
        self.pathX_list.clear()
        self.wait_list.clear()
    def shoot(self, command):
        # print("IN")
        x = 0
        y = 0
        sign = 1  # in case of a negative number
        coord = 'z'
        # analyze command for the first time
        if len(self.pathX_list) == 0:
            self.analyze_cmd(command)
        # find values that are not zeros
        x = len(self.pathX_list)  # in case value has not been found, (important)
        y = len(self.pathY_list)
        for path in self.pathX_list:
            if path != 0:
                x = self.pathX_list.index(path)
                break
        for path in self.pathY_list:
            if path != 0:
                y = self.pathY_list.index(path)
                break
        if x < y:
            coord = 'x'
            y = x
            if self.is_waiting(x):
                return
            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            self.move(-self.speed *sign, 0)
            if self.speed < 45:
                self.speed+=10


        elif y < x:
            coord = 'y'
            x = y
            if self.is_waiting(x):
                return
            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            self.move(0, -self.speed * sign)
        else:
            coord = 'xy'
            if x < len(self.pathX_list):
                if self.is_waiting(x):
                    return
                sign = self.check_sign(x, y)
                self.move(self.speed*sign,self.speed*sign)

        if x == len(self.pathX_list) and y == len(self.pathY_list):
            self.pathY_list.clear()
            self.pathX_list.clear()
            self.wait_list.clear()
            return
        self.pathX_list[x] -= (self.pathX_list[x] > 0) * self.speed
        self.pathY_list[y] -= (self.pathY_list[y] > 0) * self.speed

        if self.pathX_list[x] < 0:
            self.pathX_list[x] = 0
        if self.pathY_list[y] < 0:
            self.pathY_list[y] = 0
        # check if a command has been finished
        if coord == 'x':
            if self.pathX_list[x] == 0:
                self.start_time = time.get_ticks()
        elif coord == 'y':
            if self.pathY_list[y] == 0:
                self.start_time = time.get_ticks()
        elif coord == 'xy':
            if self.pathX_list[x] == 0 and self.pathY_list[y] == 0:
                self.start_time = time.get_ticks()

        self.pathX_list[x] = self.pathX_list[x] * sign
        self.pathY_list[y] = self.pathY_list[y] * sign

    def check_sign(self,x,y):
        if self.pathX_list[x] < 0 or self.pathY_list[y] < 0:
            self.pathY_list[y] = fabs(self.pathY_list[y])
            self.pathX_list[x] = fabs(self.pathX_list[x])
            return -1
        return 1

    def analyze_cmd(self, command):
        dist = 0
        wait = 0
        for cmd in command.split(','):
            # pick out coord value and write to dist
            for char in list(cmd):
                if char.isdigit() or char == '-':
                    dist = float(cmd[cmd.index(char):cmd.index('W')])
                    break
            # pick Waiting time from command
            wait = float(cmd[(cmd.index('W') + 1):])
            self.wait_list.append(wait)

            if cmd[0] == 'X' and cmd[1] == 'Y':
                self.pathX_list.append(dist)
                self.pathY_list.append(dist)
            elif cmd[0] == 'Y':
                self.pathY_list.append(dist)
                self.pathX_list.append(0)
            elif cmd[0] == 'X':
                self.pathX_list.append(dist)
                self.pathY_list.append(0)
            else:
                raise Exception("Incorrect command: " + command + ", should be as example \"X50,XY60,Y-10\"")
    def is_waiting(self, i):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.wait_list[i]:
            return False
        return True
    def is_active(self):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time2) / 1000
        if seconds_passed > self.wait_time:
            return False
        return True
    def make_wait(self):
        self.start_time2 = time.get_ticks()
        self.wait_time = 0.6