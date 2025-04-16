

import socket
import threading
from game_action_gui import Game_Action_GUI as Game_Action_GUI

bufferSize          = 1024
msgFromServer       = "Hello UDP Client"            # unused
bytesToSend         = str.encode(msgFromServer)     # unused
server_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)         # Create a UDP socket
server_bound = 0
FORMAT = 'utf-8'
broadcast_addr = ("127.0.0.1", 7500)


# thread action: handle_client() - wait for mesages from clients
def handle_client(game_action_gui:Game_Action_GUI) -> None:
    while True:
        msg, addr = server_sock.recvfrom(bufferSize)
        print(f"Received message [{msg.decode(FORMAT)}] from [{addr}]")

        msg_2 = msg.decode(FORMAT)

        has_colon = msg_2.count(':')

        if has_colon <= 0:                        # received only equipment ID
            equipID = msg_2

            response = (f"Received equipment ID: {equipID}")

            # return to sender
            server_sock.sendto(response.encode(FORMAT), broadcast_addr)

            print(f"Sent [{response}] to {addr}")

        else:
            msg_parts = msg_2.split(':')
            equipID = msg_parts[0]
            value_2 = int(msg_parts[1])

            if value_2 == 53:                                         # green scored pts

                # red base has been scored on
                # if player is on green team, player receives 100 pts & stylized 'B' @ codename

                # link to database for scoring

                game_action_gui.add_new_base_hit(int(equipID), 0)
                response = (f"Player {equipID} scored on RED base")

            elif value_2 == 43:                                       # red scored pts

                # green base has been scored on
                # if player is on red team, player receives 100 pts & stylized 'B' @ codename

                # link to game_action_gui for scoring

                game_action_gui.add_new_base_hit(int(equipID), 1)
                response = (f"Player {equipID} scored on GREEN base")

            else:                                                       # player hits player
                # link to game_action_gui for scoring
                
                game_action_gui.add_new_hit(int(equipID), int(value_2))
                response = (f"Received equipment ID: {equipID} and {str(value_2)}")


            # broadcast response for traffic generator
            server_sock.sendto(response.encode(FORMAT), broadcast_addr)

            print(f"Sent [{response}] to {addr}")
        

def start(new_gui:Game_Action_GUI, ip:str = "127.0.0.1", port:int = 7501) -> None:
    global server_bound

    game_action_gui = new_gui

    if server_bound == 0:
        server_bound = 1
        server_sock.bind((ip, port))                                      # bind socket
        print(f"Listening for UDP packets on {ip}:{port}")
        
        # Receive data from client, but in a thread
        thread = threading.Thread(target=handle_client, args=(game_action_gui,))
        thread.start()
