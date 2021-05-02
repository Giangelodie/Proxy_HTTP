from socket import *
from threading import *
from datetime import *
from pathlib import *

serverName = '127.0.0.1'
serverPort = 1234
clientPort = 5678


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('proxy ready')

def recv_until(cs, c,ci):
    received = ""
    while True:
        new = cs.recv(4096).decode('utf-8')
        if not new:
            return received
        received+=new
        if new.find(c):
            if((new.split(c,1)[0][0:3])=="GET"):
                return new
            else :
                if((new.split(c,1)[0][0:4])!="HTTP"):
                    return received
                else:
                    ci.sendall(new.encode('utf-8'))

def handle_client(cs):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    clientSocket.connect((serverName, clientPort))
    received = recv_until(cs,'\n', clientSocket)
    with open('log.txt', 'a') as l:
        l.write(received + "\n" + str(datetime.now()) + "\n\n")
    clientSocket.sendall(received.encode('utf-8'))
    received_from_serv=recv_until(clientSocket, '\n', cs)
    lignes = received_from_serv.split("\r\n")
    mots = []
    for i in lignes:
        mots += str(i).split("\n")
    taille = []
    for i in mots:
        taille += str(i).split(" ")
    cpt = 0
    for i in range(len(taille)):
        if taille[i] == "Content-Length:":
            cpt = i + 1
    if cpt:
        with open('log.txt', 'a') as l:
            l.write("\n\n" + received_from_serv + "\n"+ "Taille du fichier: " + taille[cpt] + "\n\n" + "////////////////////////////////////////////////\n")
    else :
        with open('log.txt', 'a') as l:
            l.write(received_from_serv + "\n" + "Taille inconnue" + "\n\n" + "////////////////////////////////////////////////\n")
    cs.sendall(received_from_serv.encode('utf-8'))
    clientSocket.close()
    cs.close()




while True:
    seSocket, address = serverSocket.accept()
    Thread(target=handle_client,args=(seSocket,)).start()
