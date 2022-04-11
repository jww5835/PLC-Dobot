####################################################################################################################################
#
#   Imported Libraries
#
####################################################################################################################################

from turtle import Turtle
import pycomm3
from pycomm3 import LogixDriver
import cv2
import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
#from matplotlib import pyplot as plt
import threading
import DobotDllType as dType
# import imutils
import time
from tracker import *
import pandas as pd

#def Machine_Learning(rgb):
    

#    df = pd.read_excel("ml_csv.xlsx")
#    dft = pd.read_excel("ml_csv_test.xlsx")

#    x_train = df.iloc[:, :-1].values
#    y_train = df.iloc[:, 3].values

#    # Creating an array that works with the machine learning format
#    unknown_color = np.array(rgb).reshape(1,-1)  
#    # How many neighbors we are comparing to. This will vary our CV accuracy
#    classifier = KNeighborsClassifier(n_neighbors = 15)
#    print("RGB array in ML: ", unknown_color)
#    # Training our machine learning code
#    #X_train = [
#    #    [128, 0, 0],    # ***RED***
#    #    [139, 0, 0],
#    #    [165, 42, 42],
#    #    [178, 34, 34],
#    #    [220, 20, 60],
#    #    [255, 0, 0],
#    #    [255, 99, 71],
#    #    [255, 69, 0],   # ***RED***
#    #    [85, 107, 47],  # ***GREEN***
#    #    [107, 142, 35],
#    #    [124, 252, 0],
#    #    [127, 255, 0],
#    #    [0, 100, 0],
#    #    [0, 128, 0],
#    #    [34, 139, 34],
#    #    [0, 255, 0],    # ***GREEN***
#    #    [255, 255, 0],  # ***YELLOW***
#    #    [204, 204, 0],
#    #    [255, 255, 51],
#    #    [255, 255, 102],
#    #    [255, 255, 153],
#    #    [255, 255, 204],
#    #    [240, 240, 15],
#    #    [245, 249, 33], # ***YELLOW***
#    #    [0, 0, 255],    # ***BLUE***
#    #    [0, 0, 205],
#    #    [0, 0, 139],
#    #    [135, 206, 250],
#    #    [135, 206, 235],
#    #    [30, 144, 255],
#    #    [18, 48, 165],
#    #    [65, 105, 225]  # ***BLUE***
#    #    ]
#    # This allows us to label each RGB value above
#    #y_train = ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
#    # Combines and labels the data
#    classifier.fit(X_train, y_train)
#    # Predicts the true color based on the K value chosen above as well as Euclidean Distance
#    true_color = classifier.predict(unknown_color)
#    return true_color

####################################################################################################################################
#
#   Functions for Sorting Methods
#
####################################################################################################################################

def Random_Sort(count):
    print("Inside Random. Count: ", count)
    count = 5
    if count < 5:
        #dType.SetQueuedCmdClear(api
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, 150, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, -48 + count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        count += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, 0, 50, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api,0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        else:
            pass
    return count

def Same_Sort(color, rc, gc, bc, yc):
    if (color == 'Red') & (rc < 7):
        print("Gang2: inside function")
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 225, -48 + rc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        plc.write('Program:MainProgram.Block_Detected', 1)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        rc += 1
    elif (color == 'Green') & (gc < 7):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 225, -48 + gc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        gc += 1
    elif (color == 'Blue') & (bc < 7):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 225, -48 + bc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        bc += 1
    elif (color == 'Yellow') & (yc < 7):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 225, -48 + yc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        yc += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, -125, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
    if rc >= 7:
        print("Maxed Out Red")
    if gc >= 7:
        print("Maxed Out Green")
    if bc >= 7:
        print("Maxed Out Blue")
    if yc >= 7:
        print("Maxed Out Yellow")
    return rc, gc, bc, yc

def Array_Sort(CA, CA_Count, color):
    if CA[CA_Count] == color & CA_Count < 7:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, -48 + CA_Count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        CA_Count += 1
    elif CA[CA_Count] == color & 7 <= CA_Count < 14:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 200, -48 + (CA_Count-7)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        CA_Count += 1
    elif CA[CA_Count] == color & 14 <= CA_Count < 21:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 200, -48 + (CA_Count-14)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        CA_Count += 1
    elif CA[CA_Count] == color & 21 <= CA_Count < 28:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 200, -48 + (CA_Count-21)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        CA_Count += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, -125, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
    if CA_Count >= 28:
        print("Maxed Out")
    return CA_Count

