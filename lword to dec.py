import math as m

def lwordToDec(num):
    x = num[3] + (256*num[2]) + (65536*num[1]) + (16777216*num[0])
    return x

def normaliseAngle(angle):
    angle = angle % (2*m.pi)
    angle = (angle + (2*m.pi)) % (2*m.pi)
    return angle

def getAngle(pos, diameter):
    angle = pos/(diameter*m.pi) * 100 # percentage of perimeter compared to distance moved
    angle *= m.pi/50 #convert percentage of perimter to radian angle
    angle = normaliseAngle(angle)
    angle *=180/m.pi #convert to degrees
    return angle

diameter = 100
degreeMove = (m.pi * diameter)/360
leftMotor = lwordToDec([0, 0, 0, 0])
rightMotor = lwordToDec([0, 0, 0, 0])

for x in range(20):
    dif = rightMotor - leftMotor
    print "%s degrees" % getAngle(dif, diameter)
    leftMotor += degreeMove
