import numpy as np
import math
import random

# main function
# read in map, starting state, inputs, p_e
# from map read x_max, y_max, obstacles
# run function, returns outputs

# GLOBALS
p_e = 0.04  # probability of error
x_max = 5  # bounds of map
y_max = 5
R_D = [2, 2]  # ice cream shop locations
R_S = [2, 0]
obstacles = [[1, 1], [2, 1], [1, 3], [2, 3]]  # obstacles
action_space = ['L', 'R', 'U', 'D', 'S']


# Returns movement to be executed adjusted for error
def getActionWithError(input_):
    rand = random.random()
    p_s = 1 - p_e  # probability of success
    if input_ == 'S' or rand <= p_s:
        return input_
    tmp = [x for x in action_space if x != input_]
    return random.choice(tmp)
# returns movement

# check if the resulting movement is allowable
def isValid(current_state):
    # check for edges
    if current_state[0] >= x_max or current_state[1] >= y_max or current_state[0] < 0 or current_state[1] < 0:
        print("Out of bounds")
        return False

    # check for obstacles
    if current_state in obstacles:
        print("Hit an obstacle")
        return False

    # if you get here it is valid
    return True


#	returns next state, output
def executeMovement(current_state, input_):
    ns = current_state.copy()
    if input_ == 'L':
        ns[0] -= 1
    elif input_ == 'R':
        ns[0] += 1
    elif input_ == 'D':
        ns[1] -= 1
    elif input_ == 'U':
        ns[1] += 1
    if isValid(ns):
        return ns
    else:
        return current_state


# returns observation
# TODO: incorporate the rounding
def getOutput():

    # need to make sure we aren't dividing by zero
    if state == R_S:
        inverse_d_S = 0
    else:
        # python handles ^2 differently than **2
        inverse_d_S = 1 / (np.sqrt((state[0] - R_S[0]) ** 2 + (state[1] - R_S[1]) ** 2))

    if state == R_D:
        inverse_d_D = 0
    else:
        inverse_d_D = 1 / (np.sqrt((state[0] - R_D[0]) ** 2 + (state[1] - R_D[1]) ** 2))

    h = 2 / (inverse_d_S + inverse_d_D)

    o = 0
    rand = random.random()
    if (rand <= 1 - (math.ceil(h) - h)):
        o = math.ceil(h)
    else:
        o = math.floor(h)

    return o


state = [0, 0]
while 1:
    userInput = input("Where you want to move")
    intendedAction = getActionWithError(userInput)
    state = executeMovement(state, intendedAction)
    print(state)
    print(getOutput())
