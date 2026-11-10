import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 5025

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen()

print(f"[+] Listening on port {bind_ip} : {bind_port}")

#client handling thread
def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        print(f"[+] Recieved: {request}")
        if len(request) == 0:
            print("Client closed connection")
            break

        cmd = request.decode().lower()

        match cmd:
            case "*idn?\n":
                response = "K02 device\n"
            case "freq?\n":
                response = "100500 khz\n"
            case _:
                response = "error: unknown command\n"

        client_socket.send(response.encode())
    
while True:
    client, addr = server.accept()
    print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
    #spin up our client thread to handle the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()