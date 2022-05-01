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

## Setting up the Dobot Magician

Physcially Setting up the system is super easy. The picture below will give a visual on how the system should look for the Dobot.

![Dobot Setup](/images/Dobot_Setup.png)

## Getting the System Started

## Calibrating the Camera
