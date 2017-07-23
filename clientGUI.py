from tkinter import *
import socket   #for sockets
import sys  #for exit
import time
from _thread import *

username = input("Enter username: ")
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print( 'Failed to create socket')
    sys.exit()
     
print('Socket Created')
 
host = "127.0.0.1"# put server ip address here
port = 8888;

#Connect to remote server
s.connect((host , port))
print('Socket Connected to ' + host + ' on ip ' + str(port))
s.send(str.encode(username + "\r\n"))




window = Tk()
window.title("Chat")
window.geometry('100x410')

messages = Text(window)
messages.pack()

def recievethread(conn):
    global messages
    data= ""
    while True:
         
        #Receiving from client
        data1 = conn.recv(1024)
        data += data1.decode()
        if "\r\n" in data:
            data = data.strip("\r\n")
            messages.insert(INSERT, '%s\n' % data)
            data = ""
     
    #came out of loop
    conn.close()

start_new_thread(recievethread, (s,))
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

def Enter_pressed(event):
    input_get = input_field.get()
    s.send(str.encode(input_get + "\r\n"))#
    input_user.set('')
    # label.pack()
    return "break"

frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()

window.mainloop()

