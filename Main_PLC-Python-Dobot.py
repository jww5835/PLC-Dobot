import math
from sklearn.neighbors import KNeighborsClassifier
#from matplotlib import pyplot as plt
import threading
import DobotDllType as dType
# import imutils
import time
from tracker import *

def PLC_comms(block_color):
    with LogixDriver('192.168.222.51') as plc: # path to PLC and declaring it plc
        #print(plc)                             # basic plc info
         
        # Depending on the users sorting method chosen from the PLC. This will determine
        # where the block goes
        if block_color == "Red":
            plc.write('Program:MainProgram.Red_Py', 1)# Setting color to 1 in PLC
        elif block_color == "Green":
            plc.write('Program:MainProgram.Green_Py', 2)# Setting color to 2 in PLC
        elif block_color == "Yellow":
            plc.write('Program:MainProgram.Yellow_Py', 3)# Setting color to 3 in PLC
        elif block_color == "Blue":
            plc.write('Program:MainProgram.Blue_Py', 4)# Setting color to 4 in PLC
    return

def Machine_Learning(rgb):

    # Creating an array that works with the machine learning format
    unknown_color = np.array(rgb).reshape(1,-1)  
    # How many neighbors we are comparing to. This will vary our CV accuracy
    classifier = KNeighborsClassifier(n_neighbors = 5)
    print("RGB array in ML: ", unknown_color)
    # Training our machine learning code
    learning_set = [
        [128, 0, 0],    # ***RED***
        [139, 0, 0],
        [165, 42, 42],
        [178, 34, 34],
        [220, 20, 60],
        [255, 0, 0],
        [255, 99, 71],
        [255, 69, 0],
        [255, 130, 92],
        [255, 147, 115],
        [237, 151, 126],
        [245, 169, 147],# ***RED***
        [85, 107, 47],  # ***GREEN***
        [107, 142, 35],
        [124, 252, 0],
        [127, 255, 0],
        [0, 100, 0],
        [0, 128, 0],
        [34, 139, 34],
        [0, 255, 0],    
        [213, 255, 145],
        [200, 247, 124],
        [186, 230, 115],
        [198, 247, 119],# ***GREEN***
        [255, 255, 0],  # ***YELLOW***
        [204, 204, 0],
        [255, 255, 51],
        [255, 255, 102],
        [255, 255, 153],
        [255, 255, 204],
        [240, 240, 15],
        [245, 249, 33],
        [247, 247, 134],
        [243, 250, 150],
        [252, 255, 173],
        [253, 255, 189],# ***YELLOW***
        [0, 0, 255],    # ***BLUE***
        [0, 0, 205],
        [0, 0, 139],
        [135, 206, 250],
        [135, 206, 235],
        [30, 144, 255],
        [18, 48, 165],
        [65, 105, 225],  
        [66, 209, 245],
        [66, 236, 245],
        [66, 245, 242],
        [101, 252, 250], # ***BLUE***
        ]
    # This allows us to label each RGB value above
    label_set = ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    # Combines and labels the data
    classifier.fit(learning_set, label_set)
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
dType.SetHOMEParams(api, 228, -31, 45, 50, isQueued = 1)
dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
dType.SetHOMECmd(api, temp=0, isQueued = 1)
dType.SetQueuedCmdStartExec(api)
time.sleep(23)
#dType.SetQueuedCmdClear(api)
#dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 228, -31, 45, 50, isQueued = 1)
#dType.SetQueuedCmdStartExec(api)
#pose = dType.GetPose(api)
#print(pose)

