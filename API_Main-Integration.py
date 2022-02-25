import cv2
import time
from tracker import *
import API as sim
import DobotDllType as dType


CON_STR = {
dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

# Connect Dobot
api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

# Setting Dobot speeds at all 4 joints 
sim.Dobot.Speed(api, 100, 100, 100, 100, 100, 100, 100, 100)

# Making sure the system is on and reading initial PLC values
sys_on, sort_style, con_on, dob_run = sim.PLC.Read()
print("here is a change")
red = 0 
green = 0
blue = 0
yellow = 0
tot = 0
global rgb
rgb = []
count = 0
#detected = 1
time.sleep(22)
# Starts the Logic Loop
if sys_on[1] == True:
    while sys_on[1] == True:
        print("System is Running.")
        sys_on, sort_style, con_on, dob_run = sim.PLC.Read()
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
        if con_on[1] == 1:
            #Dobot api, System 'on' or 'off', Conveyor speed
            sim.Dobot.Conveyor(Dapi, 'on', 5000)

### 2.) Computer Vision.
# Create tracker object
        tracker = EuclideanDistTracker()

        cap = cv2.VideoCapture(0)

        # Object detection from Stable camera
        object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

        while True:
            ret, frame = cap.read()
            height, width, _ = frame.shape


            # Extract Region of interest
            roi = frame[0: 480,0: 640]

            # 1. Object Detection
            mask = object_detector.apply(roi)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            detections = []
            for cnt in contours:
                # Calculate area and remove small elements
                area = cv2.contourArea(cnt)
                if area > 100:
                    #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)


                    detections.append([x, y, w, h])

                    print(x,y)

            # 2. Object Tracking
            boxes_ids = tracker.update(detections)
            for box_id in boxes_ids:
                #x, y, w, h, id = box_id
                #  cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                if x > -1 and y > -1:
                    sim.Dobot.Conveyor(Dapi, 'off', 0)
                    rbg = frame[x,y]
                    print(rbg)

            #cv2.imshow("roi", roi)
            cv2.imshow("Frame", frame)
            #cv2.imshow("Mask", mask)
                
            key = cv2.waitKey(30)
            if key == 27:
                break

### 3.) Machine Learning uses the pulled RGB value to detect the color of the block
        #rgb = [192, 24, 100]
        if len(rgb) == 0:
            pass
        else:
            color = sim.Machine_Learning.Color(rgb)
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
        sim.PLC.Write(color)     # Calls PLC communication function
        
### 6.) This calls the chosen sorting method and will execute the accordingly to user wants
        if sort == 'Random':
            sim.Dobot.Move_Rand(api, tot)
        elif sort == 'Manual':
            # man_sort()
            pass
        elif sort == 'Same':
            # same_sort()
            pass
        else:
            sim.Dobot.Move_Rand(api, tot)

    cap.release()
    cv2.destroyAllWindows()
else:
### * Sets dobot back to home when system is turned off
    sim.Dobot.Home(api,100, 100, 100, 50)