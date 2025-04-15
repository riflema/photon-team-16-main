
import socket
import threading

bufferSize          = 1024
msgFromServer       = "Hello UDP Client"            # unused
bytesToSend         = str.encode(msgFromServer)     # unused
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a UDP socket
server_bound = 0
FORMAT = 'utf-8'


# thread action: handle_client() - wait for mesages from clients
def handle_client() -> None:
    while True:
        msg, addr = server_sock.recvfrom(bufferSize)
        print(f"Received message [{msg.decode(FORMAT)}] from [{addr}]")

def start(ip:str = "127.0.0.1", port:int = 7500) -> None:
    global server_bound
    if server_bound == 0:
        server_sock.bind((ip, port))                                      # bind socket
        server_bound = 1

        print(f"Listening for UDP packets on {ip}:{port}")

        # Receive data from client, but in a thread
        thread = threading.Thread(target=handle_client)
        thread.start()