def Manual_Sort(count, color, man_color):
    if man_color == color & count < 7:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 175, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 175, -48 + count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 175, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        count += 1
    elif man_color == color & 7 <= count < 14:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 175, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 175, -48 + (count-7)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 175, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        count += 1
    elif man_color == color & 14 <= count < 21:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 175, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 175, -48 + (count-14)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 175, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        count += 1
    elif man_color == color & 21 <= count < 28:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, -48 + (count-21)*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        count += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, -125, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
    if count >= 28:
        print("Maxed Out")
    return count


####################################################################################################################################
#
#   Dobot Connection and initial speed and home parameters
#
####################################################################################################################################

# Dobot connection status
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

# Connect Dobot
api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

# Setting Dobot speeds and home coordinates
dType.SetQueuedCmdClear(api)
dType.SetHOMEParams(api, 243.5, 1, 50, 50, isQueued = 1)
dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
dType.SetHOMECmd(api, temp=0, isQueued = 1)
dType.SetQueuedCmdStartExec(api)
time.sleep(24)

#df = pd.read_excel("ML_CSV.xlsx")
#dft = pd.read_excel("ML_CSV_TEST.xlsx")

#X_train = df.iloc[:, :-1].values
#y_train = df.iloc[:, 3].values

while True:
####################################################################################################################################
#
#   Read in all PLC Inputs for System Start
#
####################################################################################################################################

    with LogixDriver('192.168.222.51') as plc:                               
            PLC_SysRunning = plc.read('Program:MainProgram.System_Running')               
            PLC_Stop = plc.read('Program:MainProgram.Stop')                    
            PLC_EStop = plc.read('Program:MainProgram.ESTOP')
            PLC_Conveyor = plc.read('Program:MainProgram.Conv_Run')
            PLC_Color = plc.read('Program:MainProgram.Color')
            Sort_Color_Array = plc.read('Program:MainProgram.Color_Array')
            Sort_Random = plc.read('Program:MainProgram.Random')
            Sort_Manual = plc.read('Program:MainProgram.Manual')
            Manual_Color = plc.read('Program:MainProgram.Manual_Color')
            Sort_Same = plc.read('Program:MainProgram.Same')
            Sort_Array = plc.read('Program:MainProgram.Array')
            PLC_Conveyor_Speed = plc.read('Program:MainProgram.Conv_Speed')
            plc.write('Program:MainProgram.Block_Detected', 0)

            # Initalize counter blocks
            Block_Count = 0
            break_shape = 0
            start = 1
            Block_Color = 'NULL'
            red_count = 0
            green_count = 0
            blue_count = 0
            yellow_count = 0
            Array_Count = 0

####################################################################################################################################
#
#   Start of the System Depending on PLC input
#
####################################################################################################################################
           
            while PLC_SysRunning[1] == 1:
                print("System is Running.")
                # Reread PLC Inputs for Updates
                plc.write('Program:MainProgram.Block_Detected', 0)
                PLC_SysRunning = plc.read('Program:MainProgram.System_Running')               
                PLC_Stop = plc.read('Program:MainProgram.Stop')                    
                PLC_EStop = plc.read('Program:MainProgram.ESTOP')
                PLC_Conveyor = plc.read('Program:MainProgram.Conv_Run')
                PLC_Color = plc.read('Program:MainProgram.Color')
                Sort_Color_Array = plc.read('Program:MainProgram.Color_Array')
                Sort_Random = plc.read('Program:MainProgram.Random')
                Sort_Manual = plc.read('Program:MainProgram.Manual')
                Manual_Color = plc.read('Program:MainProgram.Manual_Color')
                Sort_Same = plc.read('Program:MainProgram.Same')
                Sort_Array = plc.read('Program:MainProgram.Array')
                PLC_Conveyor_Speed = plc.read('Program:MainProgram.Conv_Speed')
                #plc.write('Program:MainProgram.Block_Detected', 0)


        
                if PLC_EStop[1] == 1:
                    dType.SetQueuedCmdForceStopExec(api)

####################################################################################################################################
#
#   Conveyor start and stop depending on PLC inputs
#
####################################################################################################################################

                if PLC_Conveyor[1] == 1:
                   # dType.SetQueuedCmdClear(api)
                    dType.SetEMotor(api, 1, 1, -(PLC_Conveyor_Speed[1]), isQueued = 0)
                   # dType.SetQueuedCmdStartExec(api)

