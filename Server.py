import datetime  # for getting current day
import socket
import threading
from dataclasses import dataclass


# Struct for cache
@dataclass
class clientCache:
    connected: bool  # True if client active
    clientName: str  # Defined by client
    serverSideName: str  # "Client##" format set by server
    dateConnected: str  # "yyyy-mm-dd"
    timeConnected: str  # "hh:mm"
    dateFinished: str  # "yyyy-mm-dd"
    timeFinished: str  # "hh:mm"

    def __repr__(self):
        return (
            f"\nClient: {self.clientName}\n"
            f"ServerSideName: {self.serverSideName}\n"
            f"Connected: {self.connected}\n"
            f"Date Accepted: {self.dateConnected}\n"
            f"Time Accepted: {self.timeConnected}\n"
            f"Date Finished: {self.dateFinished}\n"
            f"Time Finished: {self.timeFinished}\n"
        )


# Global variables for client handling
clientList = []  # List for holding current/future clients
clientLimit = 3  # Maximum concurrent clients
clientCounter = 0
lock = threading.Lock()  # Prevents race conditions when modifying shared data

# Initialize server
serverPort = 12000
serverName = ""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((serverName, serverPort))  # Bind to serverName on port serverPort
server_socket.listen(clientLimit)  # Allow up to clientLimit pending connections
print("Server is listening...")


# Function to handle each client in a separate thread
def handle_client(client_socket, addr):
    global clientCounter
    with lock:  # Ensure safe modification of shared variables
        if clientCounter >= clientLimit:
            client_socket.send("Server is full. Try again later.".encode())
            client_socket.close()
            print(f"Client ({addr}) attempted to connect while server at capacity {clientLimit}.")
            return
        else:
            client_socket.send("200".encode())

        # Assign client number
        serverSideName = f"Client{len(clientList) + 1:02d}"
        clientCounter += 1

        # Register client in cache
        currentDateTime = datetime.datetime.now()
        clientCacheInit = clientCache(
            connected=True,
            clientName=str(addr),  # Store as string
            serverSideName=serverSideName,
            dateConnected=currentDateTime.strftime("%Y-%m-%d"),
            timeConnected=currentDateTime.strftime("%H:%M:%S"),
            dateFinished="",
            timeFinished="",
        )
        clientList.append(clientCacheInit)

    print(f"New client connected: {addr} -> {serverSideName}")

    while True:
        try:
            sentence = client_socket.recv(1024).decode()
            if not sentence:
                break  # Handle client disconnect

            # Exit condition
            if sentence.lower() == "exit":
                with lock:  # Ensure safe modification of shared variables
                    for client in clientList:
                        if client.clientName == str(addr):
                            client.connected = False
                            client.dateFinished = datetime.datetime.now().strftime(
                                "%Y-%m-%d"
                            )
                            client.timeFinished = datetime.datetime.now().strftime(
                                "%H:%M:%S"
                            )
                            print(f"Client {addr} ({serverSideName}) disconnected.")
                            break

                client_socket.send("EXIT".encode())
                clientCounter -= 1
                break

            # Status condition
            elif sentence.lower() == "status":
                with lock:
                    status_msg = "\n".join([str(client) for client in clientList])
                client_socket.send(status_msg.encode())

            else:
                # Acknowledge received message
                ackSentence = sentence + " ACK"
                client_socket.send(ackSentence.encode())

        except ConnectionResetError:
            print(f"Client {addr} disconnected unexpectedly.")
            clientCounter -= 1
            break

    client_socket.close()


# Accept and handle multiple clients using threading
while True:
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")

    # Start a new thread for each client
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, addr), daemon=True
    )
    client_thread.start()
