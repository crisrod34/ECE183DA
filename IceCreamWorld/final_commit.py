import numpy as np
import math
import random
import matplotlib.pyplot as plt

# main function
# read in map, starting state, inputs, p_e
# from map read x_max, y_max, obstacles
# run function, returns outputs

# GLOBALS
p_e = 0.20  # probability of error
x_max = 5  # bounds of map
y_max = 5
o_max = math.ceil(np.sqrt(x_max ** 2 + y_max ** 2))

R_D = [2, 2]  # ice cream shop locations
R_S = [2, 0]
obstacles = [[1, 1], [2, 1], [1, 3], [2, 3]]  # obstacles

# ---------------------
# Things the simulation can access

action_space = ['L', 'R', 'U', 'D', 'S']
actionToMove = [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]
state_space = [[x, y] for x in range(x_max) for y in range(y_max)]
observation_space = [x for x in range(math.ceil(np.sqrt(x_max ** 2 + y_max ** 2)))]


# check if the resulting movement is allowable
def isValid(current_state):
    # check for edges
    if current_state[0] >= x_max or current_state[1] >= y_max or current_state[0] < 0 or current_state[1] < 0:
        # print("bound")
        return False

    # check for obstacles
    if current_state in obstacles:
        # print("obstacle")
        return False

    # if you get here it is valid
    return True


def checkBounds(current_state):
    count = 0
    if not isValid([current_state[0] - 1, current_state[1]]):
        count = count + 1
    if not isValid([current_state[0] + 1, current_state[1]]):
        count = count + 1
    if not isValid([current_state[0], current_state[1] + 1]):
        count = count + 1
    if not isValid([current_state[0], current_state[1] - 1]):
        count = count + 1
    return count


def P(nextState, currentState, action):
    if not isValid(nextState):
        return 0
    if action == 'S' and nextState == 'currentState':
        return 1
    elif action == 'S':
        return 0

    movement = np.subtract(nextState, currentState)
    if (abs(movement[0]) > 1 or abs(movement[1]) > 1 or (movement[0] != 0 and movement[1] != 0)):
        return 0

    index = action_space.index(action)
    if (nextState[0] == currentState[0] and nextState[1] == currentState[1]):
        expectedMove = [currentState[0] + actionToMove[index][0], currentState[1] + actionToMove[index][1]]
        temp = 0
        if not isValid(expectedMove):
            temp = 1 - p_e
        return p_e / 4 * (1 + checkBounds(currentState)) + temp

    if (movement[0] == actionToMove[index][0] and movement[1] == actionToMove[index][1]):
        return 1 - p_e
    else:
        return p_e / 4


# returns observatio
def O(observation, state):
    if state == R_S:
        inverse_d_S = 0
    else:
        inverse_d_S = 1 / (np.sqrt((state[0] - R_S[0]) ** 2 + (state[1] - R_S[1]) ** 2))
    if state == R_D:
        inverse_d_D = 0
    else:
        inverse_d_D = 1 / (np.sqrt((state[0] - R_D[0]) ** 2 + (state[1] - R_D[1]) ** 2))
    h = 2 / (inverse_d_S + inverse_d_D)

    prob = math.ceil(h) - h
    if (observation == math.ceil(h)):
        return 1 - prob
    elif observation == math.floor(h):
        return prob
    else:
        return 0


# --------------------------


# ---------------------
# The simulation
def getOutput(currentState):
    total = 0
    x = random.random()
    for item in observation_space:
        prob = O(item, currentState)
        if prob != 0:
            total += prob
            if total >= x:  # using cdf: if total passes the randomly generated value, then return for that specific item value- this is the next state
                return item
    raise Exception("O doesn't add up to 1, instead ", total)


def getNextState(action, currentState):
    total = 0
    x = random.random()
    for item in state_space:
        prob = P(item, currentState, action)
        if prob != 0:
            total += prob
            if total >= x:  # using cdf: if total passes the randomly generated value, then return for that specific item value- this is the next state
                return item
    raise Exception("P doesn't add up to 1, instead ", total)


def runSimulation():
    state = [0, 0]
    while 1:
        userInput = input("Where you want to move: ")

        state = getNextState(userInput, state)
        output = O(state)
        # return [state,output]
        print(state)
        print(output)


def runPath():
    state = [0, 0]
    userInput = "RRRURUULDL"
    expectedPathX = [0, 1, 2, 3, 3, 4, 4, 4, 3, 3, 2]
    expectedPathY = [0, 0, 0, 0, 1, 1, 2, 3, 3, 2, 2]
    actualStateX = [0]
    actualStateY = [0]

    for x in userInput:
        state = getNextState(x, state)
        actualStateX.append(state[0])
        actualStateY.append(state[1])

    fig = plt.figure(1)
    plt.xlim(0, 4)
    plt.ylim(0, 4)
    plt.plot(expectedPathX, expectedPathY, 'b', actualStateX, actualStateY, 'g')
    plt.show()


def testMovement():
    state = [3, 2]
    trials = 10000
    movement = 'R'
    transitions = dict()
    for i in range(trials):
        result = tuple(np.subtract(getNextState(movement, state), state))
        direction = action_space[actionToMove.index(result)]
        if (direction in transitions):
            transitions[direction] = transitions[direction] + 1
        else:
            transitions[direction] = 1
    fig = plt.figure(1)
    x = list(transitions.keys())
    y = list(transitions.values())
    plt.bar(x, y)
    for index, value in enumerate(x):
        plt.text(value, y[index], y[index])
    # fig.savefig("histogram.png")
    plt.show()


def testOutput():
    state = [3, 2]

    inverse_d_S = 1 / (np.sqrt((state[0] - R_S[0]) ** 2 + (state[1] - R_S[1]) ** 2))
    inverse_d_D = 1 / (np.sqrt((state[0] - R_D[0]) ** 2 + (state[1] - R_D[1]) ** 2))
    h = 2 / (inverse_d_S + inverse_d_D)
    prob = math.ceil(h) - h
    trials = 1000
    outputs = dict()
    for i in range(trials):
        result = getOutput(state)
        if (result in outputs):
            outputs[result] = outputs[result] + 1
        else:
            outputs[result] = 1
    x = list(outputs.keys())
    y = list(outputs.values())
    plt.bar(x, y)
    for index, value in enumerate(x):
        plt.text(value, y[index], y[index])
    plt.text(1, 0, prob)
    # fig.savefig("histogram.png")
    plt.show()


runPath()
testMovement()
testOutput()

