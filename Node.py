#0.1.0
class Node:
    mX = 0
    mY =  0
    mParent = None
    mDir = None
    
    def __init__(s, x, y):
        s.mX = x
        s.mY = y
        s.mDir = [0, 1, 2, 3]
    def remove(s, num):
        s.mDir.remove(num)
        
