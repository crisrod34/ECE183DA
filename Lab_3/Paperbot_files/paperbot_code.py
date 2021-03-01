# Simulation for Paperbot robot that uses two wheels of diameter 50mm separated by a distance of 90mm, both directly driven by a continuous rotation servo.
# The wheels drag a castor wheel for stability, that contacts the ground at a distance l = 75mm behind the front edge.
import math
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
# GLOBAL CONSTANTS
w = 90
d = 50
#dimension of simulation area
L = 1000
H = 1000
maxdist = math.sqrt(H*H + L*L)
phi = 0
# timestep
deltaT = 0.01
pi = math.pi
threshold_dz = 0.1
threshold_sat = 0.9
rpm_max = 14
# coordinates (i,j) of robot in space
i_0 = 5
j_0 = 5
theta_0 = 0
gyro_noise_density = 0.005
magneto_noise_density = 0.02
laser_noise_density = 20
loss = 1



# HELPER FUNCTIONS
def omega(d2):
    return(d2)
    # if (abs(d2) < threshold_dz):
    #     return 0
    # elif (d2 > threshold_sat):
    #     return threshold_sat * rpm_max
    # elif (d2 < -threshold_sat):
    #     return -threshold_sat * rpm_max
    # else:
    #     return rpm_max * d2


# NOISE from sensors
def getNoiseInput():
    return [noiseServo(), noiseServo()]


def noiseServo():
    return random.normal(0, 0)


def getNoiseOutput():
    return [noiseLaserFront(), noiseLaserRight(), noiseGyro(), noiseMagneto(), noiseMagneto()]


def noiseLaserFront():
    return random.normal(0, laser_noise_density)


def noiseLaserRight():
    return random.normal(0, laser_noise_density)


def noiseGyro():
    return random.normal(0, gyro_noise_density)


def noiseMagneto():
    return random.normal(0, magneto_noise_density)


# STATE EQUATIONS
# Continuous space

# i is the x-position of robot
def i_prime(x, u):
    temp = x[0] + loss*(omega(u[0]) + omega(u[1])) * d / 4 * math.cos(x[2]) * deltaT
    return temp

# y is the y-position of robot
def j_prime(x, u):
    temp = x[1] + loss*(omega(u[0]) + omega(u[1])) * d / 4 * math.sin(x[2]) * deltaT
    return temp


def theta_prime(x, u):
    a =(x[2] + loss*(omega(u[0]) - omega(u[1])) * (d/2) / w * deltaT)
    if(a > 3/2*pi):
      return a-2*pi
    elif(a<-pi/2):
      return a+2*pi      
    return a


def f(x, u, v):
    return [i_prime(x, [u[0] + v[0], u[1] + v[1]]), j_prime(x, [u[0] + v[0], u[1] + v[1]]),
            theta_prime(x, [u[0] + v[0], u[1] + v[1]]),omega_out(u)]


# OUTPUT EQN
# Front laser sensor reading
def l_f(x):
    dist = 0
    f=0
    if (L-x[0])*math.tan(x[2]) + x[1] >= 0 and (L-x[0])*math.tan(x[2]) + x[1] <= H and (x[2]<=pi/2 and x[2] >= -pi/2):     #WALL ON x = L
        dist = abs((L-x[0])/math.cos(x[2]))
        f=1
    elif (-x[0]*math.tan(x[2]) + x[1] >= 0 and (-x[0])*math.tan(x[2]) + x[1] <= H and (x[2] >= pi/2  and x[2] <= 3*pi/2)):     #WALL ON x = 0
        dist = abs(x[0]/math.cos(x[2]))
        f=2
    elif (x[2] == pi/2) or ((H-x[1])/math.tan(x[2]) + x[0] >= 0 and (H-x[1])/math.tan(x[2]) + x[0] <= L and (x[2] >= 0  and x[2] <= pi)):         #WALL ON y = H
        dist = abs((H-x[1])/math.sin(x[2]))
        f=3
    elif (x[2] == -pi/2) or (-x[1]/math.tan(x[2]) + x[0] >= 0 and -x[1]/math.tan(x[2]) + x[0] <= L and (x[2] >= pi  or x[2] <= 0)):             #WALL ON y = 0
        dist = abs(x[1]/math.sin(x[2]))
        f=4
    return dist

