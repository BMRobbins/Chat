import socket
import sys
from _thread import *
 
HOST = '127.0.0.1'   # Put server Ip address here
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print('Socket now listening')
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #send only takes string

    username = ""
    while True:
        userinput = conn.recv(1024)
        username += userinput.decode()
        if "\r\n" in username:
            username = username.strip("\r\n")
            break
    
    data= "" 
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data1 = conn.recv(1024)
        data += data1.decode()
        if "\r\n" in data:
            reply = username + ": " + data
            data = ""
            for connect in connectionList:
                connect.sendall(str.encode(reply))
     
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
global connectionList
connectionList = []
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    connectionList.append(conn)
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
