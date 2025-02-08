from socket import socket, AF_INET, SOCK_STREAM

# defined server name and port
serverName = "servername"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

# client attempts to connect to server
# error handling if client could not connect?
# try:
clientSocket.connect(("", serverPort))
# except:
#    print("Failed to connect")

# main client loop while socket open
while True:
    # user input prompt
    sentence = input("Input sentence:")

    # send user input to server
    clientSocket.send(sentence.encode())

    # receive server response
    modifiedSentence = clientSocket.recv(1024)
    modifiedSentenceData = modifiedSentence.decode()

    # exit condition
    if modifiedSentenceData == "EXIT":
        break

    elif modifiedSentenceData == "STATUS":
        # todo: print status of cache from server?
        continue

    # no special condition:
    # server should return input with "ACK" appended
    print("From Server:", modifiedSentence.decode())

# after finished, close socket
# todo: ensure it is freed up on server side?
clientSocket.close()