# Right laser sensor reading
def l_r(x):
    dist = 0
    if (L-x[0])*math.tan(x[2]-pi/2) + x[1] >= 0 and (L-x[0])*math.tan(x[2]-pi/2) + x[1] <= H and (x[2] >= 0  and x[2] <= pi):        #WALL ON x = L
        dist = abs((L-x[0])/math.cos(x[2]-pi/2))
    elif -x[0]*math.tan(x[2]-pi/2) + x[1] >= 0 and (-x[0])*math.tan(x[2]-pi/2) + x[1] <= H and (x[2] >= pi  or x[2] <= 0):           #WALL ON x = 0
        dist = abs(x[0]/math.cos(x[2]-pi/2))
    elif (H-x[1])/math.tan(x[2]-pi/2) + x[0] >= 0 and (H-x[1])/math.tan(x[2]-pi/2) + x[0] <= L and (x[2] >= pi/2  and x[2] <= 3*pi/2):    #WALL ON y = H
        dist = abs((H-x[1])/math.sin(x[2]-pi/2))
    elif -x[1]/math.tan(x[2]-pi/2) + x[0] >= 0 and -x[1]/math.tan(x[2]-pi/2) + x[0] <= L and (x[2] <= pi/2  and x[2] >= -pi/2):           #WALL ON y = 0
        dist = abs(x[1]/math.sin(x[2]-pi/2))
    return dist


def omega_out(u):
    return (omega(u[0]) - omega(u[1])) * d / w


def b1(x):
    return -math.cos(x[2] - phi)


def b2(x):
    return math.sin(x[2] - phi)


def h(x, u, v):
    return [l_f(x) + v[0], l_r(x) + v[1], omega_out(u) + v[2], b1(x) + v[3], b2(x) + v[4]]

  
def getError(webot,python):
  #maxIndex = 0
  maxdiff = 0
  totalError = 0
  for i in range(len(webot)):
    dif = abs((webot[i]-python[i])/max(abs(webot[i]),abs(python[i])))
    if dif > maxdiff:
      maxdiff = dif
    totalError = totalError + dif
  avgError = totalError/len(webot)
  return [avgError,maxdiff]

