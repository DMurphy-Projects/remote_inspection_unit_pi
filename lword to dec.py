import math as m

def lwordToDec(num):
    x = num[3] + (256*num[2]) + (65536*num[1]) + (16777216*num[0])
    return x

def getAngle(pos, diameter):
    angle = pos/(diameter*m.pi)
    angle *= 100
    angle *= m.pi/50
    while angle > 2*m.pi:
        angle -= 2*m.pi
    angle *=180/m.pi #convert to degrees
    return angle

diameter = 100
leftMotor = lwordToDec([0, 0, 0, 0])
rightMotor = lwordToDec([0, 0, 0, 0])

for x in range(10):
    if leftMotor > rightMotor:
        dif = leftMotor - rightMotor
    else:
        dif = rightMotor - leftMotor
    print "%s degrees" % getAngle(dif, diameter)
    leftMotor += 20
