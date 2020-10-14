from tensorflow import keras
import numpy as np
from tqdm import tqdm


class Agent(object):
    def __init__(self):
        self.model = keras.Sequential(
            [
                keras.layers.Dense(1, activation="relu", name="state_layer"),
                keras.layers.Dense(100, activation="relu", name="hidden_layer_1"),
                keras.layers.Dense(100, activation="relu", name="hidden_layer_2"),
                keras.layers.Dense(2, name="actions_layer"),
            ]
        )

        self.model.compile(
            optimizer="rmsprop",
            loss='mse'
        )

    def update(self, state, new_y):
        self.model.fit(np.array(state), np.array(new_y), verbose=0)

    def predict(self, state):
        return self.model.predict(np.array(state))

    def get_action(self, state):
        Q = self.model(np.array([state]), training=False)[0]

        p = 1 / (1 + np.exp(np.diff(Q)[0]))  # Action selection using softmax
        p = [p, 1 - p]
        a = np.random.choice(range(2), p=p)  # Sample the action from the softmax distribution
        return a


def vel(theta, theta_0=0, theta_dead=np.pi / 12):
    return 1 - np.exp(-(theta - theta_0) ** 2 / theta_dead)


def rew(theta, theta_0=0, theta_dead=np.pi / 12):
    return vel(theta, theta_0, theta_dead) * np.cos(theta)


random_ys = []
for episode in tqdm(range(100), desc='Running: Random agent on open sea task'):  # run for 500 episodes
    angle = 0  # always start with angle 0
    y = 0
    for i in range(200):
        a = np.random.choice(range(2))  # Sample a random action

        out = [-0.1, 0.1][a]  # Get the change in angle as a result of the selected angle

        y += rew(angle + out)

        # Update the angle
        angle += out

    random_ys.append(y)

agent = Agent()

rho = 0  # Initialize the average reward to 0
td_ys = []
memory = []

angle = 0
y = 0

for i in tqdm(range(50000), desc='Running: Generating training data for the open sea task'):
    angle = np.random.uniform(-np.pi, np.pi)

    a = np.random.choice(range(2))
    out = [-0.1, 0.1][a]  # Get the change in angle as a result of the selected angle

    r = rew(angle + out)

    y += r

    memory.append((angle, angle + out, r, rho, a))

    # Update the angle
    angle += out

    # Update the average reward
    rho += 0.1 * (r - rho)

# Replay
angles = np.array([item[0] for item in memory])
new_angles = np.array([item[1] for item in memory])
rewards = np.array([item[2] for item in memory])
rhos = np.array([item[3] for item in memory])
actions = np.array([item[4] for item in memory])

for i in tqdm(range(300), desc='Running: Training DQN on open sea task'):
    x_train = []
    y_train = []

    Q = agent.predict(angles)
    new_Q = agent.predict(new_angles)

    V = [Q[j, actions[j]] for j in range(len(actions))]
    delta = rewards - rhos + new_Q.max(1)

    x_train = angles.copy()
    y_train = Q.copy()

    for j in range(len(actions)):
        y_train[j, actions[j]] += 0.1 * delta[j]

    agent.update(x_train, y_train)

td_ys = []
memory = []
for episode in tqdm(range(100), desc='Running: Evaluate DQN on open sea task'):  # run for 500 episodes
    angle = 0
    y = 0

    for i in range(200):
        a = agent.get_action(angle)
        out = [-0.1, 0.1][a]  # Get the change in angle as a result of the selected angle

        r = rew(angle + out)

        y += r

        # Update the angle
        angle += out

        # Update the average reward
        rho += 0.1 * (r - rho)

    td_ys.append(y)

# Display results
random_mean = np.mean(random_ys[-100:])
random_std = np.std(random_ys[-100:])

td_mean = np.mean(td_ys[-100:])
td_stq = np.std(td_ys[-100:])

print('Results from last 100 episodes')
print('| ===== agent ===== | ===== mean ===== | ===== std ===== |')
print(f'{"| Random":<20}| {random_mean:<17.2f}| {random_std:<16.2f}|')
print(f'{"| DQN":<20}| {td_mean:<17.2f}| {td_stq:<16.2f}|')