#Import from excel
def testFile(fileName, outputfile):
    data = pd.read_excel(fileName)
    wl = data.left_wheel
    wr = data.right_wheel
    x_sim = (data.x * 1000) + L/2
    y_sim = (data.z * 1000)  + H/2 
    time = data.time
    theta_sim = data.angle
    file_vel = data.ang_vel
    file_lidar_F = data. lidar_f * 10000/4096               
    file_lidar_R = data.lidar_r * 10000/4096        
    file_compass_Z = data.compass_x
    file_compass_X = data.compass_z
    file_gyro = data.gyro

    l_f_values = []
    l_r_values = []
    omega_values = []
    b_1_values = []
    b_2_values = []
    x = [x_sim[0], y_sim[0],theta_sim[0],0]
    path = []
    outputs = []
    global deltaT 
    deltaT = time[1] - time[0]
    for i in range(len(wl)):
        
        u = [wr[i],wl[i]]
        x = f(x,u,getNoiseInput())
        path.append(x)
        outputs.append(h(x, u, getNoiseOutput()))

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(outputfile)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 1, "lidar_f")
    worksheet.write(0, 2, "lidar_R")
    worksheet.write(0, 3, "gyro")
    worksheet.write(0, 4, "compass_x")
    worksheet.write(0, 5, "compass_z")
    worksheet.write(0, 6, "x")
    worksheet.write(0, 7, "z")
    worksheet.write(0, 8, "angle")
    worksheet.write(0, 9, "ang_vel")

    row = 1
    for l_f_val, l_r_val, omega_val, b_1_val, b_2_val in outputs:
        worksheet.write(row, 1, l_f_val)
        worksheet.write(row, 2, l_r_val)
        worksheet.write(row, 3, omega_val)
        worksheet.write(row, 4, b_1_val)
        worksheet.write(row, 5, b_2_val)

        worksheet.write(row, 6, path[row-1][0])
        worksheet.write(row, 7, path[row-1][1])
        worksheet.write(row, 8, path[row-1][2])
        worksheet.write(row, 9, path[row-1][3])
        row = row + 1

    workbook.close()

     #------------ERROR CALCULATION----------------
    path = list(np.array(path).T)
    outputs = list(np.array(outputs).T)


    trialName1 = fileName.replace('.xlsx', '') 
    outputName = "---------------" + trialName1 + " Error Calculations" + "---------------"
    print(outputName)

    max_xError = getError(x_sim, path[0])[1]
    print("Max X Error: ", end = "  ")
    print(max_xError)

    avg_xError = getError(x_sim, path[0])[0]
    print("Average X Error: ", end = "  ")
    print(avg_xError)

    max_yError = getError(y_sim, path[1])[1]
    print("Max Y Error: ", end = "  ")
    print(max_yError)

    avg_yError = getError(y_sim, path[1])[0]
    print("Average Y Error: ", end = "  ")
    print(avg_yError)

    max_angleError = getError(theta_sim, path[2])[1]
    print("Max Angle Error: ", end = "  ")
    print(max_angleError)

    avg_angleError = getError(theta_sim, path[2])[0]
    print("Average Angle Error: ", end = "  ")
    print(avg_angleError)

    max_angularVelError = getError(file_vel, path[3])[1]
    print("Max Angular Velocity Error: ", end = "  ")
    print(max_angularVelError)

    avg_angVelError = getError(file_vel, path[3])[0]
    print("Average Angular Velocity Error: ", end = "  ")
    print(avg_angVelError)

    #---------Sensors
    
    max_LidarFrontError = getError(file_lidar_F, outputs[0])[1]
    print("Max Front Lidar Error: ", end = "  ")
    print(max_LidarFrontError)

    avg_LidarFrontError = getError(file_lidar_F, outputs[0])[0]
    print("Average Front Lidar Error: ", end = "  ")
    print(avg_LidarFrontError)

    max_LidarRightError = getError(file_lidar_R, outputs[1])[1]
    print("Max Right Lidar Error: ", end = "  ")
    print(max_LidarRightError)

    avg_LidarRightError = getError(file_lidar_R, outputs[1])[0]
    print("Average Right Lidar Error: ", end = "  ")
    print(avg_LidarRightError)

    max_GyroError = getError(file_gyro, outputs[2])[1]
    print("Max Gyro Error: ", end = "  ")
    print(max_GyroError)

    avg_GyroError = getError(file_gyro, outputs[2])[0]
    print("Average Gyro Error: ", end = "  ")
    print(avg_GyroError)

    max_CompassXError = getError(file_compass_X, outputs[3])[1]
    print("Max Compass X Error: ", end = "  ")
    print(max_CompassXError)

    avg_CompassXError = getError(file_compass_X, outputs[3])[0]
    print("Average Compass X Error: ", end = "  ")
    print(avg_CompassXError)


    max_CompassZError = getError(file_compass_Z, outputs[4])[1]
    print("Max Compass Z Error: ", end = "  ")
    print(max_CompassZError)

    avg_CompassZError = getError(file_compass_Z, outputs[4])[0]
    print("Average Compass Z Error: ", end = "  ")
    print(avg_CompassZError)


    outputName2 = "---------------" + "End of " + trialName1 + " Error Calculations" + "---------------"
    print(outputName2)
    
    
    
    #------------------PLOTTING-----------------   
    
    
    # X VS TIME
    plt.plot(time, x_sim)
    plt.plot(time,path[0])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("X position (mm)")
    plt.title("X vs Time")
    trialName = fileName.replace('.xlsx', '') 
    figName = trialName + "_X_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # Y VS TIME
    plt.plot(time, y_sim)
    plt.plot(time,path[1])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Y position (mm)")
    plt.title("Y vs Time") 
    figName = trialName + "_Y_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # ANGLE VS TIME
    plt.plot(time, theta_sim)
    plt.plot(time,path[2])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Orientation (radians)")
    plt.title("Orientation vs Time")
    figName = trialName + "_Angle_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # ANG_VEL VS TIME
    plt.plot(time, file_vel)
    plt.plot(time,path[3])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.title("Angular Velocity vs Time")
    figName = trialName + "_AngVel_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # X VS Y
    plt.plot(x_sim, y_sim)
    plt.plot(path[0],path[1])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("X Position (mm)")
    plt.ylabel("Y Position (mm)")
    plt.title("X vs Y")
    figName = trialName + "_X_vs_Y.png"
    plt.savefig(figName)
    plt.close()
    
    
    #---------------SENSORS-----------#
    # lidar front VS TIME
    plt.plot(time, file_lidar_F)
    plt.plot(time,outputs[0])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Front Lidar Distance(mm)")
    plt.title("Distance to Front Wall vs Time")
    figName = trialName + "_LidarF_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # lidar right VS TIME
    plt.plot(time, file_lidar_R)
    plt.plot(time, outputs[1])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Right Lidar Distance (mm)")
    plt.title("Distance to Right Wall vs Time")
    figName = trialName + "_LidarR_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # GYRO VS TIME
    plt.plot(time, file_gyro)
    plt.plot(time, outputs[2])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.title("Gyroscope Y Axis vs Time")
    figName = trialName + "_Gyro_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # Compass X VS TIME
    plt.plot(time, file_compass_X)
    plt.plot(time,outputs[3])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Compass X (radians)")
    plt.title("Compass X vs Time")
    figName = trialName + "_CompassX_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    # Compass Z VS TIME
    plt.plot(time, file_compass_Z)
    plt.plot(time,outputs[4])
    plt.legend(["Webot", "Analytical"])
    plt.xlabel("Time (s)")
    plt.ylabel("Compass Z (radians)")
    plt.title("Compass Z vs Time")
    figName = trialName + "_CompassZ_vs_T.png"
    plt.savefig(figName)
    plt.close()
    
    
    



