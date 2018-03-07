import numpy as np
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class SnakeBrain():

    def __init__(self, state_size, action_size):
        self.weights_backup = "snake_weights.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.memory_size = 2000  # -1 for infinite memory
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.decay = 0.995
        self.gamma = 0.95
        self.learning_rate = 0.1
        self.model = self._build_model()
        self.iter = 0

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if self.memory_size > 0 and len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def save_model(self):
        self.model.save(self.weights_backup)

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_size)
        else:
            act_values = self.model.predict(state)
            return np.argmax(act_values[0])

    def sample_batch(self, batch_size):
        return [self.memory[np.random.randint(len(self.memory))] for event in range(batch_size)]

    def replay(self, batch_size):
        self.iter += 1
        minibatch = self.sample_batch(batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            state = np.reshape(state, (1, 81))
            if not done:
                target = reward + \
                    self.gamma*np.amax(self.model.predict(state)[0])
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
                self.epsilon *= self.decay # Gros problème au niveau de l'évolution de l'epsilon
