from socket import *

serverName = "servername"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(("", serverPort))
while True:
    sentence = input("Input lowercase sentence:")

    clientSocket.send(sentence.encode())

    modifiedSentence = clientSocket.recv(1024)

    if modifiedSentence.decode() == "EXIT":
        break

    print("From Server:", modifiedSentence.decode())


clientSocket.close()
