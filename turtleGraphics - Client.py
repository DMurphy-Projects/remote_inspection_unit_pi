import socket
#example connect stuffs
TCP_IP = 'localhost'
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
_exit = False
command = None
para = None

while True:
    command = raw_input("Command: ")    
    sock.send( str(len(command)).ljust(4))
    sock.send( command )
    if command == "exit":
        break      

sock.close()
