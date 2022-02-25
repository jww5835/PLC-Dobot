from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import DobotDllType as dType
from pycomm3 import *

class Machine_Learning:
    
    def Color(rgb):
        unknown_color = np.array(rgb).reshape(1,-1)
        classifier = KNeighborsClassifier(n_neighbors = 23)
        learning_set = [
        [128, 0, 0],    # ***RED***
        [139, 0, 0],
        [165, 42, 42],
        [178, 34, 34],
        [220, 20, 60],
        [255, 0, 0],
        [255, 99, 71],
        [255, 69, 0],   # ***RED***
        [85, 107, 47],  # ***GREEN***
        [107, 142, 35],
        [124, 252, 0],
        [127, 255, 0],
        [0, 100, 0],
        [0, 128, 0],
        [34, 139, 34],
        [0, 255, 0],    # ***GREEN***
        [255, 255, 0],  # ***YELLOW***
        [204, 204, 0],
        [255, 255, 51],
        [255, 255, 102],
        [255, 255, 153],
        [255, 255, 204],
        [240, 240, 15],
        [245, 249, 33], # ***YELLOW***
        [0, 0, 255],    # ***BLUE***
        [0, 0, 205],
        [0, 0, 139],
        [135, 206, 250],
        [135, 206, 235],
        [30, 144, 255],
        [18, 48, 165],
        [65, 105, 225]  # ***BLUE***
        ]

        label_set = ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']

        classifier.fit(learning_set, label_set)

        guess = classifier.predict(unknown_color)

        return guess

class Dobot:

    def Speed(api, j1_V, j1_A, j2_V, j2_A, j3_V, j3_A, j4_V, j4_A):
        dType.SetQueuedCmdClear(api)
        dType.SetHOMEParams(api, 100, -100, 100, 100, isQueued = 1)
        dType.SetPTPJointParams(api, j1_V, j1_A, j2_V, j2_A, j3_V, j3_A, j4_V, j4_A, isQueued = 1)
        dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
        dType.SetHOMECmd(api, temp=0, isQueued = 1)
        dType.SetQueuedCmdStartExec(api)
        return

    def Conveyor(api, state, speed):
        
        if state == 'on':
            dType.SetEMotor(api, 0, 1, speed, isQueued = 0)
            dType.SetQueuedCmdStartExec(api)
        elif state == 'off':
            dType.SetEMotor(api, 0, 0, speed, isQueued = 0)
            dType.SetQueuedCmdStartExec(api) 
        else:
            pass
        return
    
    def Move_Rand(api, tot):

        if tot < 4:
            dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            dType.SetPTPCmd(api, 1, 0, -150, -43 + (tot-1)*27, 25, isQueued = 1) # stacking blocks location
            dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion

        elif tot >= 4 and tot < 8:
            dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            dType.SetPTPCmd(api, 1, 0, -130, -43 + tot*27, 25, isQueued = 1) # stacking blocks location
            dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion

        elif tot >= 8 and tot < 12:
            dType.SetPTPCmd(api, 1, 100, 0, 25, 0, isQueued = 1)    # on top of conveyor block
            dType.SetPTPCmd(api, 1, 100, 0, 14, 0, isQueued = 1)    # 13 Z is ideal for conveyor pick up
            dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
            dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)    # lifts straight up
            dType.SetPTPCmd(api, 1, 0, -150, 13, 25, isQueued = 1)  # Home-esk position
            dType.SetPTPCmd(api, 1, 0, -110, -43 + tot*27, 25, isQueued = 1) # stacking blocks location
            dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
            dType.SetPTPCmd(api, 1, 0, -150, 50, 25, isQueued = 1)  # lifts straight up
            dType.SetPTPCmd(api, 1, 100, -150, 30, 25, isQueued = 1)# nuetral postion
        dType.SetQueuedCmdStartExec(api)
        return

    def Home(api, x, y, z, rhead):
        dType.SetPTPCmd(api, 1, x, y, z, rhead, isQueued = 1)# nuetral postion
        dType.SetQueuedCmdStartExec(api) 
        return

class PLC:

    def Read():
        with LogixDriver('192.168.222.51') as plc:  
        ### *** This reads the PLC status and user inputs for sorting style
            sys_on = plc.read('Program:MainProgram.System_Running')               
            sort_style = plc.read('Program:MainProgram.Sorting')                    
            con_on = plc.read('Program:MainProgram.Conv_Run')
            dob_run = plc.read('Program:MainProgram.Dobot_Run')
            return sys_on, sort_style, con_on, dob_run

    def Write(block_color):
        with LogixDriver('192.168.222.51') as plc: # path to PLC and declaring it plc
            
            # Depending on the users sorting method chosen from the PLC. This will determine
            # where the block goes
            if block_color == "R":
                plc.write('Program:MainProgram.Red_Py', 1)# Setting color to 1 in PLC
            elif block_color == "G":
                plc.write('Program:MainProgram.Green_Py', 2)# Setting color to 2 in PLC
            elif block_color == "Y":
                plc.write('Program:MainProgram.Yellow_Py', 3)# Setting color to 3 in PLC
            elif block_color == "B":
                plc.write('Program:MainProgram.Blue_Py', 4)# Setting color to 4 in PLC
            return