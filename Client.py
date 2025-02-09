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
    sentence = input("Input sentence (type 'help' to list keywords): ")

    # 'help' keyword condition
    # do not send anything to server, list keywords for client when prompted
    if sentence == "help":
        print("""
    'status': print list of clients
    'list': list files from server directory
    note: type in file name (with extension) from 'list' for server to stream file to client
    'exit': close client connection
        """)
        continue

    # white space condition
    # do not send to server, provide error
    elif sentence == "" or sentence == "\n" or sentence == "\t":
        print("Invalid message")
        continue

    # send user input to server
    clientSocket.send(sentence.encode())

    # receive server response
    modifiedSentence = clientSocket.recv(1024)
    modifiedSentenceData = modifiedSentence.decode()

    # conditions when client types in keywords:
    # 'exit' keyword condition
    if modifiedSentenceData == "EXIT":
        break

    # 'status' and 'list' keyword condition: server sends specialized message, instead of message + ACK
    # no keyword condition:
    # server should send input with "ACK" appended
    print("From Server:", modifiedSentence.decode())

# after finished, close socket
clientSocket.close()
