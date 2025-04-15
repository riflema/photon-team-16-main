from tkinter import *
from typing import List, Tuple, Union, Any
import sys
from udp_files import python_udpserver, python_udpclient, python_trafficgenarator_v2
from game_action_gui import Game_Action_GUI as Game_Action_GUI
from game_start_countdown import run_countdown as Game_Start_Countdown
import psycopg2
from psycopg2 import sql

connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

class Player_Entry_GUI:
    def __init__(self) -> None:
        self.root = Tk()
                               #codename, player exist?, player id, equipment id
        self.red_team:List[Tuple[StringVar, BooleanVar, StringVar, StringVar]] = [] #Each player is index in list
        self.green_team:List[Tuple[StringVar, BooleanVar, StringVar, StringVar]] = []
        self.selected_player:int = 0
        self.arrow = PhotoImage(file="gui_sprites/player_select_arrow.png")
        self.equiproot:Any = ''
        self.iproot:Any = ''
        self.ip = "127.0.0.1"

        self.root.title('Entry Terminal')
        self.root.configure(bg='black')

        self.create_main()

        self.root.mainloop()

    def quit(self) -> None:
        sys.exit()

    #Clear GUI
    def clear(self) -> None:
        list = self.root.pack_slaves()
        for l in list:
            l.destroy()
        list = self.root.grid_slaves()
        for l in list:
            l.destroy()

    #Create each player check box and entry field
    def create_player(self, team_entry:Frame, color:str, num:int) -> None:
        #Set up new player frame
        if (color == 'red4'):
            new_player_entry = Frame(team_entry, bg=color, name="red_" + str(num))
        if (color == 'green4'):
            new_player_entry = Frame(team_entry, bg=color, name="green_" + str(num))
        new_player_entry.pack()
        is_player = BooleanVar()
        player_name = StringVar()
        player_id = StringVar()
        equip_id = StringVar()
        num_str = str(num)
        if (num < 10):
            num_str = str(num) + "  "

        #Add red player
        if (color == 'red4'):
            if (num == 0):
                Label(new_player_entry, bg='red4', image=self.arrow, name="select_space").pack(side=LEFT)
            else:
                Label(new_player_entry, bg='red4', text= "  ", name="select_space").pack(side=LEFT)
            Checkbutton(new_player_entry, text=num_str, bg=color, borderwidth=0, highlightthickness=0, variable=is_player, justify=LEFT, onvalue=1, offvalue=0).pack(side=LEFT)
            player_id_entry = Entry(new_player_entry, bg='lightgray', textvariable=player_id, width=15, relief=FLAT, name="player_id")
            player_id_entry.pack(side=LEFT)
            player_id_entry.bind('<Return>', lambda event: self.submit_player_id(num, color))
            codename_entry = Entry(new_player_entry, bg='lightgray', textvariable=player_name, relief=FLAT, name="codename")
            codename_entry.pack(side=LEFT, padx=5, pady=2)
            codename_entry.bind('<Return>', lambda event: self.submit_codename(player_name.get(), player_id.get(), color, num))
            self.red_team.append((player_name, is_player, player_id, equip_id))

        #Add green player
        if (color == 'green4'):
            Label(new_player_entry, bg='green4', text= "  ", name="select_space").pack(side=LEFT)
            Checkbutton(new_player_entry, text=num_str, bg=color, borderwidth=0, highlightthickness=0, variable=is_player, onvalue=1, offvalue=0).pack(side=LEFT)
            player_id_entry = Entry(new_player_entry, bg='lightgray', textvariable=player_id, width=15, relief=FLAT, name="player_id")
            player_id_entry.pack(side=LEFT)
            player_id_entry.bind('<Return>', lambda event: self.submit_player_id(num, color))
            codename_entry = Entry(new_player_entry, bg='lightgray', textvariable=player_name, relief=FLAT, name="codename")
            codename_entry.pack(side=LEFT, padx=5, pady=2)
            codename_entry.bind('<Return>', lambda event: self.submit_codename(player_name.get(), player_id.get(), color, num))
            self.green_team.append((player_name, is_player, player_id, equip_id))
    
    def move_up(self) -> None:
        self.root.focus()
        if (int(self.selected_player / 2) - 1 > -1):
            #move up on red side if red
            if (self.selected_player % 2 == 0):
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".select_space").config(image="", text="  ")
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2) - 1) + ".select_space").config(image=self.arrow, text="")
            #move up on green side if green
            else:
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".select_space").config(image="", text="  ")
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2) - 1) + ".select_space").config(image=self.arrow, text="")
            self.selected_player -= 2
    
    def move_down(self) -> None:
        self.root.focus()
        if (self.selected_player + 2 < 32):
            self.selected_player += 2
        if (int(self.selected_player / 2) - 1 > -1):
            #move down on red side if red
            if (self.selected_player % 2 == 0):
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".select_space").config(image=self.arrow, text="")
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2) - 1) + ".select_space").config(image="", text="  ")
            #move down on green side if green
            else:
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".select_space").config(image=self.arrow, text="")
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2) - 1) + ".select_space").config(image="", text="  ")

    def move_left(self) -> None:
        self.root.focus()
        #move arrow to left side
        if ((self.selected_player - 1) % 2 == 0):
            self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".select_space").config(image="", text="  ")
            red_player:int = 0
            for player_num in range(len(self.red_team)):
                if (self.red_team[player_num][1].get() == False):
                    red_player = player_num
                    break
            self.root.nametowidget(".player_entry.teams.red_team.red_" + str(red_player) + ".select_space").config(image=self.arrow, text="")
            self.selected_player = red_player * 2

    def move_right(self) -> None:
        self.root.focus()
        #move arrow to right side
        if ((self.selected_player + 1) % 2 != 0):
            self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".select_space").config(image="", text="  ")
            green_player:int = 0
            for player_num in range(len(self.green_team)):
                if (self.green_team[player_num][1].get() == False):
                    green_player = player_num
                    break
            self.root.nametowidget(".player_entry.teams.green_team.green_" + str(green_player) + ".select_space").config(image=self.arrow, text="")
            self.selected_player = green_player * 2 + 1

    #Send new name to database
    def send_to_database(self, player_id:int, codename:str) -> None:
        try:
            conn = psycopg2.connect(**connection_params)
            cursor = conn.cursor()

            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Connected to - {version}")

            cursor.execute('''
                INSERT INTO players (id, codename)
                VALUES (%s, %s);
            ''', (player_id, codename))
            
            conn.commit()
        except Exception as error:
            print(f"Error connecting to PostgreSQL database: {error}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    #Ask database for name and return it if it exists
    def query_codename_database(self, player_id:int) -> Union[str, None]:
        try:
            conn = psycopg2.connect(**connection_params)
            cursor = conn.cursor()

            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Connected to - {version}")

            cursor.execute('''SELECT * FROM players WHERE id = (%s);
            ''', (player_id,))
            player = cursor.fetchone()

            if (player != None):
                return str(player[1])
            else:
                return None

        except Exception as error:
            print(f"Error connecting to PostgreSQL database: {error}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return None
    
    #Tell database about new codename/move down to next player and ask for equipment id
    def submit_codename(self, codename:str, player_id:str, color:str, num:int) -> None:
        self.send_to_database(int(player_id), codename)
        self.move_down()
        self.get_equipment_id(num, color)

    #Submit player id to database to find out if codename, then enter codename if not
    def submit_player_id(self, num:int, color:str) -> None:
        if (color == 'red4'):
            red_codename:Union[str, None] = self.query_codename_database(int(self.red_team[num][2].get()))
            if (red_codename == None):
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".codename").focus()
                return None
            self.red_team[num][0].set(str(red_codename))
        if (color == 'green4'):
            green_codename:Union[str, None] = self.query_codename_database(int(self.green_team[num][2].get()))
            if (green_codename == None):
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".codename").focus()
                return None
            self.green_team[num][0].set(str(green_codename))
        self.move_down()
        self.get_equipment_id(num, color)

    #Auto-check next player and select field to input name by pressing <Insert>
    def insert_player(self) -> None:
        #if red
        if (self.selected_player % 2 == 0):
            if (self.red_team[int(self.selected_player / 2)][1].get() == True):
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".codename").focus()
            elif (self.red_team[int(self.selected_player / 2) - 1][1].get() == True or self.selected_player == 0):
                self.red_team[int(self.selected_player / 2)][1].set(True)
                self.root.nametowidget(".player_entry.teams.red_team.red_" + str(int(self.selected_player / 2)) + ".player_id").focus()

        #if green
        else:
            if (self.green_team[int(self.selected_player / 2)][1].get() == True):
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".codename").focus()
            elif (self.green_team[int(self.selected_player / 2) - 1][1].get() == True or self.selected_player == 1):
                self.green_team[int(self.selected_player / 2)][1].set(True)
                self.root.nametowidget(".player_entry.teams.green_team.green_" + str(int(self.selected_player / 2)) + ".player_id").focus()

    #Delete last player and select field of previous player name by pressing <Delete>
    def delete_player(self) -> None:
        #if red
        if (self.selected_player % 2 == 0):
            self.red_team[int(self.selected_player / 2)][0].set("")
            self.red_team[int(self.selected_player / 2)][1].set(False)
            self.red_team[int(self.selected_player / 2)][2].set("")
            self.red_team[int(self.selected_player / 2)][3].set("")

        #if green
        else:
            self.green_team[int(self.selected_player / 2)][0].set("")
            self.green_team[int(self.selected_player / 2)][1].set(False)
            self.green_team[int(self.selected_player / 2)][2].set("")
            self.green_team[int(self.selected_player / 2)][3].set("")

        self.move_up()

    #Create Equipment ID entry GUI
    def get_equipment_id(self, num:int, color:str) -> None:
        self.equiproot = Toplevel(self.root)
        self.equiproot.title("Equipment ID Entry")
        equip_frame = Frame(self.equiproot, bg='black')
        equip_label = Label(equip_frame, text="Enter integer equipment id:", bg='black', fg='lime')
        equip_id_str = StringVar()
        equip_entry = Entry(equip_frame, textvariable=equip_id_str, bg='lightgray', relief=FLAT)
        equip_frame.pack()
        equip_label.pack(side=LEFT)
        equip_entry.pack(side=LEFT)
        equip_entry.focus()
        equip_entry.bind('<Return>', lambda event: self.equipment_id_set(num, color, equip_id_str.get()))

    #Set equipment ID in lists, then destroy GUI/Should also send equipment id to database
    def equipment_id_set(self, num:int, color:str, equip_id:str) -> None:
        if (color == 'red4'):
            self.red_team[num][3].set(str(int(equip_id)))
        if (color == 'green4'):
            self.green_team[num][3].set(str(int(equip_id)))
        
                # Send the equipment code to the server
        python_udpclient.sendMessage(equip_id, self.ip, 7500)
        
        self.equiproot.destroy()

    #Placeholder for "Edit Game" function
    def edit_game(self) -> None:
        print("Edit game")

    #Placeholder for "Game Parameters" function
    def game_parameters(self) -> None:
        print("Game parameters")

    #Placeholder for "Start Game" function
    def start_game(self) -> None:
        print("Start game")
        self.root.nametowidget(".player_entry.teams").destroy()
        self.root.nametowidget(".player_entry.instructions").destroy()
        self.root.nametowidget(".player_entry.game_mode").destroy()
        self.root.nametowidget(".player_entry.top_edit").destroy()
        red_list:List[str] = []
        for player in range(len(self.red_team)):
            red_list.append(self.red_team[player][0].get())
        green_list:List[str] = []
        for player in range(len(self.green_team)):
            green_list.append(self.green_team[player][0].get())
        countdown = Game_Start_Countdown(parent_window = self.root)
        game_action_gui = Game_Action_GUI(self.root, red_list, green_list)
        python_udpserver.start(game_action_gui, self.ip)
        python_udpclient.sendMessage("202", self.ip)

    #Create window to enter new IP
    def create_ip_window(self) -> None:
        print("Change ip")
        self.iproot = Toplevel(self.root)
        self.iproot.title("New IP Entry")
        ip_frame = Frame(self.iproot, bg='black')
        ip_label = Label(ip_frame, text="Enter new socket IP:", bg='black', fg='lime')
        ip_str = StringVar()
        ip_entry = Entry(ip_frame, textvariable=ip_str, bg='lightgray', relief=FLAT)
        ip_frame.pack()
        ip_label.pack(side=LEFT)
        ip_entry.pack(side=LEFT)
        ip_entry.focus()
        ip_entry.bind('<Return>', lambda event: self.ip_set(ip_str.get()))

    #Change socket IP
    def ip_set(self, new_ip:str) -> None:
        self.ip = new_ip
        self.iproot.destroy()

    #Placeholder for "Preentered Games" function
    def preentered_games(self) -> None:
        print("Preentered games")

    #Placeholder for "F7" function
    def f7_func(self) -> None:
        print("F7")

    #Placeholder for "View Game" function
    def view_game(self) -> None:
        print("View game")

    #Placeholder for "Flick Sync" function
    def flick_sync(self) -> None:
        print("Flick sync")

    #Placeholder for "Clear Game" function
    def clear_game(self) -> None:
        self.move_right()
        for green_player in range(len(self.green_team)):
            self.delete_player()
        self.move_left()
        for red_player in range(len(self.red_team)):
            self.delete_player()

    ###Player Entry Screen###
    def create_main(self) -> None:
        #Create frame and top label
        player_entry = Frame(self.root, bg='black', name="player_entry")
        top_edit = Label(player_entry, text="Edit Current Game", bg='black', fg='royalblue', font='75', name="top_edit")
        player_entry.pack(expand=True)
        top_edit.pack()
    
        #Create each team's entry screen
        team_entry = Frame(player_entry, bg='black', name="teams")
        team_entry.pack()
        self.red_team_entry = Frame(team_entry, bg='red4', name="red_team")
        red_label = Label(self.red_team_entry, text="RED TEAM", bg='red4', fg='lightgray')
        self.red_team_entry.pack(side=LEFT)
        red_label.pack()
        self.green_team_entry = Frame(team_entry, bg='green4', name="green_team")
        green_label = Label(self.green_team_entry, text="GREEN TEAM", bg='green4', fg='lightgray')
        self.green_team_entry.pack()
        green_label.pack()
        for player_num in range(16):
            self.create_player(self.red_team_entry, 'red4', player_num)
            self.create_player(self.green_team_entry, 'green4', player_num)

        #Create label for game mode
        game_mode = Label(player_entry, text="Game Mode: Standard public mode", bg='gray30', fg='lightgray', name="game_mode")

        #Create option buttons at bottom
        option_buttons = Frame(player_entry, bg='black', name='option_buttons')
        edit = Button(option_buttons, text='F1' + '\n' + 'Edit' + '\n' + 'Game', width=10, height=5, bg='black', fg='lime', command=self.edit_game)
        self.root.bind('<F1>', lambda event: self.edit_game())
        param = Button(option_buttons, text='F2' + '\n' + 'Game' + '\n' + 'Parameters', width=10, height=5, bg='black', fg='lime', command=self.game_parameters)
        self.root.bind('<F2>', lambda event: self.game_parameters())
        start = Button(option_buttons, text='F3' + '\n' + 'Start' + '\n' + 'Game', width=10, height=5, bg='black', fg='lime', command=self.start_game)
        self.root.bind('<F3>', lambda event: self.start_game())
        change_ip = Button(option_buttons, text='F4' + '\n' + 'Change' + '\n' + 'Socket IP', width=10, height=5, bg='black', fg='lime', command=self.create_ip_window)
        self.root.bind('<F4>', lambda event: self.create_ip_window())
        preentered = Button(option_buttons, text='F5' + '\n' + 'PreEntered' + '\n' + 'Games', width=10, height=5, bg='black', fg='lime', command=self.preentered_games)
        self.root.bind('<F5>', lambda event: self.preentered_games())
        f7 = Button(option_buttons, text='F7', width=10, height=5, bg='black', fg='lime', command=self.f7_func)
        self.root.bind('<F7>', lambda event: self.f7_func())
        view = Button(option_buttons, text='F8' + '\n' + 'View' + '\n' + 'Game', width=10, height=5, bg='black', fg='lime', command=self.view_game)
        self.root.bind('<F8>', lambda event: self.view_game())
        sync = Button(option_buttons, text='F10' + '\n' + 'Flick' + '\n' + 'Sync', width=10, height=5, bg='black', fg='lime', command=self.flick_sync)
        self.root.bind('<F10>', lambda event: self.flick_sync())
        clear = Button(option_buttons, text='F12' + '\n' + 'Clear' + '\n' + 'Game', width=10, height=5, bg='black', fg='lime', command=self.clear_game)
        self.root.bind('<F12>', lambda event: self.clear_game())

        #Create label showing instructions
        options_width:int = int(self.root.winfo_reqwidth() / 1.32)
        instructions = Label(player_entry, name="instructions", text="<Del> to Delete Player, <Ins> to Manually Insert, or edit codename", width=options_width, bg='lightgray', fg='black')
        self.root.bind('<Insert>', lambda event: self.insert_player())
        self.root.bind('<Delete>', lambda event: self.delete_player())
        self.root.bind('<Up>', lambda event: self.move_up())
        self.root.bind('<Down>', lambda event: self.move_down())
        self.root.bind('<Left>', lambda event: self.move_left())
        self.root.bind('<Right>', lambda event: self.move_right())

        #Packing widgets
        game_mode.pack()
        option_buttons.pack()
        edit.pack(side=LEFT)
        param.pack(side=LEFT)
        start.pack(side=LEFT)
        change_ip.pack(side=LEFT)
        preentered.pack(padx=(0, 80), side=LEFT)
        f7.pack(side=LEFT)
        view.pack(side=LEFT)
        sync.pack(padx=80, side=LEFT)
        clear.pack(side=LEFT)
        instructions.pack()
