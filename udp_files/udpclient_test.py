import socket

ip = "127.0.0.1"
port = 7500
msg = "here"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Hello, UDP!"  # message to send

# send message with dynamic ip and port
#def sendMessage(message:str = "default message", ip:str = "127.0.0.1", port:int = 7501) -> None:
print("ip = ", ip)
client_sock.sendto(message.encode(), (ip, port))
print(f"Sent UDP packet to {ip}:{port}: {message}")
