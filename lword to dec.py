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
    curAngle = getAngle(lm-rm, diameter)
    per = diameter * m.pi
    curPos = posOnPer(per, curAngle)
    tarPos = posOnPer(per, tAngle)
    dLeft = curPos - tarPos
    dRight = tarPos - curPos
    if dLeft < 0: dLeft += per
    if dRight < 0: dRight += per
    #print "L %s, R %s" % (dLeft, dRight)
    if (dLeft < dRight):
        distance = dLeft
        mod = (-1, 1)
    else:
        distance = dRight
        mod = (1, -1)
    leftMPos = lm + (mod[0] * distance/2)
    rightMPos = rm + (mod[1] * distance/2)
    print "L Pos %s, R Pos %s" % (decToLword(leftMPos), decToLword(rightMPos))
    

diameter = 100
degreeMove = (m.pi * diameter)/360
leftMotor = lwordToDec([0, 1, 0, 0])
rightMotor = lwordToDec([0, 1, 0, 0])

targetAngle(leftMotor, rightMotor, diameter, 90)

print getAngle(leftMotor-rightMotor, diameter)
leftMotor += 50
rightMotor -= 50
print getAngle(leftMotor-rightMotor, diameter)

#targetAngle(leftMotor, rightMotor, diameter, 90)


