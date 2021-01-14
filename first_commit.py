import numpy as np
import math
import random

# main function
# read in map, starting state, inputs, p_e
# from map read x_max, y_max, obstacles
# run function, returns outputs

# GLOBALS
p_e = 0.04  # probability of error
x_max = 5
y_max = 5
# ice cream shop locations
R_D = [2, 2]
R_S = [2, 0]
# initial state
state = [0, 0]


# Returns movement to be executed (if valid)
def getMovementWithError(input_):
    moves = ['L', 'R', 'U', 'D', 'S']
    p_s = 1 - p_e  # probability of success
    rand = random.random()
    if (input_ == 'L')
        if (rand <= p_s)
    return input_
    elif (rand > p_s & & rand <= (p_s + p_e / 4))
    return 'R'

elif (rand > (p_s + p_e / 4) & & rand <= (p_s + 2 * p_e / 4))
return 'D'
elif (rand > (p_s + 2 * p_e / 4) & & rand <= (p_s + 3 * p_e / 4)
return 'U'
elif (rand > (p_s + 3 * p_e / 4 & & rand <= 1)
return 'S'
elif (input_ == 'R')
if (rand <= p_s)
    return input_
elif (rand > p_s & & rand <= (p_s + p_e / 4))
return 'L'
elif (rand > (p_s + p_e / 4) & & rand <= (p_s + 2 * p_e / 4))
return 'D'
elif (rand > (p_s + 2 * p_e / 4) & & rand <= (p_s + 3 * p_e / 4)
return 'U'
elif (rand > (p_s + 3 * p_e / 4 & & rand <= 1)
return 'S'
elif (input_ == 'D')
if (rand <= p_s)
    return input_
elif (rand > p_s & & rand <= (p_s + p_e / 4))
return 'R'
elif (rand > (p_s + p_e / 4) & & rand <= (p_s + 2 * p_e / 4))
return 'L'
elif (rand > (p_s + 2 * p_e / 4) & & rand <= (p_s + 3 * p_e / 4)
return 'U'
elif (rand > (p_s + 3 * p_e / 4 & & rand <= 1)
return 'S'
elif (input_ == 'U')
if (rand <= p_s)
    return input_
elif (rand > p_s & & rand <= (p_s + p_e / 4))
return 'R'
elif (rand > (p_s + p_e / 4) & & rand <= (p_s + 2 * p_e / 4))
return 'D'
elif (rand > (p_s + 2 * p_e / 4) & & rand <= (p_s + 3 * p_e / 4)
return 'L'
elif (rand > (p_s + 3 * p_e / 4 & & rand <= 1)
return 'S'
if (input_ == 'S')
    return input_


# returns movement

# check if the resulting movement is allowable
def isValid(current_state):
    # check for edges
    if (current_state[0] >= x_max or current_state[1] >= y_max):
        return false

    # check for obstacles


for


# returns next state, output
def executeMovement(current_state, input_):
    ns = current_state;
    if (input_ == 'L')
        ns[0]


if (input_ == 'R')

if (input_ == 'D')

if (input_ == 'U')


# returns observation
def getOutput(R_S, R_D):
    # euclidian distance of ice cream shop location equation
    h = 2 / ((1 / (np.sqrt((state[0] - R_S[0]) ^ 2 + (state[1] - R_S[1]) ^ 2))) + (
                1 / (np.sqrt((state[0] - R_D[0]) ^ 2 + (state[1] - R_D[1]) ^ 2))))
    rand = random.random()

    if (rand <= (1 - (math.ceil(h) - h))):
        return (math.ceil(h))
    else:
        return (math.floor(h))


while 1:
    userInput = input("Where do you want to move")
    intendedAction = getIntendedMovement(userInput)
    state = executeMovement(state, intendedMovement)
    print(getOutput())