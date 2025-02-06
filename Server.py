import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)
    print("Server is listening...")
    print("Type 'close' to end server")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = client_socket.recv(1024).decode()
        if data:
            # test exit condition:
            # client sent "close" as message
            if data == "close":
                print(f"Received: {data}")
                # special message when exit condition
                print("Goodbye")
                client_socket.send("Server closing")

                # close server socket and end loop
                server_socket.close()
                break

            # non-exit condition proceeds as normal
            print(f"Received: {data}")
            upcased_data = data.upper()
            client_socket.send(upcased_data.encode())

        client_socket.close()

if __name__ == '__main__':
    start_server()
