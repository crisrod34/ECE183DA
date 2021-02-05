import math
from numpy import random
import matplotlib.pyplot as plt

# GLOBAL CONSTANTS
w = 2
d = 1
L = 10
H = 10
phi = 0
deltaT = 0.1
pi = math.pi
threshold_dz = 0.1
threshold_sat = 0.9
rpm_max = 14
i_0 = 5
j_0 = 5
theta_0 = 0
gyro_noise_density = 0.005
magneto_noise_density = 0.02


# HELPER FUNCTIONS
def omega(d2):
    if (abs(d2) < threshold_dz):
        return 0
    elif (d2 > threshold_sat):
        return threshold_sat * rpm_max
    elif (d2 < -threshold_sat):
        return -threshold_sat * rpm_max
    else:
        return rpm_max * d2


def getNoiseInput():
    return [noiseServo(), noiseServo()]


def noiseServo():
    return random.normal(0, 0.001)


def getNoiseOutput(x, u):
    return [noiseLaserFront(x, u), noiseLaserRight(x, u), noiseGyro(), noiseMagneto(), noiseMagneto()]


def noiseLaserFront(x, u):
    return random.normal(0, l_f(x) * 0.01)


def noiseLaserRight(x, u):
    return random.normal(0, l_r(x) * 0.01)


def noiseGyro():
    return random.normal(0, 1 / 60 * gyro_noise_density)


def noiseMagneto():
    return random.normal(0, 1 / 60 * magneto_noise_density)


# STATE EQN
def i_prime(x, u):
    temp = x[0] + (omega(u[0]) + omega(u[1])) * d / 4 * math.cos(x[2]) * deltaT
    if (temp > L):
        return L
    elif (temp < 0):
        return 0
    else:
        return temp


def j_prime(x, u):
    temp = x[1] + (omega(u[0]) + omega(u[1])) * d / 4 * math.sin(x[2]) * deltaT
    if (temp > H):
        return H
    elif (temp < 0):
        return 0
    else:
        return temp


def theta_prime(x, u):
    return (x[2] + (omega(u[0]) - omega(u[1])) * d / w * deltaT) % (2 * pi)


def f(x, u, v):
    return [i_prime(x, [u[0] + v[0], u[1] + v[1]]), j_prime(x, [u[0] + v[0], u[1] + v[1]]),
            theta_prime(x, [u[0] + v[0], u[1] + v[1]])]


# OUTPUT EQN
def l_f(x):
    if (L-x[0])*math.tan(x[2]) + x[1] >= 0 and (L-x[0])*math.tan(x[2]) + x[1] <= H and (x[2] >= 3*pi/2  or x[2] <= pi/2):     #WALL ON x = L
        return abs((L-x[0])/math.cos(x[2]))
    elif -x[0]*math.tan(x[2]) + x[1] >= 0 and (L-x[0])*math.tan(x[2]) + x[1] <= H and (x[2] >= pi/2  and x[2] <= 3*pi/2):     #WALL ON x = 0
        return abs(x[0]/math.cos(x[2]))
    elif (H-x[1])/math.tan(x[2]) + x[0] >= 0 and (H-x[1])/math.tan(x[2]) + x[0] <= L and (x[2] >= 0  and x[2] <= pi):         #WALL ON y = H
        return abs((H-x[1])/math.sin(x[2]))
    elif -x[1]/math.tan(x[2]) + x[0] >= 0 and -x[1]/math.tan(x[2]) + x[0] <= L and (x[2] >= 0  and x[2] <= 2*pi):             #WALL ON y = 0
        return abs(x[1]/math.sin(x[2]))
    print("none")

def l_r(x):
    if (L-x[0])*math.tan(x[2]-pi/2) + x[1] >= 0 and (L-x[0])*math.tan(x[2]-pi/2) + x[1] <= H and (x[2] >= 0  and x[2] <= pi):        #WALL ON x = L
        return abs((L-x[0])/math.cos(x[2]-pi/2))
    elif -x[0]*math.tan(x[2]-pi/2) + x[1] >= 0 and (L-x[0])*math.tan(x[2]-pi/2) + x[1] <= H and (x[2] >= pi  and x[2] <= 2*pi):           #WALL ON x = 0
        return abs(x[0]/math.cos(x[2]-pi/2))
    elif (H-x[1])/math.tan(x[2]-pi/2) + x[0] >= 0 and (H-x[1])/math.tan(x[2]-pi/2) + x[0] <= L and (x[2] >= pi/2  and x[2] <= 3*pi/2):    #WALL ON y = H
        return abs((H-x[1])/math.sin(x[2]-pi/2))
    elif -x[1]/math.tan(x[2]-pi/2) + x[0] >= 0 and -x[1]/math.tan(x[2]-pi/2) + x[0] <= L and (x[2] >= 3*pi/2  or x[2] <= pi/2):           #WALL ON y = 0
        return abs(x[1]/math.sin(x[2]-pi/2))
    print("none")

def omega_out(u):
    return (omega(u[0]) - omega(u[1])) * d / w


def b1(x):
    return math.cos(x[2] - phi)


def b2(x):
    return math.sin(x[2] - phi)


