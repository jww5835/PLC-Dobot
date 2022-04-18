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

####################################################################################################################################
#
#   Functions for Sorting Methods and PLC tag Reading
#
####################################################################################################################################

def Random_Sort(count):
    print("Inside Random. Count: ", count)
    if count < 5:
        dType.SetQueuedCmdClear(api
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, 150, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, -48 + count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 250, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
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
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        else:
            pass
    return count

def Same_Sort(color, rc, gc, bc, yc):
    if (color == 'Red') & (rc < 5):
        print("Gang2: inside function")
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api,1, 150, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 200, -48 + rc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetQueuedCmdStartExec(api)
        plc.write('Program:MainProgram.Block_Detected', 1)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        rc += 1
    elif (color == 'Green') & (gc < 5):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 90, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 90, 225, -48 + gc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 90, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetPTPCmd(api, 1, 75, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 200, -48 + gc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 200, 150, 50, isQueued = 1)#lifts straight up
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
        gc += 1
    elif (color == 'Blue') & (bc < 5):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 130, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 130, 225, -48 + bc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 130, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetPTPCmd(api, 1, 100, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 200, -48 + bc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api,0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.dSleep(3000)
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
        bc += 1
    elif (color == 'Yellow') & (yc < 5):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 170, 225, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 170, 225, -48 + yc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 170, 225, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetPTPCmd(api, 1, 75, 250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 250, -48 + yc*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 75, 250, 150, 50, isQueued = 1)#lifts straight up
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
        yc += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, 0, 50, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
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
    if (CA[CA_Count] == color) & (CA_Count < 5):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, -48 + CA_Count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, 200, 150, 50, isQueued = 1)#lifts straight up
        dType.dSleep(2000)
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        CA_Count += 1
    else:
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
    return CA_Count

def Manual_Sort(count, color, man_color):

    print(color)
    print(man_color)
    print(count)
    if (man_color == color) & (count < 5):
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, -48 + count*25, 50, isQueued = 1)#Drops Block off
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 125, 175, 150, 50, isQueued = 1)#lifts straight up
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
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 150, -250, 100, 50, isQueued = 1)#Goes over drop off location
        dType.dSleep(2000)
        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)#Suction off
        dType.SetPTPCmd(api, 0, 243.5, 1, 50, 50, isQueued = 1)#Goes back to home
        dType.SetQueuedCmdStartExec(api)
        if PLC_EStop[1] == 1:
            dType.SetQueuedCmdForceStopExec(api)
        elif PLC_Stop[1] == 1:
            dType.SetQueuedCmdStopExec(api)
        else:
            pass
    if count >= 5:
        print("Maxed Out")
    return count

def PLC_Read():
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
            Manual_Color = plc.read('Program:MainProgram.Color')
            Sort_Same = plc.read('Program:MainProgram.Same')
            Sort_Array = plc.read('Program:MainProgram.Array')
            PLC_Conveyor_Speed = plc.read('Program:MainProgram.Conv_Speed')
            return PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed


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
time.sleep(23)

while True:
####################################################################################################################################
#
#   Read in all PLC Inputs for System Start
#
####################################################################################################################################
    with LogixDriver('192.168.222.51') as plc:                               
            plc.write('Program:MainProgram.Block_Detected', 0)
            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
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
            Manual_Count = 0
            Chosen_Color = ''

####################################################################################################################################
#
#   Start of the System Depending on PLC input
#
####################################################################################################################################
           
            while PLC_SysRunning[1] == 1:
                print("System is Running.")
                # Reread PLC Inputs for Updates
                plc.write('Program:MainProgram.Block_Detected', 0)
                PLC_Read()
                PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                if PLC_EStop[1] == 1:
                    dType.SetQueuedCmdForceStopExec(api)

####################################################################################################################################
#
#   Conveyor start and stop depending on PLC inputs
#
####################################################################################################################################
                PLC_Read()
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

                    PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                    if PLC_SysRunning[1] == 0:
                        dType.SetEMotor(api, 1, 0, 0, isQueued = 0)
                    else:
                        dType.SetEMotor(api, 1, 1, -(PLC_Conveyor_Speed[1]), isQueued = 0)



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
                        PLC_Read()
                        if PLC_Conveyor[1] == 1:
                            dType.SetEMotor(api, 1, 0, 0, isQueued = 0) 
                        #Might not need conveyor dType Syntax
                        dType.SetQueuedCmdClear(api)
                        PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                        if PLC_Conveyor[1] == 0:
                            dType.SetEMotor(api, 1, 0, 0, isQueued = 0) 
                        ##dType.SetQueuedCmdStartExec(api)
                
                        if 0 < x < 150:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4 + 220
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            PLC_Read()
                            if PLC_Stop[1] == 1:
                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                        elif 150 < x < 240:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.15 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            PLC_Read()
                            if PLC_Stop[1] == 1:
                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                        elif 240 < x < 300:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.42 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            PLC_Read()
                            if PLC_Stop[1] == 1:
                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                        elif 300 < x < 350:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/4.75 + 215 
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            PLC_Read()
                            if PLC_Stop[1] == 1:

                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                        elif 350 < x < 405:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/5 + 215
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            if PLC_Stop[1] == 1:
                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                        elif x > 405:
                            cap.release()
                            cv2.destroyAllWindows()
                            dType.SetQueuedCmdClear(api)
                            x = x/5.2 + 215
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 90, 50, isQueued = 1)
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 90, 7, 50, isQueued = 1)
                            dType.dSleep(2000)
                            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                            dType.dSleep(1000)
                            dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 250, 73, 100, 50, isQueued = 1)    # lifts straight up
                            PLC_Read()
                            if PLC_Stop[1] == 1:
                            PLC_SysRunning, PLC_Stop, PLC_EStop, PLC_Conveyor, PLC_Color,Sort_Color_Array,Sort_Random,Sort_Manual,Manual_Color,Sort_Same,Sort_Array,PLC_Conveyor_Speed = PLC_Read()
                            if PLC_Stop[1] == 0:
                                dType.SetQueuedCmdStartExec(api)
                            else:
                                dType.SetQueuedCmdStopExec(api)
                                break
                            break_shape = 1
                break_shape = 0
                start = 1
                print(Block_Color)
        
####################################################################################################################################
#
#   Sorting method executed based on PLC
#
####################################################################################################################################
                if Sort_Manual[1] == 1:
                    if Manual_Color[1] == 1:
                        Chosen_Color = 'Red'
                        print("Manual--Red")
                    elif Manual_Color[1] == 2:
                        Chosen_Color = 'Green'
                    elif Manual_Color[1] == 3:
                        Chosen_Color = 'Yellow'
                    else:
                        Chosen_Color = 'Blue'
                    Manual_Count = Manual_Sort(Manual_Count, Block_Color, Chosen_Color)
                elif Sort_Same[1] == 1:
                    red_count, green_count, blue_count, yellow_count = Same_Sort(Block_Color, red_count, green_count, blue_count, yellow_count)
                elif Sort_Array[1] == 1:
                    Array_Count = Array_Sort(PLC_Color_Array,Array_Count,Block_Color)
                else:
                   Block_Count = Random_Sort(Block_Count)

