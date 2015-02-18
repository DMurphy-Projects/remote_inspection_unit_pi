#from bluetooth import *
#import socket
import sys

class BluetoothConnection:
    UUID = "42656e20-6c6f-7665-7320-636f636b7321"
    mPort = 20
    mServerSock = None
    mIp = ""
    
    mClient = None
    mClientSock = None

    mEnd = False
    
    def __init__(s, local):
        if local:
            import socket
            s.mServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.mIp = "localhost"
        else:
            from bluetooth import *
            s.mServerSock = BluetoothSocket( RFCOMM )
            advertise_service( s.mSeverSock, "RemoteInspectionService",
                   service_id = s.UUID,
                   service_classes = [ s.UUID, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])
            
        s.mServerSock.bind((s.mIp, s.mPort))
        s.mServerSock.listen(1)
        s.mServerSock.settimeout(1)
        
    def connect(s):
        sys.stdout.write("Waiting for Connection")
        while not s.mEnd:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                s.mClientSock, s.mClient = s.mServerSock.accept()
                s.mClientSock.settimeout(1)
                break
            except IOError:
                pass
        print "\nConnected : ", s.mClient
        
    def recieve(s):
        while not s.mEnd:
            try:
                data = s.mClientSock.recv(1024)
                if len(data) == 0:
                    print "Disconnected"
                    s.mClientSock.close()
                    s.connect()
                else:
                    print "Received : %s" % data
                    return data
            except IOError:
                pass

    def stop(s):
        s.mEnd = True
    
    def __del__(s):
        print "Server Ending"
        if s.mClientSock is not None:
            s.mClientSock.close()
        if s.mServerSock is not None:
            s.mServerSock.close()
