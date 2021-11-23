import numpy as np
import random
from tabulate import tabulate
from tqdm import tqdm


class QLearning:
    def __init__(self, World):
        self.world = World
        self.max_steps_per_episode = 500
        self.learning_rate = 0.1  # alpha
        self.discount_rate = self.world.gamma  # gamma
        self.exploration_rate = self.world.exploration

    def qLearning(self, num_episodes):
        action_space_size = len(self.world.actions)
        state_space_size = self.world.nStates
        q_table = np.zeros((state_space_size, action_space_size))
        action_counter = np.zeros((state_space_size, action_space_size))
        action_map = {v: k for k, v in zip(self.world.actions, [0, 2, 1, 3])}

        # Q-learning algorithm
        for episode in tqdm(range(num_episodes)):
            # initialize new episode params
            state = self.world.stateStartIndex[0]  # start field
            done = False

            for step in range(self.max_steps_per_episode):
                # Exploration-exploitation trade-off
                exploration_rate_threshold = random.uniform(0, 1)  # explore or exploit the environment
                if exploration_rate_threshold > self.exploration_rate:
                    # exploit the environment and choose the action that has the highest Q-value
                    # in the Q-table for the current state.
                    action = np.argmax(q_table[state - 1, :])
                else:
                    # explore the environment, and sample an action randomly.
                    action = self.world.generateRandomAction()
                action_counter[state - 1][action] += 1  # update action counter
                # Take new action
                new_state, reward, done = self.world.doStep(state, action_map[action])

                # # ***Debugging***
                # print("State: ", state, "  Action: ", action_map[action])
                # print("\nNew state: ", new_state, " reward: ", reward, " done: ", done )
                # # ***************

                # Update Q-table for Q(s,a)
                self.learning_rate = 1 / action_counter[state - 1][action]

                q_table[state - 1, action] = q_table[state - 1, action] * (1 - self.learning_rate) + \
                                             self.learning_rate * (reward + self.discount_rate * np.max(
                    q_table[new_state - 1, :]))

                q_table[state - 1, action] = round(q_table[state - 1, action], 2)
                # Set new state
                state = new_state  # current state is not new state
                # Add new reward
                if done:
                    q_table[state - 1, action] = q_table[state - 1, action] * (1 - self.learning_rate) + \
                                                 self.learning_rate * (reward + self.discount_rate * np.max(
                        q_table[new_state - 1, :]))
                    break
            # Add current episode reward to total rewards list
        return q_table

    def printQTableText(self, Qtable):
        rows_names = np.zeros((self.world.nStates, 1))
        for i in range(0, self.world.nStates):
            rows_names[i][0] = str(i + 1)
        Qtable = np.hstack((rows_names, Qtable))
        headers = ["State", "UP", "RIGHT", "DOWN", "LEFT"]
        table = tabulate(Qtable, headers, "github", numalign="center")
        print(table)

    def extractUtilitiesAndPolicy(self, Qtable):
        utilities = []
        policy = np.zeros((self.world.nStates, 1))
        for i in range(self.world.nStates):
            utilities.append(np.max(Qtable[i, :]))
            policy[i][0] = (np.argmax(Qtable[i, :])) + 1
        return utilities, policy

    def saveQTableToTxt(self, Qtable, filename):
        rows_names = np.zeros((self.world.nStates, 1))
        for i in range(0, self.world.nStates):
            rows_names[i][0] = str(i + 1)
        Qtable = np.hstack((rows_names, Qtable))
        headers = ["State", "UP", "RIGHT", "DOWN", "LEFT"]
        table = tabulate(Qtable, headers, "github", numalign="center")
        with open((filename + "_qtable.txt"), 'w') as file:
            file.write(table)
