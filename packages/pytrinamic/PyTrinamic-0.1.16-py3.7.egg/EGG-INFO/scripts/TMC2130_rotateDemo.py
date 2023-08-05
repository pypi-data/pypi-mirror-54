#!/usr/bin/env python3
'''
Move a motor back and forth using velocity and position mode of the TMC2130

Created on 15.10.2019

@author: JM
'''

import time
import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.evalboards.TMC2130_eval import TMC2130_eval


connectionManager = ConnectionManager()
myInterface = connectionManager.connect()

PyTrinamic.showInfo()

TMC2130 = TMC2130_eval(myInterface)

DEFAULT_MOTOR = 0

print("Rotating")
TMC2130.rotate(DEFAULT_MOTOR, 20*25600)

time.sleep(2);

print("Stopping")
TMC2130.stop(DEFAULT_MOTOR)

time.sleep(1);

print("Moving back to 0")
TMC2130.moveTo(DEFAULT_MOTOR, 0, 10000)
 
# Wait until position 0 is reached
while TMC2130.getAxisParameter(TMC2130.APs.ACTUAL_POSITION, DEFAULT_MOTOR) != 0:
    pass

print("Reached Position 0")

myInterface.close()
