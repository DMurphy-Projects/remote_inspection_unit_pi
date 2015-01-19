from Tkinter import *
import threading as t
import time
import math as m
import random as r
import socket

#python version: 2.7
class turtle:
    height = 20#of field
    width = 20
    pos = (2, 2)
    angle = 6.28
    ob = [(2, 1), (2, 3), (2, 5), (2, 7)]#obstacles
    #ob = [(5, 5)]
    aiState = 0#0 off, 1 on, 2 end
    movement = 1#many blocks turtle moves by
    end = False
    
    TCP_IP = 'localhost'
    TCP_PORT = 5001
    sock = None#socket
    conn = None
    
    def __init__(s):
        s.root = Tk()
        s.canvas = Canvas(s.root, width=s.width*10, height=s.height*10)
        s.canvas.pack()
        s.canvas.create_rectangle(0, 0, s.width*10, s.height*10, fill='white')
        s.rec = s.canvas.create_rectangle(0, 0, 0, 0, fill='black')
        s.line = s.canvas.create_line(0, 0, 0, s.width)
        s.userControlled()
        s.root.protocol("WM_DELETE_WINDOW", s.__del__)
        s.clientThread = t.Thread(target = s.clientControlled)#client on own thread/client being remote user
        s.clientThread.start()
        s.aiThread = t.Thread(target = s.ai)#ai on own thread
        s.aiThread.start()
        s.draw()
        for o in s.ob:
            x = ((o[0]+1)*10)-10
            y = ((o[1]+1)*10)-10
            s.canvas.create_rectangle(x, y, x+10, y+10)
        s.root.mainloop()
        
    def ai(s):#stupid ai, thread 01
        while not s.end:
            if s.aiState == 0:
                pass#pause state
            elif s.aiState == 1:
                rNum = r.randint(0, 99)
                if rNum >=0 and rNum < 75:
                    s.move(moves=r.randint(1, 10))
                elif rNum >= 75 and rNum < 87:
                    s.turnRight(angle=r.uniform(0, m.pi/2))
                else:
                    s.turnLeft(angle=r.uniform(0, m.pi/2))
            else:
                s.end = True
            time.sleep(1)
        print("Ai Thread End")

    def recLength(s):#blocks thread with control
        length = False
        while not length:
            length = s.recvall(s.conn,4)
            if length or s.end:break
        return length
    #0 forward, 1 turnRight, 2 turnLeft, eg 010(forward 10)
    def clientControlled(s):#thread 02
        s.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.sock.bind((s.TCP_IP, s.TCP_PORT))
        s.sock.listen(True)
        s.sock.settimeout(True)
        print "Waiting for Con"
        while not s.end:
            try:
                s.conn, addr = s.sock.accept()
                print "Connected"
                break
            except: pass
        if not s.end:
            s.conn.settimeout(True)
            while not s.end:
                length = s.recLength()
                if s.end:break
                data = s.recvall(s.conn, int(length))
                print ("command " + str(data))
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
                        para = (para/360) * (2*m.pi)
                        if command == "1": s.turnRight(angle=para)
                        elif command == "2": s.turnLeft(angle=para)
                else:
                    s.__del__()
        print ("Client Thread End")
            
    def userControlled(s):
        def aiToggle(e):
            if s.aiState == 0:
                s.aiState = 1
            else:
                s.aiState = 0
            print (s.aiState)
        def userEnd(e):
            s.__del__()
        frame = Frame(s.root, width=0, height=0)
        frame.bind("<Up>", s.move)
        frame.bind("<Left>", s.turnLeft)
        frame.bind("<Right>", s.turnRight)
        frame.bind("<Return>", aiToggle)
        frame.bind("<Escape>", userEnd)
        frame.pack()
        frame.focus_set()
    
    def draw(s):
        x = ((s.pos[0]+1)*10)-10
        y = ((s.pos[1]+1)*10)-10
        lineX = ((s.pos[0] + m.cos(s.angle)+1)*10)-10
        lineY = ((s.pos[1] - m.sin(s.angle)+1)*10)-10
        s.canvas.delete(s.rec)
        s.rec = s.canvas.create_rectangle(x, y, x+9, y+9, fill='black')
        s.canvas.delete(s.line)
        s.line = s.canvas.create_line(x+5, y+5, lineX+5, lineY+5, fill="red")            
    
    def turnLeft(s, event=None, angle=m.pi/2):#90deg=pi/2, etc
        s.angle = s.angle + angle
        if s.angle > 2*m.pi:
            s.angle = 0 + s.angle-2*m.pi
        s.angle = round(s.angle, 2)
        #print(s.angle)
        s.draw()

    def turnRight(s, event=None, angle=m.pi/2):
        s.angle = s.angle - angle
        if s.angle <= 0:
            s.angle = 2*m.pi + s.angle
        s.angle = round(s.angle, 2)
        #print(s.angle)
        s.draw()

    def move(s, event=None, moves=1):
        for x in range(0, moves):
            pos = (s.pos[0] + (m.cos(s.angle)*s.movement), s.pos[1] - (m.sin(s.angle)*s.movement))
            pos = (round(pos[0], 2), round(pos[1], 2))
	    #check for objects in way
            canMove = True
            for o in s.ob:
                rec = (o[0], o[0]+1, o[1], o[1]+1)
                rec2 = (pos[0], pos[0]+1, pos[1], pos[1]+1)
                if (rec[0] < rec2[1] and rec[1] > rec2[0] and rec[2] < rec2[3] and rec[3] > rec2[2]):
                    print ("Pos: " + str(pos) + " Object: " + str(o))
                    canMove = False
                    break
	    #check inside field
            if (canMove):
                if (pos[0] >= 0 and pos[0]+1 <= s.width and pos[1] >= 0 and pos[1]+1 <= s.height):
                    s.pos = pos
                    s.draw()

    #for local host receiving
    def recvall(s, sock, count):
        try:
            buf = b''
            while count:
                newbuf = sock.recv(count)
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
            return buf
        except:
            return False
    
    def __del__(s):
        s.end = True
        if s.sock is not None:
            print ("Socket End")
            s.sock.close()
        print ("Gui End")
        s.root.after(0, s.root.destroy)
                
t = turtle()


