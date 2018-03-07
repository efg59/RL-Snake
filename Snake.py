from collections import deque
import numpy as np


class Snake(object):

    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, mmap):
        self.speed = 1
        self.location = deque([[np.int(mmap.height/2), np.int(mmap.width/2)]])
        self.direction = Snake.UP
        self.length = 1
        self.map = mmap
        self.points = 0
        self.isDead = False

    def move(self):
        xhead = self.location[-1][1]
        yhead = self.location[-1][0]
        oldPositions = deque()
        for i in range(max(self.speed, self.length)):
            oldPositions.append(self.location.popleft())

        if (self.direction == Snake.LEFT):
            for i in range(self.speed):
                self.location.append([yhead, (xhead-(i+1)) % self.map.width])

        elif(self.direction == Snake.RIGHT):
            for i in range(self.speed):
                self.location.append([yhead, (xhead+(i+1)) % self.map.width])

        elif(self.direction == Snake.UP):
            for i in range(self.speed):
                self.location.append([(yhead-(i+1)) % self.map.height, xhead])

        elif(self.direction == Snake.DOWN):
            for i in range(self.speed):
                self.location.append([(yhead+(i+1)) % self.map.height, xhead])

        self.testLoose()
        if self.isDead:
            self.points -= 50
            return -50
        nb_eaten_fruits = self.countPoints(oldPositions)
        if nb_eaten_fruits >= 1:
            self.location.appendleft(oldPositions.pop())
            reward = 10
        else:
            reward = 1
        self.points += reward

        return reward

    def changeDirection(self, newDirection):
        if((self.direction == Snake.LEFT) or (self.direction == Snake.RIGHT)):
            if((newDirection == Snake.UP) or (newDirection == Snake.DOWN)):
                self.direction = newDirection
        else:
            if((newDirection == Snake.LEFT) or (newDirection == Snake.RIGHT)):
                self.direction = newDirection

    def countPoints(self, oldPositions):
        points = self.map.fruitMap[self.location[-1][0]][self.location[-1][1]]
        self.map.fruitMap[self.location[-1][0]][self.location[-1][1]] = 0
        return points

    def testLoose(self):
        if(np.unique(self.location, axis=0).shape[0] != len(self.location)):
            self.isDead = True
