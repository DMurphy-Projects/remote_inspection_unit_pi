import math as m

def lwordToDec(num):
    x = num[3] + (256*num[2]) + (65536*num[1]) + (16777216*num[0])
    return x
def decToLword(num):
    lword = [0, 0, 0, 0]
    lword[0] = int(num / 16777216)
    num = num % 16777216
    lword[1] = int(num / 65536)
    num = num % 65536
    lword[2] = int(num / 256)
    num = num % 256
    lword[3] = int(num)
    return lword
    
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

def posOnPer(per, angle):
    return (float(angle)/360)*per

def targetAngle(lm, rm, diameter, tAngle):
    curAngle = None
    acc = 1.5
    rightMov = 0
    leftMov = 0
    while not (curAngle < tAngle + acc/2 and curAngle > tAngle - acc/2) or curAngle is None:
        curAngle = getAngle(lm-rm, diameter)
        if curAngle > tAngle:
            distance = curAngle - tAngle
            left = True
        else:
            distance = tAngle - curAngle
            left = False
        if distance > 180 or distance < -180:
            left = not left
        if left:
            leftMov += 1
            rm += 5
        else:
            rightMov += 1
            lm += 5
        curAngle = getAngle(lm-rm, diameter)
    print "Movements L: %s, R: %s, Angle %s, target %s" % (leftMov, rightMov, curAngle, tAngle)
    return lm, rm

diameter = 1000
degreeMove = (m.pi * diameter)/360
leftMotor = lwordToDec([0, 1, 0, 0])
rightMotor = lwordToDec([255, 255, 255, 0])

print "Start %s" % getAngle(leftMotor-rightMotor, diameter)
leftMotor, rightMotor = targetAngle(leftMotor, rightMotor, diameter, 90)
leftMotor, rightMotor = targetAngle(leftMotor, rightMotor, diameter, 180)


