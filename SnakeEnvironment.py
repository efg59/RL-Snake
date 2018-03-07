import gym
from Map import Map
from Snake import Snake
import numpy as np
import pygame


class SnakeEnvironment(gym.Env):

    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, width, height):
        """
        The action space is composed by the five actions up, down,
        right, left, nothing

        the observation space is composed by :
            - the position of the head
            - a binary map of the position of the snake (flattened)
            - a map of the fruits (flattened)
        """
        pygame.init()
        self.width = width
        self.height = height
        self.map = Map(self.height, self.width)
        self.snake = Snake(self.map)
        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = gym.spaces.MultiDiscrete(4*np.ones(self.width*self.height))

    def step(self, action):
        assert(self.action_space.contains(action))
        self.snake.changeDirection(action)
        reward = self.snake.move()

        if reward > 1:
            self.map.newFruit(self.snake.location)
        self.map.time += 1

        return(self._get_obs(), reward, self.snake.isDead, {})

    def _get_obs(self):
        snakeMapFlattened = np.zeros(self.height*self.width, dtype=np.int64)
        head = self.snake.location[-1]
        snakeMapFlattened[head[0]*self.height+head[1]] = 1
        for t in range(1, len(self.snake.location)):
            snakeMapFlattened[self.snake.location[t][0]*self.height+self.snake.location[t][1]] = 2
        snakeMapFlattened += 3*self.map.fruitMap.reshape(self.width*self.height)
        return(snakeMapFlattened)

    def reset(self):
        self.map = Map(self.height, self.width)
        self.snake = Snake(self.map)
        self.map.newFruit(self.snake.location)
        return(self._get_obs())

    def render(self, mode='Computer'):
        self.map.render(self, self.snake, mode)
