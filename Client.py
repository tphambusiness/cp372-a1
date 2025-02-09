from socket import socket, AF_INET, SOCK_STREAM

# defined server name and port
serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

# main client loop while socket open

connectionMessage = clientSocket.recv(1024).decode()
if connectionMessage == "200":
    flag = True

else:
    flag = False
    print(connectionMessage)


while flag:
    # user input prompt
    sentence = input("Input sentence (Keywords: 'status', 'exit'): ")

    # send user input to server
    clientSocket.send(sentence.encode())

    # receive server response
    modifiedSentence = clientSocket.recv(1024)
    modifiedSentenceData = modifiedSentence.decode()

    # exit condition
    if modifiedSentenceData == "EXIT":
        break

    # status condition
    elif modifiedSentenceData == "STATUS":
        continue

    # no special condition:
    # server should return input with "ACK" appended
    print("From Server:", modifiedSentence.decode())

# after finished, close socket
clientSocket.close()