####################################################################################################################################
#
#   Start of the Computer Vision While loop
#
####################################################################################################################################
                while break_shape == 0:
                    if start == 1:
                        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        start = 0
                    x = -1
                    y = 0
                    _, frame = cap.read()
                    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    #Define Red Array
                    low_red = np.array([160,50,50])
   
                    high_red = np.array([180,255,255])
   
                    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
   
                    red = cv2.bitwise_and(frame, frame, mask=red_mask)

                    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    #Define Green Array
                    low_green = np.array([50,100,100])
   
                    high_green = np.array([70,255,255])
   
                    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
   
                    green = cv2.bitwise_and(frame, frame, mask=green_mask)

                    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
                    #Define Blue Array
                    low_blue = np.array([100,150,0])

                    high_blue = np.array([140,255,255])
   
                    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
   
                    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

                    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    #Define Yellow Array
                    low_yellow = np.array([10,100,100])
   
                    high_yellow = np.array([30,255,255])
   
                    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
   
                    yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

                    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


                    for cnt in red_contours:
                        # Calculate area and remove small elements
                        area = cv2.contourArea(cnt)

                        if area > 12000:
                            x, y, w, h = cv2.boundingRect(cnt)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            x = int(x + w/2)
                            y = int(y + h/2)
                            Block_Color = 'Red'
            

                    for cnt in green_contours:
                        # Calculate area and remove small elements
                        area = cv2.contourArea(cnt)

                        if area > 12000:
                            x, y, w, h = cv2.boundingRect(cnt)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            x = int(x + w/2)
                            y = int(y + h/2)
                            Block_Color = 'Green'
            

                    for cnt in blue_contours:
                        # Calculate area and remove small elements
                        area = cv2.contourArea(cnt)

                        if area > 12000:
                            x, y, w, h = cv2.boundingRect(cnt)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                            x = int(x + w/2)
                            y = int(y + h/2)
                            Block_Color = 'Blue'

                    for cnt in yellow_contours:
                        # Calculate area and remove small elements
                        area = cv2.contourArea(cnt)

                        if area > 10000:
                            x, y, w, h = cv2.boundingRect(cnt)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
                            x = int(x + w/2)
                            y = int(y + h/2)
                            Block_Color = 'Yellow'

                    if y > 220:
                        print(x,y)
                        plc.write('Program:MainProgram.Block_Detected', 1)
                        #Might not need conveyor dType Syntax
                        dType.SetQueuedCmdClear(api)
                        dType.SetEMotor(api, 1, 0, 0, isQueued = 0) 
                        ##dType.SetQueuedCmdStartExec(api)
                        
                        #Might not need rgb code due to ML Pull
                        #x1 = x
                        #if x1 > 480:
                        #    x1 = 479
                        #bgr = frame[x1,y]
                        #rgb = bgr[::-1]
                        #print(rgb)
                
                        if 0 < x < 150:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4 + 220
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                        elif 150 < x < 240:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.15 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                        elif 240 < x < 300:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.42 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                        elif 300 < x < 350:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.75 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                        elif 350 < x < 405:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/5 + 215
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                        elif x > 405:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/5.2 + 215
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            dType.dSleep(1000)
                            if PLC_Stop[1] == 1:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                            break_shape = 1
                            #plc.write('Program:MainProgram.Block_Detected', 0)
                 
                        #if break_shape == 1:
                        #    start = 1
                        #    break
                break_shape = 0
                start = 1
                ### 3.) Machine Learning uses the pulled RGB value to detect the color of the block
                        #rgb = [192, 24, 100]
                #if len(rgb) == 0:
                #    pass
                #else:
                #    color = Machine_Learning(rgb)
                ### 4.) Keeping track of the blocks counted to account for sorting purposes
                print(Block_Color)
        
####################################################################################################################################
#
#   Sorting method executed based on PLC
#
####################################################################################################################################
                #print("Sort Manual: " + string(Sort_Manual[1]))
                #print("Sort Same: " + Sort_Same[1])
                #print("Sort Array: " + Sort_Array[1])
                #print("Sort Random: " + Sort_Random[1])
                if Sort_Manual[1] == 1:
                    Manual_Count = Manual_Sort(Manual_Count, Block_Color, Manual_Color)
                elif Sort_Same[1] == 1:
                    red_count, green_count, blue_count, yellow_count = Same_Sort(Block_Color, red_count, green_count, blue_count, yellow_count)
                elif Sort_Array[1] == 1:
                    Array_Count = Array_Sort(PLC_Color_Array,Array_Count,Block_Color)
                else:
                   Block_Count = Random_Sort(Block_Count)
