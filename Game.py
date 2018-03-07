from SnakeEnvironment import SnakeEnvironment
from SnakeBrain import SnakeBrain
import matplotlib.pyplot as plt
import numpy as np
import time


class Game():

    def __init__(self):
        self.env = SnakeEnvironment(9, 9)
        self.num_episodes = 1000
        self.agent = \
            SnakeBrain(self.env.width*self.env.height, self.env.action_space.n)
        self.rewards = np.zeros(self.num_episodes)

    def run(self):
        for i_episode in range(self.num_episodes):
            state = self.env.reset()
            done = False
            while not done:
                action = self.agent.act(state)
                next_state, reward, done, info = self.env.step(action)
                self.rewards[i_episode] += reward
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                # time.sleep(0.01)
            self.agent.replay(32)
        self.agent.save_model()
        self.statistics()

    def statistics(self):
        episodes = np.arange(0, self.num_episodes)
        plt.figure()
        plt.xlabel("Episodes"), plt.ylabel("Rewards")
        plt.scatter(episodes, self.rewards, marker='+')
        plt.show()


snakeGame = Game()
snakeGame.run()