# SIMULATION
def simulatePath():
    x = [i_0, j_0, theta_0]
    x_noisy = [i_0, j_0, theta_0]
    correctPath_i = []
    correctPath_j = []
    correctPath_theta = []
    trials = 10000
    noisyPath_i = []
    noisyPath_j = []
    noisyPath_theta = []
    for i in range(trials):
        u = [300,100]  # [2*random.random()-1,2*random.random()-1]
        correctPath_i.append(x[0])
        correctPath_j.append(x[1])
        correctPath_theta.append(x[2])

        noisyPath_i.append(x_noisy[0])
        noisyPath_j.append(x_noisy[1])
        noisyPath_theta.append(x_noisy[2])

        x = f(x, u, [0, 0])
        x_noisy = f(x_noisy, u, getNoiseInput())

    plt.plot(correctPath_i,correctPath_j)
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

  

testFile("trial1.xlsx","output1.xlsx")
testFile("trial2.xlsx","output2.xlsx")
testFile("trial3.xlsx","output3.xlsx")
testFile("trial4.xlsx","output4.xlsx")

testFile("trial5.xlsx","output5.xlsx")
testFile("trial6.xlsx","output6.xlsx")
testFile("trial7.xlsx","output7.xlsx")
testFile("trial8.xlsx","output8.xlsx")

testFile("trial9.xlsx","output9.xlsx")
testFile("trial10.xlsx","output10.xlsx")
testFile("trial11.xlsx","output11.xlsx")
testFile("trial12.xlsx","output12.xlsx")







