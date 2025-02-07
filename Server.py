import socket

serverPort = 12000
serverName = ""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((serverName, serverPort))  # Bind to localhost on port 12345
server_socket.listen(1)
print("Server is listening...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

while True:
    sentence = client_socket.recv(1024).decode()
    if sentence == "exit":
        client_socket.send("EXIT".encode())
        break
    elif sentence == "status":
        client_socket.send("STATUS".encode())
    else:
        capSentence = sentence.upper()
        client_socket.send(capSentence.encode())

client_socket.close()
