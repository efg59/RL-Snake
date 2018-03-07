import numpy as np


class TabularBrain():

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.decay = 0.995
        self.gamma = 0.95
        self.learning_rate = 0.001
        self.Q_table

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
        if len(self.memory) < batch_size:
            return None
        return np.array(np.sample(self.memory, batch_size))

    def replay(self, batch_size):
        minibatch = self.sample_batch(batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + \
                    self.gamma*np.amax(self.model.predict(state)[0])
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.decay
