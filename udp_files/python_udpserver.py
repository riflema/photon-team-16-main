
import socket
import threading

bufferSize          = 1024
msgFromServer       = "Hello UDP Client"            # unused
bytesToSend         = str.encode(msgFromServer)     # unused
server_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)         # Create a UDP socket
FORMAT = 'utf-8'
broadcast_addr = ("127.0.0.1", 7500)


# thread action: handle_client() - wait for mesages from clients
def handle_client() -> None:
    while True:
        msg, addr = server_sock.recvfrom(bufferSize)
        msg = msg.decode(FORMAT)
        print(f"Received message [{msg}] from [{addr}]")

        if msg.count(":") <= 0:                                         # received only equipment ID
            equipID = msg

            response = f"Received equipment ID: {equipID}"

            # return to sender
            server_sock.sendto(response.encode(FORMAT), broadcast_addr)

            print(f"Sent [{response}] to {addr}")

        else:
            msg_parts = msg.split(":")
            equipID = msg_parts[0]
            value_2 = msg_parts[1]

            if value_2 == 53:                                         # green scored pts

                # red base has been scored on
                # if player is on green team, player receives 100 pts & stylized 'B' @ codename

                # link to database for scoring

                response = f"Player {equipID} scored on RED base"

            elif value_2 == 43:                                       # red scored pts

                # green base has been scored on
                # if player is on red team, player receives 100 pts & stylized 'B' @ codename

                # link to game_action_gui for scoring

                response = f"Player {equipID} scored on GREEN base"

            else:                                                       # player hits player
                # link to game_action_gui for scoring
                
                response = f"Received equipment ID: {equipID} and {value_2}"


            # broadcast response for traffic generator
            server_sock.sendto(response.encode(FORMAT), broadcast_addr)

            print(f"Sent [{response}] to {addr}")
        

def start(ip:str = "127.0.0.1", port:int = 7501) -> None:
    server_sock.bind((ip, port))                                      # bind socket
    print(f"Listening for UDP packets on {ip}:{port}")

    # Receive data from client, but in a thread
    thread = threading.Thread(target=handle_client)
    thread.start()
