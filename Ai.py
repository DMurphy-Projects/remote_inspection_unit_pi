import time
import threading as t
import math as m
import time
from Node import Node
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
        s.mCurNode = Node(s.mDrone.pos[0], s.mDrone.pos[1])
        s.mMazeInfo.append(s.mCurNode)#adds start loc
        while (not s.mDrone.mEnd):
            if (s.mState == 0):
                time.sleep(0.5)
            elif (s.mState == 1):
                print ("Exploring")
                end = False
                while (s.mState == 1):
                    avDir = False#available direction
                    i = 0
                    while i < len(s.mPosDir):
                        s.faceDir(s.mPosDir[i])
                        block = s.mDrone.getAhead()
                        #print ("Block:" + str(block) + " dir:" + str(i))
                        if (not block):
                            temp = Node(round(s.mDrone.pos[0]+m.cos(s.mDrone.angle), 2), round(s.mDrone.pos[1]-m.sin(s.mDrone.angle), 2))
                            #print ("--TempNode : " + str(temp.mX) + " " + str(temp.mY) + " Exist:" + str(exist) + " i:"+str(i))
                            if (not s.nodeExists(temp)):
                                avDir = True
                                break
                        i += 1
                    if (avDir):
                        #goto curNode
                        #print ("Goto : " + str(s.mCurNode.mX) + " " + str(s.mCurNode.mY) + "\n")
                        s.goTo(temp)
                    else:
                        print ("Going home")
                        #goto curNode.parent
                        s.goHome()
            elif (s.mState == 2):
                print ("Returning")
                s.goHome()
            else:
                s.setState(0)
        print ("Ai Ended")
    def goHome(s):
        while (not s.mCurNode.mParent == None and (s.mState == 2 or s.mState == 1)):
            if (not s.mCurNode == None):
                if (not s.mCurNode.mParent == None):
                    #print ("Goto : " + str(s.mCurNode.mParent.mX) + " " + str(s.mCurNode.mParent.mY) + "\n")
                    s.goTo(s.mCurNode.mParent)
        if (s.mCurNode.mParent == None):
            print ("Home")
            s.setState(0)
            s.clearMaze()
                
    def faceDir(s, _dir):
        #print ("Face Dir : " + str(_dir))
        while (not s.mDrone.angle == round(_dir, 2)):
            s.mDrone.turnLeft()
    def goTo(s, node):
        deltaX = node.mX - s.mDrone.pos[0]
        deltaY = s.mDrone.pos[1] - node.mY
        
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
        temp = Node(s.mDrone.pos[0], s.mDrone.pos[1])
        existNode = s.nodeExists(temp)
        if (not existNode):
            temp.mParent = s.mCurNode
            s.mMazeInfo.append(temp)
            s.mCurNode = temp
            #print("CurNode : " + str(s.mCurNode.mX) + " " + str(s.mCurNode.mY))
            #print("ParNode : " + str(s.mCurNode.mParent.mX) + " " + str(s.mCurNode.mParent.mY))
        else:
            s.mCurNode = existNode
            
    def clearMaze(s):
        temp = s.mMazeInfo[0]
        s.mMazeInfo = []
        s.mMazeInfo.append(temp)
    
