

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Hello, UDP!"  # message to send

# send message with dynamic ip and port
def sendMessage(message:str = "default message", ip:str = "127.0.0.1", port:int = 7500) -> None:
    print("ip = ", ip)
    sock.sendto(message.encode(), (ip, port))
    print(f"Sent UDP packet to {ip}:{port}: {message}")
