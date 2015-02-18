import socket

TCP_IP = 'localhost'
TCP_PORT = 20

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
_exit = False
command = None

while True:
    command = raw_input("Command: ")    
    sock.send( command.encode() )
    if command == "exit":
        break      

sock.close()
