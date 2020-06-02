
"""Handles receiving of messages."""

l=[]

def recv():
        i=1
        while True:
                try:
                        if(i<=2):
                                msg = client.recv(2048).decode("utf8")
                                print(msg)
                                secmsg = input()
                                client.send(bytes(secmsg,'utf-8'))
                        else:
                                msg = client.recv(2048).decode("utf8")
                                print(msg) 
                                send()
                except OSError:  # Possibly client has left the chat.
                        break
                i+=1

def send(event=None):
        l =[]
        with open("messages.txt",'w',encoding = 'utf-8') as f:
                l = f.readlines()
                newmsg = random.choice(l)

                client.send(bytes(newmsg, "utf8"))
                if newmsg == "{quit}":
                       client.close()


import random              
import socket
from threading import Thread
client = socket.socket()
client.connect(('localhost',33765))

receive_thread = Thread(target=recv)
receive_thread.start()
