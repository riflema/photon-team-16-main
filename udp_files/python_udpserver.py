# import socket

# localIP     = "127.0.0.1"
# localPort   = 20001
# bufferSize  = 1024
# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)

# # Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPServerSocket.bind((localIP, localPort))

# print("UDP server up and listening")

# # Listen for incoming datagrams

# while(True):

#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)
    
#     print(clientMsg)
#     print(clientIP)

#     # Sending a reply to client
#     UDPServerSocket.sendto(bytesToSend, address)


# provided by Strother ^


import socket
import threading

bufferSize          = 1024
msgFromServer       = "Hello UDP Client"            # unused
bytesToSend         = str.encode(msgFromServer)     # unused
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a UDP socket
FORMAT = 'utf-8'


# thread action: handle_client() - wait for mesages from clients
def handle_client() -> None:
    while True:
        msg, addr = server_sock.recvfrom(bufferSize)
        print(f"Received message [{msg.decode(FORMAT)}] from [{addr}]")


def start(ip:str = "127.0.0.1", port:int = 7500) -> None:
    server_sock.bind((ip, port))                                      # bind socket
    print(f"Listening for UDP packets on {ip}:{port}")

    # Receive data from client, but in a thread
    thread = threading.Thread(target=handle_client)
    thread.start()