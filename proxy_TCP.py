from socket import *
from threading import *


serverName = '127.0.0.1'
serverPort = 1234
clientPort = 5678



serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('proxy ready')

def handle_client(servSocket):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    clientSocket.connect((serverName, clientPort))
    delay = 5
    while True:
        servSocket.settimeout(delay)
        try:
            received = servSocket.recv(4096)
        except timeout:
            servSocket.close()
            clientSocket.close()
            break
        if not received:
            servSocket.close()
            clientSocket.close()
            break
        else:
            clientSocket.sendall(received)
            received_from_serv=clientSocket.recv(2048)
            print(received_from_serv)
            servSocket.sendall(received_from_serv)


while True:
    seSocket, address = serverSocket.accept()
    Thread(target=handle_client,args=(seSocket,)).start()
