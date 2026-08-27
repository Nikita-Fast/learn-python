import socket
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5025))
sock.send(b"*IDN?\n")
print(sock.recv(1024))
sock.close()

time.sleep(1)

sock.connect(("127.0.0.1", 5025))
sock.send(b"*IDN?\n")
print(sock.recv(1024))
sock.close()


# buff = b""
#
# while True:
#     scpi_cmd = input("Enter SCPI command: ")
#     scpi_cmd += "\n"
#
#     # send scpi command
#     sock.send(scpi_cmd.encode())
#
#     # read socket until newline character received
#     while b"\n" not in buff:
#         x = sock.recv(1024)
#         if x:
#             buff += x
#
#             i = buff.find(b"\n")
#             if i != -1:
#                 response = buff[:i+1]
#                 buff = buff[i+1:]
#                 print(f"Response: {repr(response.decode())}")
#                 break



