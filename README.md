# PLC-Dobot

- Joshua Waite
- Dara Eisler
- Bryce McClafferty

Primary Advisor: Dr. Asare-Yeboah
Secondary: Dr. Cho

Advisor: Penn State Behrend (Professor Loker)

## Project Goal

The goal of this project is to pick and place blocks using a DOBOT, PC, and PLC. This project incorporates computer vision for determining the color of the block being picked up as well as comparing coordinate systems so the DOBOT knows where to pick up the block on the conveyor belt. 

There will also be a manuscript provided with this to better describe how the project works and the communication methods used to accomplish the PLC and python communication.

## Included Files

All files provided are needed for use of the main file. The main file (Main_PLC-Python-Dobot.py) is used for the main control between the PLC and Dobot.

###### Tracking API (tracker.py)

This will allow the user to track objects on conveyor belt. This file should not be tampered with as it allows the Computer Vision to function properly.

###### DOBOT API (DobotDllType.py)

This will allow the user to control the Dobot. This file should not be tampered with as this is directly from the manufacturer.

# Manual

Here we will be describing what you will need to do to get this system up and running.

## Disclaimer

The Dobot API that runs through the dll files will only work on windows as they do not provide the libraries for Mac or Linux environments. There are solutions out there to combat this problem but we had a very hard time in a linux environment creating the .so files. 

## IDE Setup

In this project we used Visual Studio on Windows 10. Although this is what we used you can use whatever IDE works for you. In Visual Studio you will have to pip install this set of Python libraries into this projects environment. 

- pip install pycomm3
- pip install opencv-python
- pip install numpy

After these have been installed the main file will work well with all imported libraries.

## HMI & PLC Setup

Compact Logix 5380 5069-L306ERM is the specific controller that was used for this project. 

Software for the PLC Code: Allen Bradley Rockwell Studio 5000
  - Exact file in the GitHub: Dobot_V1PLC.ACD

Software used to create the HMI: Studio 5000 View Designer
  - Exact file in the GitHub: DobotPLC_HMI_V1.vpd

If you are using compact logix the current code will work. If you need other drivers for different Allen Bradley PLCs please check the Pycomm3 Documentation linked below:

https://docs.pycomm3.dev/en/latest/

## System Diagram 

Follow this level 2 diagram to replicate our system:

![Level 2](/Images/Level2.png)

## Setting up the Dobot Magician

Physcially Setting up the system is super easy. The picture below will give a visual on how the system should look for the Dobot.

![Dobot Setup](/Images/Dobot_Setup.png)

The motor of the conveyor belt should be placed away from the dobot on the right side. The conveyor box also provides a setter that will allow the Dobot to be set in the same position everytime. Once the Dobot is set up, the last thing youll have to do is set up the webcam. The webcam will be placed right next to the suction cup on the end of the robotic arm. This 3D printed arm was found online at ---. This will be mounted with whatever camera you have using --- notches of the ball and socket joints. These joints have been soldered together for permanent results.   

## Getting the System Started

Once everything is wired up and set up, we can start the running process. Get the main python program running (Main_PLC-Python-Dobot.py) and the Dobot will home to calibrate itself and then stop. This is on a timer so nothing will happen for roughly 23 seconds. From here, everything can be ran from the HMI and PLC. The system is full functional and capable of being changed from there. 

## Calibrating the Camera

## HMI Screens
