from Tkinter import *
from Ai import Ai
from PIL import Image
import threading as t
import time
import math as m
import random as r
from BluetoothConnection import BluetoothConnection

#0.3.0
class turtle:
    height = 20#of field
    width = 20
    mPos = (5, 5)
    mAngle = 6.28
    ob = []#obstacles
    #ob = [(5, 5)]
    movement = 1#many blocks turtle moves by
    mEnd = False

    ai = None
    bc = None
    def __init__(s):
        img = Image.open("maze.jpg")
        pixels = img.load()
        s.width, s.height = img.size

        s.bc = BluetoothConnection(True)
        
        s.root = Tk()
        s.canvas = Canvas(s.root, width=s.width*10+10, height=s.height*10+10)
        s.canvas.pack()
        s.canvas.create_rectangle(0, 0, s.width*10, s.height*10, fill='white')
        s.rec = s.canvas.create_rectangle(0, 0, 0, 0, fill='black')
        s.line = s.canvas.create_line(0, 0, 0, s.width)
        s.userControlled()
        s.root.protocol("WM_DELETE_WINDOW", s.__del__)
        s.clientThread = t.Thread(target = s.clientControlled)#client on own thread/client being remote user
        s.clientThread.start()

        s.ai = Ai(s)
        for x in range(s.width):
            for y in range(s.height):
                if (pixels[x, y] >= (0, 0, 0) and pixels[x, y] <= (10, 10, 10)):
                    s.ob.append((x, y))
        
        s.draw()
        for o in s.ob:
            x = ((o[0]+1)*10)-10
            y = ((o[1]+1)*10)-10
            s.canvas.create_rectangle(x, y, x+10, y+10, fill='black')
        s.root.mainloop()

    #0 forward, 1 turnRight, 2 turnLeft, eg 010(forward 10)
    def clientControlled(s):#thread 02
        s.bc.connect()
        while not s.mEnd:
            data = s.bc.recieve()
            if not data == "exit":
                command = data[:1]#first char
                para = data[1:]#from the first to the end
                if command == "0":
                    para = int(para)
                    if para < 1: para=1
                    elif para > 100: para=100
                    s.move(moves=para)
                elif command == "1" or command == "2":
                    para = float(para)
                    if para < 0: para=0
                    elif para > 360: para=360
                    para = (para/180) * (m.pi)
                    if command == "1": s.turnRight(angle=para)
                    elif command == "2": s.turnLeft(angle=para)
                elif command == "3":
                    s.ai.setState(int(para))
            else:
                s.__del__()
        print ("Client Thread End")
            
    def userControlled(s):
        def aiExplore(e):
            if not s.ai.getState() == 1:
                s.ai.setState(1)
            else:
                s.ai.setState(0)
        def aiReturnHome(e):
            if not s.ai.getState() == 2:
                s.ai.setState(2)
            else:
                s.ai.setState(0)
        def userEnd(e):
            s.__del__()
        frame = Frame(s.root, width=0, height=0)
        frame.bind("<Up>", s.move)
        frame.bind("<Left>", s.turnLeft)
        frame.bind("<Right>", s.turnRight)
        frame.bind("<Return>", aiExplore)
        frame.bind("<BackSpace>", aiReturnHome)
        frame.bind("<Escape>", userEnd)
        frame.pack()
        frame.focus_set()
    
    def draw(s):
        x = ((s.mPos[0]+1)*10)-10
        y = ((s.mPos[1]+1)*10)-10
        lineX = ((s.mPos[0] + m.cos(s.mAngle)+1)*10)-10
        lineY = ((s.mPos[1] - m.sin(s.mAngle)+1)*10)-10
        s.canvas.delete(s.rec)
        s.rec = s.canvas.create_rectangle(x, y, x+9, y+9)
        s.canvas.delete(s.line)
        s.line = s.canvas.create_line(x+5, y+5, lineX+5, lineY+5, fill="red")            
    
    def turnLeft(s, event=None, angle=m.pi/2):#90deg=pi/2, etc
        s.mAngle = s.mAngle + angle
        if s.mAngle > 2*m.pi:
            s.mAngle = 0 + s.mAngle-2*m.pi
        s.mAngle = round(s.mAngle, 2)
        #print(s.mAngle)
        s.draw()

    def turnRight(s, event=None, angle=m.pi/2):
        s.mAngle = s.mAngle - angle
        if s.mAngle <= 0:
            s.mAngle = 2*m.pi + s.mAngle
        s.mAngle = round(s.mAngle, 2)
        #print(s.mAngle)
        s.draw()

    def move(s, event=None, moves=1):
        for x in range(0, moves):
            pos = (s.mPos[0] + (m.cos(s.mAngle)*s.movement), s.mPos[1] - (m.sin(s.mAngle)*s.movement))
            pos = (round(pos[0], 2), round(pos[1], 2))
	    #check for objects in way
	    #check inside field
            if (not s.getAhead()):
                if (pos[0] >= 0 and pos[0]+1 <= s.width and pos[1] >= 0 and pos[1]+1 <= s.height):
                    s.ai.updateNode()
                    s.mPos = pos
                    s.draw()
                    s.ai.updateNode()
                    
    def getAhead(s):
        pos = (s.mPos[0] + (m.cos(s.mAngle)*s.movement), s.mPos[1] - (m.sin(s.mAngle)*s.movement))
        pos = (round(pos[0], 2), round(pos[1], 2))
        #check for objects in way
        canMove = True
        for o in s.ob:
            rec = (o[0], o[0]+1, o[1], o[1]+1)
            rec2 = (pos[0], pos[0]+1, pos[1], pos[1]+1)
            if (rec[0] < rec2[1] and rec[1] > rec2[0] and rec[2] < rec2[3] and rec[3] > rec2[2]):
                #print ("Pos: " + str(pos) + " Object: " + str(o))
                return o
        return False
    
    def __del__(s):
        s.mEnd = True
        s.bc.stop()
        print ("Gui End")
        s.root.after(0, s.root.destroy)
                
t = turtle()
