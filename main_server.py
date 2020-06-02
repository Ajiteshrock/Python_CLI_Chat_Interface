import time
import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import hashlib
import itertools
import sys
'''from Crypto import Random
from Crypto.PublicKey import RSA
from CryptoPlus.Cipher import IDEA'''

ports={}
clients = {}

def adding_clients():
    while True:
        client , cli_port = server.accept()
        print("The client with the port is connected"+str(cli_port))
        client.send(bytes("Hey ! Now you are connected Enter your name","utf-8"))
        ports[client] = cli_port
        Thread(target = handling_client ,args=(client,)).start()

def handling_client(client):
    
    name = client.recv(1024).decode()
    clients[client] = name
    print(clients[client])

    while True:
        client.send(bytes("Enter your message as public key",'utf-8'))
        #client's message(Public Key)
        get_key = client.recv(2048).decode("utf-8")
        #print(get_key)

        #conversion of string to KEY
        server_public_key = RSA.importKey(get_key)

        #hashing the public key in server side for validating the hash from client
        hash_object = hashlib.sha1(get_key)
        hex_digest = hash_object.hexdigest()

        if get_key != "":
            #print (get_key)
            client.send("YES")
            gethash = client.recv(1024)
           
        if hex_digest == gethash:
            # creating session key
            key_128 = os.urandom(16)
            #encrypt CTR MODE session key
            en = AES.new(key_128,AES.MODE_CTR,counter = lambda:key_128)
            encrypto = en.encrypt(key_128)
            #hashing sha1
            en_object = hashlib.sha1(encrypto)
            en_digest = en_object.hexdigest()
            E = server_public_key.encrypt(encrypto,16)
            client.sned(bytes("enter the new message"))
            newmess = client.recv(1024)
        #decoding the message from HEXADECIMAL to decrypt the ecrypted version of the message only
            decoded = newmess.decode("hex")
        #making en_digest(session_key) as the key
            key = en_digest[:16]
        #print ("\nENCRYPTED MESSAGE FROM CLIENT -> "+newmess)
        #decrypting message from the client
            ideaDecrypt = IDEA.new(key, IDEA.MODE_CTR, counter=lambda: key)
            dMsg = ideaDecrypt.decrypt(decoded)
       # print ("\n**New Message**  "+time.ctime(time.time()) +" > "+dMsg+"\n")
            if(dMsg[0]=="$"):
                    mess = input("\n Okay this is a linux working command   ")
                    if mess != "":
                        ideaEncrypt = IDEA.new(key, IDEA.MODE_CTR, counter=lambda : key)
                        eMsg = ideaEncrypt.encrypt(mess)
                        eMsg = eMsg.encode("hex").upper()
                        if eMsg != "":
                    #print ("ENCRYPTED MESSAGE TO CLIENT-> " + eMsg)
                            client.send(eMsg)
            else:

                mess = input("\n Hello let's chat now   ")
                if mess != "":
                    ideaEncrypt = IDEA.new(key, IDEA.MODE_CTR, counter=lambda : key)
                    eMsg = ideaEncrypt.encrypt(mess)
                    eMsg = eMsg.encode("hex").upper()
                if eMsg != "":
                    #print ("ENCRYPTED MESSAGE TO CLIENT-> " + eMsg)
                    client.send(eMsg)



            client.close()
        else:
            print ("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")



HOST = 'localhost'
PORT =  33765
BUFSIZ = 1024
ADDR = (HOST, PORT)

server = socket()
server.bind(ADDR)

if __name__ == "__main__":
    server.listen(20)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=adding_clients)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()