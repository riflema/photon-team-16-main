# import socket

# msgFromClient       = "Hello UDP Server"
# bytesToSend         = str.encode(msgFromClient)
# serverAddressPort   = ("127.0.0.1", 7501)
# bufferSize          = 1024

# # Create a UDP socket at client side
# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Send to server using created UDP socket
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)
# msg = "Message from Server {}".format(msgFromServer[0])

# print(msg)


# provided by Strother ^


import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Hello, UDP!"  # message to send

# send message with dynamic ip and port
def sendMessage(message:str = "default message", ip:str = "127.0.0.1", port:int = 7501) -> None:
    print("ip = ", ip)
    sock.sendto(message.encode(), (ip, port))
    print(f"Sent UDP packet to {ip}:{port}: {message}")
