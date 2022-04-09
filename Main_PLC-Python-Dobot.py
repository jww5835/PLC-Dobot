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

#def PLC_comms(block_color):
#    with LogixDriver('192.168.222.51') as plc: # path to PLC and declaring it plc
#        print(plc)                             # basic plc info
         
#        #Depending on the users sorting method chosen from the PLC. This will determine
#        #where the block goes
#        if block_color == "Red":
#            plc.write('Program:MainProgram.Red_Py', 1)# Setting color to 1 in PLC
#        elif block_color == "Green":
#            plc.write('Program:MainProgram.Green_Py', 2)# Setting color to 2 in PLC
#        elif block_color == "Yellow":
#            plc.write('Program:MainProgram.Yellow_Py', 3)# Setting color to 3 in PLC
#        elif block_color == "Blue":
#            plc.write('Program:MainProgram.Blue_Py', 4)# Setting color to 4 in PLC
#    return

def Machine_Learning(rgb):
    

    df = pd.read_excel("ml_csv.xlsx")
    dft = pd.read_excel("ml_csv_test.xlsx")

    x_train = df.iloc[:, :-1].values
    y_train = df.iloc[:, 3].values

    # Creating an array that works with the machine learning format
    unknown_color = np.array(rgb).reshape(1,-1)  
    # How many neighbors we are comparing to. This will vary our CV accuracy
    classifier = KNeighborsClassifier(n_neighbors = 15)
    print("RGB array in ML: ", unknown_color)
    # Training our machine learning code
    #X_train = [
    #    [128, 0, 0],    # ***RED***
    #    [139, 0, 0],
    #    [165, 42, 42],
    #    [178, 34, 34],
    #    [220, 20, 60],
    #    [255, 0, 0],
    #    [255, 99, 71],
    #    [255, 69, 0],   # ***RED***
    #    [85, 107, 47],  # ***GREEN***
    #    [107, 142, 35],
    #    [124, 252, 0],
    #    [127, 255, 0],
    #    [0, 100, 0],
    #    [0, 128, 0],
    #    [34, 139, 34],
    #    [0, 255, 0],    # ***GREEN***
    #    [255, 255, 0],  # ***YELLOW***
    #    [204, 204, 0],
    #    [255, 255, 51],
    #    [255, 255, 102],
    #    [255, 255, 153],
    #    [255, 255, 204],
    #    [240, 240, 15],
    #    [245, 249, 33], # ***YELLOW***
    #    [0, 0, 255],    # ***BLUE***
    #    [0, 0, 205],
    #    [0, 0, 139],
    #    [135, 206, 250],
    #    [135, 206, 235],
    #    [30, 144, 255],
    #    [18, 48, 165],
    #    [65, 105, 225]  # ***BLUE***
    #    ]
    # This allows us to label each RGB value above
    #y_train = ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    # Combines and labels the data
    classifier.fit(X_train, y_train)
    # Predicts the true color based on the K value chosen above as well as Euclidean Distance
    true_color = classifier.predict(unknown_color)
    return true_color



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

df = pd.read_excel("ML_CSV.xlsx")
dft = pd.read_excel("ML_CSV_TEST.xlsx")

X_train = df.iloc[:, :-1].values
y_train = df.iloc[:, 3].values

