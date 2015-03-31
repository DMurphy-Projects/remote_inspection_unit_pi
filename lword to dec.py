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
    #angle *=180/m.pi #convert to degrees
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


def getNewPos(l, r, l2, r2, diameter):
    x = 0
    y = 0
    angle1 = getAngle(l-r, diameter)
    angle2 = getAngle(l2-r2, diameter)
    res = 2
    angleDist = min(abs(angle1-angle2), angle2-angle1)/res
    dist = (((l2-l) + (r2-r)) / 2) / res
    for i in range(res+1):
        x += m.cos(angle1)*dist
        y += m.sin(angle1)*dist
        angle1 += angleDist
        
    return x, y
diameter = 1000
#leftMotor = lwordToDec([0, 1, 100, 0])
#rightMotor = lwordToDec([255, 255, 255, 0])

l = 400
r = 400
l2 = l + 100
r2 = r - 100

x, y = getNewPos(l, r, l2, r2, diameter)
print x
print y

