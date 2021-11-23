# Kamil Goś 235184
import numpy as np
import matplotlib.pyplot as plt
import random
from tabulate import tabulate

class World:
    def __init__(self):
        self.nRows = 3
        self.nCols = 4
        self.nStates = self.nRows * self.nCols
        self.start = [[0,0]]
        self.stateStartIndex = [self.nRows]
        self.start_appear = None
        self.prob = [0.8, 0.1, 0.1]
        self.step_reward = -0.04
        self.gamma = 1.0
        self.exploration = None
        self.stateTerminals = []
        self.stateTerminalsIndexes = []
        self.stateSpecial = []
        self.stateSpecialIndexes = []
        self.stateForbidden = []
        self.stateForbiddenIndexes = []
        self.actions = ["U", "D", "R", "L"]
        self.rewards = np.array([self.step_reward] * self.nStates)

    def readFile(self, filename):
        file = open(filename)
        try:
            text = file.readlines()
        except:
            print("*** ERROR: Cant read file ***")
            return 1
        finally:
            file.close()
            print("Data taken from file")
        self.updateWorld(text)

    def updateWorld(self, text):
        for line in text:
            line = line.split()
            if line[0] == "W":
                self.nCols = int(line[1])
                self.nRows = int(line[2])
            if line[0] == "S":
                self.start = []
                self.start.append([int(line[1]), int(line[2])])
                self.start_appear = True
            if line[0] == "P":
                self.prob = [float(line[1]), float(line[2]), float(line[3])]
            if line[0] == "R":
                self.step_reward = float(line[1])
            if line[0] == "G":
                self.gamma = float(line[1])
            if line[0] == "E":
                self.exploration = float(line[1])
            if line[0] == "T":
                self.stateTerminals.append([int(line[1]), int(line[2]), float(line[3])])
            if line[0] == "B":
                self.stateSpecial.append([int(line[1]), int(line[2]), float(line[3])])
            if line[0] == "F":
                self.stateForbidden.append([int(line[1]), int(line[2])])
            if line[0] == 'E':
                self.exploration = float(line[1])
        self.nStates = self.nRows * self.nCols
        self.rewards = np.array([self.step_reward] * self.nStates)
        self.translateToIndexes()

    def showWorldValues(self):
        print("============ WORLD INFOS ==============")
        print("World size: ", self.nRows, " x ", self.nCols)
        print("Start: ", self.start, "  Index: ", self.stateStartIndex)
        print("Probabilities: ", self.prob)
        print("Step reward: ", self.step_reward)
        print("Discounting parameter: ", self.gamma)
        print("Terminal states: ", self.stateTerminals, "  Indexes: ", self.stateTerminalsIndexes)
        print("Special states: ", self.stateSpecial, "  Indexes: ", self.stateSpecialIndexes)
        print("Forbidden states: ", self.stateForbidden, "  Indexes: ", self.stateForbiddenIndexes)
        print("Exploration parameter: ", self.exploration)

    def translateToIndexes(self):
        for state in self.stateTerminals:
            index = int(state[0] * self.nRows - (state[1] - 1))
            self.rewards[index - 1] = state[2]
            self.stateTerminalsIndexes.append(index)
        for state in self.stateSpecial:
            index = int(state[0] * self.nRows - (state[1] - 1))
            self.rewards[index - 1] = state[2]
            self.stateSpecialIndexes.append(index)
        for state in self.stateForbidden:
            index = int(state[0] * self.nRows - (state[1] - 1))
            self.rewards[index - 1] = 0.0
            self.stateForbiddenIndexes.append(index)
        if self.start_appear:
            for state in self.start:
                self.stateStartIndex = []
                print(state)
                index = int(state[0] * self.nRows - (state[1] - 1))
                self.stateStartIndex.append(index)

    def generateRandomAction(self):
        return random.randint(0,len(self.actions)-1)

    def doStep(self, state, action):
        nrows = self.nRows
        nstates = self.nStates
        done = False

        if action == "U":  # UP
            new_state = state - 1
            if new_state%nrows == 0: # upper wall
                new_state = state
            if new_state in self.stateForbiddenIndexes: # forbidden (stay in place)
                new_state = state
            if new_state in self.stateTerminalsIndexes:
                done = True

        if action == "D":  # DOWN
            new_state = state + 1
            if (new_state-1) % nrows == 0:  # lower wall
                new_state = state
            if new_state in self.stateForbiddenIndexes: # forbidden (stay in place)
                new_state = state
            if new_state in self.stateTerminalsIndexes:
                done = True

        if action == "R":  # RIGHT
            new_state = state + self.nCols
            if new_state > nstates:  # right wall
                new_state = state
            if new_state in self.stateForbiddenIndexes: # forbidden (stay in place)
                new_state = state
            if new_state in self.stateTerminalsIndexes:
                done = True

        if action == "L":  # LEFT
            new_state = state - self.nCols
            if new_state < 1:  # left wall
                new_state = state
            if new_state in self.stateForbiddenIndexes: # forbidden (stay in place)
                new_state = state
            if new_state in self.stateTerminalsIndexes:
                done = True

        reward = self.rewards[new_state-1]
        return new_state, reward, done


    def createCoordinates(self, index):
        (I, J) = np.unravel_index(index - 1, shape=(self.nRows, self.nCols), order='F')
        coord = [[J, self.nRows - I],
                 [J + 1, self.nRows - I],
                 [J + 1, self.nRows - I - 1],
                 [J, self.nRows - I - 1],
                 [J, self.nRows - I]]
        return zip(*coord)

    def plotTemplate(self):
        ## plot outside rectangle
        coord = [[0, 0], [self.nCols, 0], [self.nCols, self.nRows], [0, self.nRows], [0, 0]]
        xs, ys = zip(*coord)
        plt.plot(xs, ys, "black")

        # plot obstacles as black squares
        for i in self.stateForbiddenIndexes:
            xs, ys = self.createCoordinates(i)
            plt.fill(xs, ys, "black")
            plt.plot(xs, ys, "black")

        # plot forbidden as lightgreen squares
        for i in self.stateTerminalsIndexes:
            xs, ys = self.createCoordinates(i)
            plt.fill(xs, ys, "lightgreen")
            plt.plot(xs, ys, "black")

        # plot specials as gold squares
        for i in self.stateSpecialIndexes:
            xs, ys = self.createCoordinates(i)
            plt.fill(xs, ys, "gold",zorder=1)
            plt.plot(xs, ys, "black",zorder=1)

        # plot start as blue squares
        for i in self.stateStartIndex:
            xs, ys = self.createCoordinates(i)
            plt.fill(xs, ys, "deepskyblue",zorder=1)
            plt.plot(xs, ys, "black",zorder=1)

        # plot grid
        plt.plot(xs, ys, "black")
        X, Y = np.meshgrid(range(self.nCols + 1), range(self.nRows + 1))
        plt.plot(X, Y, 'k-')
        plt.plot(X.transpose(), Y.transpose(), 'k-')

    def addGridInfos(self):
        self.plotTemplate()  # plot template
        states = range(1, self.nStates + 1)
        iter = 0
        for i in range(self.nCols):
            for j in range(self.nRows, 0, -1):
                if iter + 1 in self.stateForbiddenIndexes:
                    plt.text(i + 0.5, j - 0.5, str(states[iter]) + " (F)", fontsize=20, horizontalalignment='center',
                             verticalalignment='center', color='white')
                elif iter + 1 in self.stateTerminalsIndexes:
                    plt.text(i + 0.5, j - 0.5, str(states[iter]) + " (T)", fontsize=20, horizontalalignment='center',
                             verticalalignment='center', color='black')
                elif iter + 1 in self.stateSpecialIndexes:
                    plt.text(i + 0.5, j - 0.5, str(states[iter]) + " (B)", fontsize=20, horizontalalignment='center',
                             verticalalignment='center', color='black')
                elif iter + 1 in self.stateStartIndex:
                    plt.text(i + 0.5, j - 0.5, str(states[iter]) + " (S)", fontsize=20, horizontalalignment='center',
                             verticalalignment='center', color='black')
                else:
                    plt.text(i + 0.5, j - 0.5, str(states[iter]), fontsize=20, horizontalalignment='center',
                             verticalalignment='center')
                iter += 1
        plt.axis("equal")
        plt.axis("off")

    def plotUtilities(self, utilities, type):
        plot1 = plt.figure(figsize=(8,8))
        self.plotTemplate()
        iter = 0
        for i in range(self.nCols):
            for j in range(self.nRows, 0, -1):
                if type == "mdp":
                    if iter + 1 not in self.stateForbiddenIndexes:
                        plt.text(i + 0.5, j - 0.5, str(round(utilities[iter], 4)), fontsize=17,
                                 horizontalalignment='center', verticalalignment='center')
                        plt.title('Markov Decision Problem. Utilities', size=16)
                elif type == "q":
                    if iter + 1 in self.stateForbiddenIndexes:
                        plt.text(i + 0.5, j - 0.5, str(round(utilities[iter], 4)), fontsize=17,
                                 horizontalalignment='center', verticalalignment='center', color='white')
                    else:
                        plt.text(i + 0.5, j - 0.5, str(round(utilities[iter], 4)), fontsize=17,
                                 horizontalalignment='center', verticalalignment='center')
                    plt.title('Q-learning. Utilities', size=16)

                iter += 1
        plt.axis("equal")
        plt.axis("off")
        return plt

    def plotUtilitiesActionText(self, utilities, policy):
        actions = ["^", "v", ">", "<"]
        actions_map = {v: k for k, v in zip(actions, [1, 3, 2, 4])}
        data = np.empty((self.nRows, self.nCols), dtype='object')
        iter = 0
        for i in range(self.nCols):
            for j in range(self.nRows):
                data[j][i] = str(round(utilities[iter],3)) + " " + str(actions_map[int(policy[iter])])
                iter +=1

        rows_names = np.zeros((self.nRows, 1))
        for i in range(self.nRows):
            rows_names[i][0] = str(i + 1)
        data = np.hstack((rows_names, data))
        columns_names = []
        for i in range(self.nCols):
            columns_names.append(str(i+1))
        table = tabulate(data, columns_names, "github", numalign="center")
        print(table)

    def plotPolicy(self, policy, type):
        plot2 = plt.figure(figsize=(6,6))    # plot in second window
        nActions = len(self.actions)
        policy = policy.reshape(self.nRows, self.nCols, order="F").reshape(-1, 1)
        X, Y = np.meshgrid(range(self.nCols + 1), range(self.nRows + 1))
        X1 = X[:-1, :-1]
        Y1 = Y[:-1, :-1]
        X2 = X1.reshape(-1, 1) + 0.5
        Y2 = np.flip(Y1.reshape(-1, 1)) + 0.5
        X2 = np.kron(np.ones((1, nActions)), X2)
        Y2 = np.kron(np.ones((1, nActions)), Y2)
        mat = np.cumsum(np.ones((self.nStates, nActions)), axis=1).astype("int64")
        if policy.shape[1] == 1:
            policy = (np.kron(np.ones((1, nActions)), policy) == mat)
        index_policy = [item - 1 for item in range(1, self.nStates + 1) if item not in (self.stateForbiddenIndexes + self.stateTerminalsIndexes)]
        mask = policy.astype("int64") * mat
        print(mask.shape)
        mask = mask.reshape(self.nRows, self.nCols, 4)
        X3 = X2.reshape(self.nRows, self.nCols, nActions)
        Y3 = Y2.reshape(self.nRows, self.nCols, nActions)
        alpha = np.pi - np.pi / 2 * mask
        self.plotTemplate()
        for ii in index_policy:
            j = int(ii / self.nRows)
            i = (ii + 1 - j * self.nRows) % self.nCols - 1
            index = np.where(mask[i, j] > 0)[0]
            h = plt.quiver(X3[i, j, index], Y3[i, j, index], np.cos(alpha[i, j, index]), np.sin(alpha[i, j, index]),1,
                           color='blue', zorder = 100)
        states = range(1, self.nStates + 1)
        k = 0
        # add state number in upper-left corner
        for i in range(self.nCols):
            for j in range(self.nRows, 0, -1):
                plt.text(i + 0.25, j - 0.25, str(states[k]), fontsize=16, horizontalalignment='right',
                         verticalalignment='bottom')
                k += 1
        plt.axis("equal")
        plt.axis("off")
        if type == "mdp":
            plt.title("Markov Decision Problem. Policy", size=16)
        elif type == "q":
            plt.title("Q-learning. Policy", size=16)
        return plt

    @staticmethod
    def savePolicyPlot(plot, filename, type):
        if type == "mdp":
            filename = filename + "_mdp_actions.png"
        elif type == 'q':
            filename = filename + "_q_actions.png"
        plot.savefig(filename, transparent=False)

    @staticmethod
    def saveUtilitiesPlot(plot, filename, type):
        if type == "mdp":
            filename = filename + "_mdp_utilities.png"
        elif type == 'q':
            filename = filename + "_q_utilities.png"
        plot.savefig(filename, transparent=False)

    @staticmethod
    def showPlots(self):
        plt.show()