while True:


         #Making sure the system is on and reading initial PLC values
    with LogixDriver('192.168.222.51') as plc:                                  #all read tags assigned
        PLC_SysRunning = plc.read('Program:MainProgram.System_Running')                 #system on
        sort_style = plc.read('Program:MainProgram.Sorting')                    #sorting style
        con_on = plc.read('Program:MainProgram.Conv_Run')
        dob_run = plc.read('Program:MainProgram.Dobot_Run')
        red = 0 
        green = 0
        blue = 0
        yellow = 0
        tot = 0
        global rgb
        rgb = []
        Block_Count = 0
        break_shape = 0
        start = 1

        # Starts the Logic Loop
        while PLC_SysRunning[1] == 1:


            print("System is Running.")
            #with LogixDriver('192.168.222.51') as plc:  
        ### *** This reads the PLC status and user inputs for sorting style
            PLC_SysRunning = plc.read('Program:MainProgram.System_Running')               
            PLC_Stop = plc.read('Program:MainProgram.Stop')                    
            PLC_EStop = plc.read('Program:MainProgram.ESTOP')
            PLC_Conveyor = plc.read('Program:MainProgram.Conv_Run')
            PLC_Color = plc.read('Program:MainProgram.Color')
            Sort_Random = plc.read('Program:MainProgram.Random')
            Sort_Manual = plc.read('Program:MainProgram.Manual')
            Sort_Same = plc.read('Program:MainProgram.Same')
        
            if PLC_EStop[1] == 1:
                dType.SetQueuedCmdForceStopExec(api)
       #     if PLC_Stop[1] == 1:
			    #	dType.SetQueuedCmdStartExec(api)
			    #else:
			    #	dType.SetQueuedCmdStopExec(api)

            # Determining the sort style
        #           if sort_style[1] == 1:
        #               sort = 'Random'
        #           elif sort_style[1] == 2:
        #               sort = 'Manual'
        #           elif sort_style[1] == 3:
        #               sort = 'Same'
        #           else:
        #               sort = 'Random'

        ### 1.) Conveyor runs when no block is detected and system is on
        ###     If block is detected or system is stopped conveyor stops
            if PLC_Conveyor[1] == 1:
                dType.SetQueuedCmdClear(api)
                dType.SetEMotor(api, 1, 1, -5000, isQueued = 1)   
                dType.SetQueuedCmdStartExec(api)
         
        ### 2.) Computer Vision.
        # Create tracker object
            #if start == 1:
            #    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            #    start = 0
            while True:
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
            

                for cnt in green_contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)

                    if area > 12000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        x = int(x + w/2)
                        y = int(y + h/2)
            

                for cnt in blue_contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)

                    if area > 12000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                        x = int(x + w/2)
                        y = int(y + h/2)

                for cnt in yellow_contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)

                    if area > 10000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
                        x = int(x + w/2)
                        y = int(y + h/2)

                if y > 220:
                    print(x,y)
                    plc.write('Program:MainProgram.Block_Detected', 1)
                    dType.SetEMotor(api, 1, 0, -5000, isQueued = 1) 
                    dType.SetQueuedCmdClear(api)
                    x1 = x
                    if x1 > 480:
                        x1 = 479
                    bgr = frame[x1,y]
                    rgb = bgr[::-1]
                    print(rgb)
                    
                
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1

                        plc.write('Program:MainProgram.Block_Detected', 0)
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1
                        plc.write('Program:MainProgram.Block_Detected', 0)
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1
                        plc.write('Program:MainProgram.Block_Detected', 0)
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1
                        plc.write('Program:MainProgram.Block_Detected', 0)
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1
                        plc.write('Program:MainProgram.Block_Detected', 0)
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
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 100, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, -48 + Block_Count*23, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, 250, 150, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(2000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243.5, 1, 50, 50, isQueued = 1)
                        dType.dSleep(3000)
                        if PLC_Stop[1] == 1:
                            dType.SetQueuedCmdStartExec(api)
                        else:
                            dType.SetQueuedCmdStopExec(api)
                        Block_Count +=1
                        break_shape = 1
                        plc.write('Program:MainProgram.Block_Detected', 0)
                 
                    if break_shape == 1:
                        start = 1
                        break
            break_shape = 0

            ### 3.) Machine Learning uses the pulled RGB value to detect the color of the block
                    #rgb = [192, 24, 100]
            if len(rgb) == 0:
                pass
            else:
                color = Machine_Learning(rgb)
            ### 4.) Keeping track of the blocks counted to account for sorting purposes
            print(color)
            ### 5.) This function writes to the PLC telling it what color has been detected
            ###     This helps with PLC control to validate what the user wants
        
            ### 6.) This calls the chosen sorting method and will execute the accordingly to user wants
            #if sort == 'Random':
            #    dType.SetQueuedCmdClear(api) # clears anything in que
            #    if tot < 4:
            #        print(tot)
            #        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -150, -43 + (tot-1)*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 100, -150, 30, 25, isQueued = 1)# nuetral postion
            #        dType.SetQueuedCmdStartExec(api)

            #    elif tot >= 4 and tot < 8:
            #        dType.SetPTPCmd(api, 0, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            #        dType.SetPTPCmd(api, 0, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            #        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            #        dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            #        dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, 1, 0, -130, -43 + tot*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion

            #    elif tot >= 8 and tot < 12:
            #        dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            #        dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            #        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            #        dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            #        dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, 1, 0, -110, -43 + tot*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion
            #    dType.SetQueuedCmdStartExec(api)
            #elif sort == 'Manual':
            #    # man_sort()
            #    break
            #elif sort == 'Same':
            #    # same_sort()
            #    break
            #else:
            #    dType.SetQueuedCmdClear(api) # clears anything in que
            #    break
            #    if count < 4:
            #        break
            #        print(count)
            #        dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            #        dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            #        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            #        dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            #        dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, 1, 0, -150, -43 + (count-1)*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion
            #        dType.SetQueuedCmdStartExec(api)

            #    elif count >= 4 and count < 8:
            #        dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            #        dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            #        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            #        dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            #        dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, 1, 0, -130, -43 + count*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion

            #    elif count >= 8 and count < 12:
            #        dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            #        dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            #        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            #        dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            #        dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            #        dType.SetPTPCmd(api, 1, 0, -110, -43 + count*27, 25, isQueued = 1) # stacking blocks location
            #        dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            #        dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            #        dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion

            #    dType.SetQueuedCmdStartExec(api)

            #dType.SetQueuedCmdClear(api)
            #dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)
            #dType.SetQueuedCmdStartExec(api)
            #block_detected = 0  #dont know if this is needed.