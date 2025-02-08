import socket
from dataclasses import dataclass
import datetime # for getting current day
import time

# struct for cache
# this might be overkill
@dataclass
class clientCache:
    connected: bool # true if client active
    clientName: str # defined by client
    serverSideName: str # "Client##" format set by server (when connected)
    dateConnected: str # "yyyy-mm-dd"
    timeConnected: str # "hh:mm"
    dateFinished: str # "yyyy-mm-dd"
    timeFinished: str # "hh:mm"

    # magic function, return contents of class object when class called
    # prints over 2 lines
    def __repr__(self):
        print("Client: {} ServerSideName: {} Connected: {}\nDate Accepted: {} Time Accepted: {} Date Finished: {} Time Finished: {}"
              .format(self.clientName, self.serverSideName, self.connected, self.dateConnected, self.timeConnected, self.dateFinished, self.timeFinished))


# client cache variables
clientList = list[clientCache()] # list for holding current/future clients
clientLimit = 3 # assumed limit of 3
clientConcurrent = 0 # init server with 0 connected clients

# init server variables
serverPort = 12000
serverName = ""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((serverName, serverPort))  # Bind to serverName on port serverPort
server_socket.listen(1)
print("Server is listening...")

# client handling
# todo: client assign name
# todo: client limit (3)
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# get current date and time for client connection init
currentDateTime = datetime.now()

# successful client connection, add to clientList
# todo: check implementation of datetime format (strftime)
clientCacheInit = clientCache(connected = True,
                            clientName = addr, # client might want to add/change name later?
                            serverSideName = "Client01", # adjust for multiple clients
                            dateConnected = currentDateTime.strftime("%d-%m-%Y %p"),
                            timeConnected = currentDateTime.strftime("%H:%M:%S"),
                            dateFinished = "",
                            timeFinished = "",)

# todo: limit clientList size based on clientLimit (3)
clientList += clientCacheInit

# main server loop
# todo: multi-threading
# todo: cache
# cache: accepted clients during session, date and time accepted, date and time finished
while True:
    sentence = client_socket.recv(1024).decode()

    # exit condition: 
    # client sent "exit" as message
    # stop server
    # todo: change to stop client
    # different way to close server?
    if sentence == "exit":
        # update dateFinished, timeFinished in client cache
        # todo: actual way to identify current client and not hard coded
        # todo: check if above strftime format works for below
        clientNum = 0
        currentDateTime = datetime.now()
        clientList[clientNum].connected = False
        clientList[clientNum].serverSideName = "" # clear Client## from cache
        clientList[clientNum].dateFinished = currentDateTime.strftime("%d-%m-%Y %p")
        clientList[clientNum].timeFinished = currentDateTime.strftime("%H:%M:%S")

        client_socket.send("EXIT".encode())
        break # end loop

    # status condition
    elif sentence == "status":
        # print content of each entry in cache from clientList
        # todo: check if this works lol
        for i in len(clientList):
            clientList[i]

        client_socket.send("STATUS".encode())
    else:
        # no special condition
        # return input with ACK appended
        ackSentence = sentence + " ACK"
        client_socket.send(ackSentence.encode())

# server loop ends, close socket
client_socket.close()
server_socket.close()

