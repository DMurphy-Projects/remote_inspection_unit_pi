from BluetoothConnection import BluetoothConnection
from Ai import Ai
import time
import math as m
#0.1.0
class Drone:
    mBC = None
    mPos = (0, 0)#internal coords for drone
    mAngle = 6.28
    mMovement = 1#how accurate the drones internal coords are
    mEnd = False
    mAi = None
    #debug/testing
    script = ["31", "30", "010"]
    scriptCount = 0
    
    def __init__(s):
        s.mBC = BluetoothConnection()
        s.mAi = Ai(s)
        while (not s.mEnd):
            com = s.recieveCommand()
            s.convertToAction(com)
            
    def __del__(s):
        s.mEnd = True

    def recieveCommand(s):#may be replace with call to bluetoothConnection
        #bluetooth recieve using class
        #example of command recieved, eg 1st char is command rest are parameters
        if (s.scriptCount >= len(s.script)):
            s.mEnd = True
            return ""
        else: data = s.script[s.scriptCount]
        s.scriptCount += 1
        return data

    def convertToAction(s, data):
        command = data[:1]
        parameter = data[1:]
        #print(str(command) + " " + str(parameter))
        if (s.mAi.getState() == 0):
            if (command == "0"):
                s.forward(int(parameter))
            elif (command == "1"):
                s.turnLeft()
            elif (command == "2"):
                s.turnRight()
        if (command == "3"):
            s.mAi.setState(int(parameter))
            
            
    def forward(s, count = 1):
        for x in range(0, count):
            if (not s.getAhead()):
                pos = (s.mPos[0] + (m.cos(s.mAngle)*s.mMovement), s.mPos[1] - (m.sin(s.mAngle)*s.mMovement))
                s.mPos = (round(pos[0], 2), round(pos[1], 2))
                #whatever makes the hardware move
                
    def turnLeft(s, angle=m.pi/2):
        s.mAngle = s.mAngle + angle
        if s.mAngle > 2*m.pi:
            s.mAngle = 0 + s.mAngle-2*m.pi
        s.mAngle = round(s.mAngle, 2)
        #whatever makes the hardware turn
    
    def turnRight(s, angle=m.pi/2):
        s.mAngle = s.mAngle - angle
        if s.mAngle <= 0:
            s.mAngle = 2*m.pi + s.mAngle
        s.mAngle = round(s.mAngle, 2)
        #whatever makes the hardware turn

    def getAhead(s):
        #take reading from drones sensors
        return False
Drone()