def h(x, u, v):
    return [l_f(x) + v[0], l_r(x) + v[1], omega_out(u) + v[2], b1(x) + v[3], b2(x) + v[4]]


# SIMULATION
def simulatePath():
    x = [i_0, j_0, theta_0]
    x_noisy = [i_0, j_0, theta_0]
    correctPath_i = []
    correctPath_j = []
    correctPath_theta = []
    trials = 100
    noisyPath_i = []
    noisyPath_j = []
    noisyPath_theta = []
    for i in range(trials):
        u = [0.5, 0.1]  # [2*random.random()-1,2*random.random()-1]
        correctPath_i.append(x[0])
        correctPath_j.append(x[1])
        correctPath_theta.append(x[2])

        noisyPath_i.append(x_noisy[0])
        noisyPath_j.append(x_noisy[1])
        noisyPath_theta.append(x_noisy[2])

        x = f(x, u, [0, 0])
        x_noisy = f(x_noisy, u, getNoiseInput())

    u_vector = [math.cos(correctPath_theta[i]) for i in range(trials)]
    v_vector = [math.sin(correctPath_theta[i]) for i in range(trials)]

    u_vector_noisy = [math.cos(noisyPath_theta[i]) for i in range(trials)]
    v_vector_noisy = [math.sin(noisyPath_theta[i]) for i in range(trials)]

    plt.quiver(correctPath_i,correctPath_j,u_vector,v_vector,width=0.02,scale=1, units="xy",color = "b")
    #plt.plot(correctPath_i,correctPath_j,linewidth=0.4)
  
    plt.quiver(noisyPath_i,noisyPath_j,u_vector,v_vector,width=0.01,scale=4, units="xy", color = "r")
    plt.plot(noisyPath_i,noisyPath_j, "r--",linewidth=0.2)

    plt.xlim(0, L)
    plt.ylim(0, H)
    plt.xlabel("X Direction")
    plt.ylabel("Y Direction")
    plt.title("Trajectory of Robot over " + str(trials) + " Simulations")
    plt.legend(['Noisy Path', 'Ideal Path'])
    plt.show()





# Helper function to truncate values in plot
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def simulateOutputs():
    x = [random.random() * L, random.random() * H, random.random() * 2 * pi]
    trials = 1000
    l_f_values = []
    l_r_values = []
    omega_values = []
    b_1_values = []
    b_2_values = []
    u = [0.5, 0.1]
    for i in range(trials):
        l_f_val, l_r_val, omega_val, b_1_val, b_2_val = h(x, u, getNoiseOutput(x, u))
        l_f_values.append(l_f_val)
        l_r_values.append(l_r_val)
        omega_values.append(omega_val)
        b_1_values.append(b_1_val)
        b_2_values.append(b_2_val)

    # PLOTTING
    n_bins = 50
    fig, (plots) = plt.subplots(3, 2)
    plots[0, 0].quiver(x[0], x[1], math.cos(x[2]), math.sin(x[2]),width=0.2,scale=0.5, units="xy",color = "b")  # testing point
    plots[0, 0].legend(['Testing Point'])
    for i in range(len(x)):
        x[i] = truncate(x[i], 2)
    plots[0, 0].text(x=0.1, y=0.2,s='Testing State: ' + str(x))
    for i in range(len(u)):
        u[i] = truncate(u[i], 2)
    plots[0, 0].text(x=0.1, y=1.2, s='Input: ' + str(u))
    plots[0, 0].set_title("Testing State")
    plots[0, 0].set_xlabel("X Direction")
    plots[0, 0].set_ylabel("Y Direction")
    plots[0, 0].set_xlim(0, 10)
    plots[0, 0].set_ylim(0, 10)
    plots[0, 1].hist(x=l_f_values, bins=n_bins)
    plots[0, 1].set_title("Output Values of L_f for " + str(trials) + " simulations")
    plots[0, 1].set_xlabel("Simulated Output Value of L_f")
    plots[0, 1].set_ylabel("Occurrences")
    plots[1, 0].hist(x=l_r_values, bins=n_bins)
    plots[1, 0].set_xlabel("Simulated Output Value of L_r")
    plots[1, 0].set_ylabel("Occurrences")
    plots[1, 0].set_title("Output Values of L_r for " + str(trials) + " simulations")
    plots[1, 1].hist(x=omega_values, bins=n_bins)
    plots[1, 1].set_xlabel("Simulated Output Value of \u03C9")
    plots[1, 1].set_ylabel("Occurrences")
    plots[1, 1].set_title("Output Values of \u03C9 for " + str(trials) + " simulations")
    plots[2, 0].hist(x=b_1_values, bins=n_bins)
    plots[2, 0].set_xlabel("Simulated Output Value of b_1")
    plots[2, 0].set_ylabel("Occurrences")
    plots[2, 0].set_title("Output Values of b_1 for " + str(trials) + " simulations")
    plots[2, 1].hist(x=b_2_values, bins=n_bins)
    plots[2, 1].set_xlabel("Simulated Output Value of b_2")
    plots[2, 1].set_ylabel("Occurrences")
    plots[2, 1].set_title("Output Values of b_2 for " + str(trials) + " simulations")
    plt.tight_layout()
    plt.show()

  
  
simulatePath()
simulateOutputs()










