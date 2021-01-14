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
obstacles = np.array([[1, 1], [2, 1], [1, 3], [2, 3]])  # obstacles
action_space = ['L', 'R', 'U', 'D', 'S']


# Returns movement to be executed adjusted for error
def getActionWithError(input_):
    rand = random.random()
    p_s = 1 - p_e  # probability of success
    if (input_ == 'S' or rand <= p_s):
        return input_
    tmp = [x for x in action_space if x != input_]
    return random.choice(tmp)


# returns movement

# check if the resulting movement is allowable
def isValid(current_state):
    # check for edges
    if (current_state[0] >= x_max or current_state[1] >= y_max or current_state[0] < 0 or current_state[1] < 0):
        return False

    # check for obstacles


for ob in obstacles:
    if (current_state == ob):
        return False

    # if you get here it is valid
return True


#	returns next state, output
def executeMovement(current_state, input_):
    ns = current_state;
    if (input_ == 'L'):
        ns[0] -= 1

else if (input_ == 'R'):
    ns[0] += 1
else if (input_ == 'D'):
    ns[1] -= 1
else if (input_ == 'U'):
    ns[1] += 1
if (isValid(ns)):
    return ns
else:
    return current_state


# returns observation
# TODO: incirporate the rounding
def getOutput():
    h = 2 / ((1 / (np.sqrt((state[0] - R_S[0]) ^ 2 + (state[1] - R_S[1]) ^ 2))) + (
                1 / (np.sqrt((state[0] - R_D[0]) ^ 2 + (state[1] - R_D[1]) ^ 2))))
    return h


state = [0, 0]
while 1:
    userInput = input("Where you want to move")
    intendedAction = getIntendedMovement(userInput)
    state = executeMovement(state, intendedMovement)
    print(state)
    print(getOutput())