while True:
    # Making sure the system is on and reading initial PLC values
    with LogixDriver('192.168.222.51') as plc:                                  #all read tags assigned
                sys_on = plc.read('Program:MainProgram.System_Running')                 #system on
                sort_style = plc.read('Program:MainProgram.Sorting')                    #sorting style
                con_on = plc.read('Program:MainProgram.Conv_Run')
                dob_run = plc.read('Program:MainProgram.Dobot_Run')
    #print(sys_on)
    #print(sort_style)
    #print(con_on)
    #print(dob_run)
    red = 0 
    green = 0
    blue = 0
    yellow = 0
    tot = 0
    global rgb
    rgb = []
    count = 0
    break_shape = 0
    #detected = 1
    #dType.dSleep(10000)

    # Starts the Logic Loop
    if sys_on[1] == True:
        while sys_on[1] == True:
            break_shape = 0
            dType.SetQueuedCmdClear(api)
            print("System is Running.")
            with LogixDriver('192.168.222.51') as plc:  
    ### *** This reads the PLC status and user inputs for sorting style
                sys_on = plc.read('Program:MainProgram.System_Running')               
                sort_style = plc.read('Program:MainProgram.Sorting')                    
                con_on = plc.read('Program:MainProgram.Conv_Run')
                dob_run = plc.read('Program:MainProgram.Dobot_Run')
            #   print(sys_on)
            #   print(sort_style)
            #   print(con_on)
            #   print(dob_run)

            # Determining the sort style
                if sort_style[1] == 1:
                    sort = 'Random'
                elif sort_style[1] == 2:
                    sort = 'Manual'
                elif sort_style[1] == 3:
                    sort = 'Same'
                else:
                    sort = 'Random'

    ### 1.) Conveyor runs when no block is detected and system is on
    ###     If block is detected or system is stopped conveyor stops

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            while(True):
                ret, frame = cap.read()                 # Capture the video frame by frame
                cv2.imshow('Camera', frame)             # Display the resulting frame
                break
            if con_on[1] == 1:
                dType.SetQueuedCmdClear(api)
                dType.SetEMotor(api, 1, 1, -2500, isQueued = 1)            
                dType.SetQueuedCmdStartExec(api)

    ### 2.) Computer Vision.
    # Create tracker object
            tracker = EuclideanDistTracker()

            # Object detection from Stable camera
            object_detector = cv2.createBackgroundSubtractorMOG2(history=225, varThreshold=55)

            while True:
                ret, frame = cap.read()
                height, width, _ = frame.shape

                # Extract Region of interest
                roi = frame[395: 500,100: 440]
         
                # 1. Object Detection
                mask = object_detector.apply(roi)
                _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                detections = []
                for cnt in contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                        x, y, w, h = cv2.boundingRect(cnt)
                        detections.append([x, y, w, h])

                # 2. Object Tracking
                boxes_ids = tracker.update(detections)
                for box_id in boxes_ids:
                    #x, y, w, h, id = box_id
                    #  cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    if x > -1 and y > -1:
                        dType.SetEMotor(api, 1, 0, 0, isQueued = 0)
                        #dType.SetQueuedCmdClear(api)
                        #dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 273, 85.5, 100, 50, isQueued = 1)
                        dType.SetQueuedCmdStartExec(api)
                        cap.release()
                        
                        print(x,y)
                        x2 = x + 120
                        y2 = 350
                        
                        
                        bgr = frame[x2,y2]
                        rgb = bgr[::-1]
                        print(rgb)
                      
                        x = x/3.08 + 200
                        print(x,y)
                        dType.SetQueuedCmdClear(api)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 273, 45, 100, 50, isQueued = 1)
                        dType.dSleep(1000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, 45, 5, 50, isQueued = 1)
                        dType.dSleep(1000)
                        dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued = 1) # suction on
                        dType.dSleep(1000)
                        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode,  273, 45, 50, 50, isQueued = 1)    # lifts straight up
                        dType.dSleep(1000)
                       # dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                        #dType.dSleep(1000)
                        dType.SetQueuedCmdStartExec(api)
                        #lastIndex = dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1)[0]
                        #while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                        #    dType.dSleep(100)
                        break_shape = 1
                        time.sleep(5)
                        #break

                cv2.imshow("roi",roi)
                cv2.imshow("Frame", frame)
                cv2.destroyAllWindows()

                if break_shape == 1:
                    break

    ### 3.) Machine Learning uses the pulled RGB value to detect the color of the block
            #rgb = [192, 24, 100]
            if len(rgb) == 0:
                pass
            else:
                color = Machine_Learning(rgb)
    ### 4.) Keeping track of the blocks counted to account for sorting purposes
            if (color == 'R') and (red < 4):
                red += 1
                tot += 1
            elif (color == 'G') and (green < 4):
                green += 1
                tot += 1
            elif (color == 'B') and (blue < 4):
                blue += 1
                tot += 1
            elif (color == 'Y') and (yellow < 4):
                yellow += 1
                tot += 1
            print(color)
    ### 5.) This function writes to the PLC telling it what color has been detected
    ###     This helps with PLC control to validate what the user wants
            PLC_comms(color)     # Calls PLC communication function
        
    ### 6.) This calls the chosen sorting method and will execute the accordingly to user wants
            if sort == 'Random':
                dType.SetQueuedCmdClear(api) # clears anything in que
                if tot < 5:

                    print("Total Blocks Stacked: ", tot)
                    print("Total block stack: ", (tot-1)*27)
                    z = -50 + (tot-1)*24
                    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 72, 212, 100, 0, isQueued = 1)  # Home-esk position
                    dType.dSleep(1000)
                    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 72, 212, z, 25, isQueued = 1) # stacking blocks location
                    dType.dSleep(1000)
                    dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued = 1) # suction off
                    dType.dSleep(1000)
                    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 72, 212, 100, 0, isQueued = 1)  # lifts straight up
                    dType.dSleep(1000)
                    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 273, 85.5, 100, 50, isQueued = 1)# nuetral postion
                    dType.dSleep(1000)
                    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 228, -31, 45, 50, isQueued = 1)
                    dType.dSleep(5000)
                    dType.SetQueuedCmdStartExec(api)

                elif tot >= 8 and tot < 12:
                    pass
                dType.SetQueuedCmdStartExec(api)
            elif sort == 'Manual':
                # man_sort()
                break
            elif sort == 'Same':
                # same_sort()
                break
            else:
                dType.SetQueuedCmdClear(api) # clears anything in que
                break
                if count < 4:
                    break
                    print(count)

                dType.SetQueuedCmdStartExec(api)

            #dType.SetQueuedCmdClear(api)
            #dType.SetPTPCmd(api, 1, 100, 0, 30, 0, isQueued = 1)
            #dType.SetQueuedCmdStartExec(api)
            #block_detected = 0  #dont know if this is needed.

    else:
    ### * Sets dobot back to home when system is turned off
        print("System is off")
        #dType.SetHOMECmd(api, temp = 0, isQueued = 0)
        time.sleep(5)
