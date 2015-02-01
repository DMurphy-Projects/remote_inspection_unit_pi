import time
import threading as t
import math as m
import time
from Node import Node
#0.1.2
class Ai:
    mState = 0#0 pause, 1 explore, 2 return, 3 stop
    mDrone = None
    mAiThread = None
    mPosDir = [2*m.pi, m.pi/2, m.pi, 3*m.pi/2]
    mMazeInfo = []
    mCurNode = None
    
    def __init__(s, _drone):
        s.mDrone = _drone
        s.mAiThread = t.Thread(target = s.aiLoop)
        s.mAiThread.start()
        
    def aiLoop(s):
        s.mCurNode = Node(s.mDrone.mPos[0], s.mDrone.mPos[1])
        s.mMazeInfo.append(s.mCurNode)#adds start loc
        while (not s.mDrone.mEnd):
            if (s.mState == 0):
                time.sleep(0.5)
            elif (s.mState == 1):
                print ("Exploring")
                end = False
                while (s.mState == 1):
                    avDir = False#available direction
                    #skipDir = s.getOppositeDir(s.getCardinalDir())#the direction that is 180 degrees of the current direction
                    for i in s.mCurNode.mDir[:]:
                        s.faceDir(s.mPosDir[i])
                        block = s.mDrone.getAhead()
                        s.mCurNode.remove(i)
                        #print ("Block:" + str(block) + " dir:" + str(i))
                        if (not block):
                            temp = Node(round(s.mDrone.mPos[0]+m.cos(s.mDrone.mAngle), 2), round(s.mDrone.mPos[1]-m.sin(s.mDrone.mAngle), 2))
                            #print ("--TempNode : " + str(temp.mX) + " " + str(temp.mY) + " Exist:" + str(exist) + " i:"+str(i))
                            if (not s.nodeExists(temp)):
                                avDir = True
                                break
                    if (avDir):
                        #goto curNode
                        #print ("Goto : " + str(s.mCurNode.mX) + " " + str(s.mCurNode.mY) + "\n")
                        s.goTo(temp)
                        #print (s.getOppositeDir(s.getCardinalDir()))
                        s.mCurNode.remove(s.getOppositeDir(s.getCardinalDir()))
                    else:
                        print ("Back Tracking")
                        #goto curNode.parent
                        s.backTrack()
            elif (s.mState == 2):
                print ("Returning")
                while (not s.mCurNode.mParent == None and s.mState == 2):
                    s.backTrack()
            else:
                s.setState(0)
        print ("Ai Ended")
        
    def backTrack(s):
        if (not s.mCurNode == None):
            if (not s.mCurNode.mParent == None):
                #print ("Goto : " + str(s.mCurNode.mParent.mX) + " " + str(s.mCurNode.mParent.mY) + "\n")
                s.goTo(s.mCurNode.mParent)
        if (len(s.mCurNode.mDir) == 0 and s.mCurNode.mParent == None):
            print ("Home")
            s.setState(0)
            for x in s.mMazeInfo:
                if (not len(x.mDir) == 0):
                    print (str(x.mDir) + " " + str(x.mX) + " " + str(x.mY))
            s.clearMaze()
                
    def faceDir(s, _dir):
        #time.sleep(0.5)
        #print ("Face Dir : " + str(_dir))
        while (not s.mDrone.mAngle == round(_dir, 2)):#needs to be better
            s.mDrone.turnLeft()
            
    def goTo(s, node):
        deltaX = node.mX - s.mDrone.mPos[0]
        deltaY = s.mDrone.mPos[1] - node.mY
        
        angle = m.atan2(deltaY, deltaX)
        #print(round(angle, 2))
        if (angle <= 0):
            angle += m.pi*2
        #print (round(angle, 2))
        s.faceDir(angle)
        s.mDrone.move()
        time.sleep(0.1)
        
    def nodeExists(s, temp):
        for node in s.mMazeInfo:
            #print ("CheckNode : " + str(node.mX) + " " + str(node.mY))
            if (node.mX == temp.mX and node.mY == temp.mY):
                return node
        return False
    
    def setState(s, state):
        s.mState = state
        print ("Ai State : " + str(state))
        
    def getState(s):
        return s.mState
    
    def updateNode(s):
        temp = Node(s.mDrone.mPos[0], s.mDrone.mPos[1])
        existNode = s.nodeExists(temp)
        if (not existNode):
            temp.mParent = s.mCurNode
            s.mMazeInfo.append(temp)
            s.mCurNode = temp
            #print("CurNode : " + str(s.mCurNode.mX) + " " + str(s.mCurNode.mY))
            #print("ParNode : " + str(s.mCurNode.mParent.mX) + " " + str(s.mCurNode.mParent.mY))
        else:
            s.mCurNode = existNode

    def getCardinalDir(s):
        for i in range(len(s.mPosDir)):
            if (round(s.mPosDir[i],2) == s.mDrone.mAngle):
                return i
    def getOppositeDir(s, _dir):
        _dir -= 2
        if (_dir < 0): _dir += 4
        return _dir
        
    def clearMaze(s):
        temp = s.mMazeInfo[0]
        s.mMazeInfo = []
        s.mMazeInfo.append(temp)
    
