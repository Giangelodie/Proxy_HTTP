from socket import *
from threading import *
from datetime import *
from pathlib import *

serverName = '127.0.0.1'
serverPort = 1234
clientPort = 3456

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('proxy ready')

def recv_until(cs, c,ci):
    while True:
        new = cs.recv(4096).decode('utf-8')
        if not new:
            return new
        if new.find(c):
            if((new.split(c,1)[0][0:4])!="HTTP"):
                return new
            else:
                ci.sendall(new.encode('utf-8'))

def handle_client(cs):
    i=0
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    clientSocket.connect((serverName, clientPort))
    received = recv_until(cs,'\n', clientSocket)
    filename = Path(received.split("\n",1)[0].split(" ")[1].lstrip("/"))
    with open("fichiers_interdits.txt","r") as f:
        liste = f.read()
    liste=liste.split(' ')
    for l in liste :
        if (l==received.split("\n",1)[0].split(" ")[1].lstrip("/")):
            i+=1
    if (i==1):
        path1 = Path('avertissement.txt')
        cs.sendall(b"HTTP/1.1 200 OK\nServer: Python HTTP Server\nConnection: close\r\n\r\n")
        with open(str(path1),"br") as f:
            cs.sendall(f.read())
        i=0
    else :
        clientSocket.sendall(received.encode('utf-8'))
        received_from_serv = recv_until(clientSocket, '\n', cs)
        cs.sendall(received_from_serv.encode('utf-8'))
    clientSocket.close()
    cs.close()



while True:
    seSocket, address = serverSocket.accept()
    Thread(target=handle_client,args=(seSocket,)).start()
