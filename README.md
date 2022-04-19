# PLC-Dobot

- Joshua Waite
- Dara Eisler
- Bryce McClafferty

Primary Advisor: Dr. Asare

Secondary: Dr. Cho

## Project Goal

The goal of this project is to pick and place blocks using a DOBOT, PC, and PLC. This project incorporates computer vision for determining the color of the block being picked up as well as comparing coordinate systems so the DOBOT knows where to pick up the block on the conveyor belt. 

There will also be a manuscript provided with this to better describe how the project works and the communication methods used to accomplish the PLC and python communication.

## Included Files

All files provided are needed for use of the main file. The main file (Main_PLC-Python-Dobot.py) is used for the main control between the PLC and Dobot.

###### Tracking API (tracker.py)

This will allow the user to track objects on conveyor belt. This file should not be tampered with as it allows the Computer Vision to function properly.

###### DOBOT API (DobotDllType.py)

This will allow the user to control the Dobot. This file should not be tampered with as this is directly from the manufacturer.