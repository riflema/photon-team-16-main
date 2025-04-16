from tkinter import *
from typing import Dict, List, Union
import sys
import psycopg2

connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

class Game_Action_GUI:
    def __init__(self, rt:Tk, red_list:List[str], green_list:List[str]) -> None:
        self.root = rt
                        #codename, points
        self.red_team:Dict[str, IntVar] = {}
        for codename in red_list:
            self.red_team[codename] = IntVar()
        self.green_team:Dict[str, IntVar] = {}
        for codename in green_list:
            self.green_team[codename] = IntVar()

        self.red_total_points = IntVar()
        self.green_total_points = IntVar()
        self.time_remaining = StringVar()
        self.time_remaining.set("0:00")
        self.events_frame = None
        self.event_counter:int = 0
        self.B = PhotoImage(file="gui_sprites/B_image.png")

        self.root.title('Game Action')
        self.root.configure(bg='black')

        self.create_main()

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

    def create_player(self, team_players:Frame, color:str, player:str) -> None:
        if (color == 'red2'):
            new_player = Frame(team_players, height=20, width=300, bg='black', name="red_" + player.replace(" ", ""))
            new_player.pack_propagate(False)
            new_player.pack()
            Label(new_player, bg='black', fg=color, name=player.replace(" ", "").lower()).pack(side=LEFT)
            Label(new_player, text=player, bg = 'black', fg=color, font='75').pack(side=LEFT, padx=(0,175))
            Label(new_player, textvariable=self.red_team[player], bg = 'black', fg=color, font='75').pack(side=RIGHT)
        if (color == 'green2'):
            new_player = Frame(team_players, height=20, width=300, bg='black', name="green_" + player.replace(" ", ""))
            new_player.pack_propagate(False)
            new_player.pack()
            Label(new_player, bg='black', fg=color, name=player.replace(" ", "").lower()).pack(side=LEFT)
            Label(new_player, text=player, bg = 'black', fg=color, font='75').pack(side=LEFT, padx=(0,175))
            Label(new_player, textvariable=self.green_team[player], bg = 'black', fg=color, font='75').pack(side=RIGHT)
    
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

    def add_new_hit(self, first_id:int, second_id:int) -> None:
        first_codename:Union[str, None] = self.query_codename_database(first_id)
        if (first_codename == None):
            first_codename = ""
        second_codename:Union[str, None] = self.query_codename_database(second_id)
        if (second_codename == None):
            second_codename = ""
        color_1:int = -1 #0 red 1 green
        color_2:int = -1
        for player in self.red_team:
            if player == first_codename:
                color_1 = 0
            if player == second_codename:
                color_2 = 0
        for player in self.green_team:
            if player == first_codename:
                color_1 = 1
            if player == second_codename:
                color_2 = 1
        if color_1 == color_2:
            if color_1 == 0:
                self.red_team[first_codename].set(self.red_team[first_codename].get() - 10)
                self.red_total_points.set(self.red_total_points.get() - 10)
            if color_1 == 1:
                self.green_team[first_codename].set(self.green_team[first_codename].get() - 10)
                self.green_total_points.set(self.green_total_points.get() - 10)
        else:
            if color_1 == 0:
                self.red_team[first_codename].set(self.red_team[first_codename].get() + 10)
                self.red_total_points.set(self.red_total_points.get() + 10)
            if color_1 == 1:
                self.green_team[first_codename].set(self.green_team[first_codename].get() + 10)
                self.green_total_points.set(self.green_total_points.get() + 10)
        list = self.event_frame.pack_slaves()
        if len(self.event_frame.pack_slaves()) >= 9:
            list[0].destroy()
        self.event_counter += 1
        Label(self.event_frame, text=(first_codename + " hit " + second_codename), bg='darkblue', fg='white', font='75', name=("event_" + str(self.event_counter))).pack()

    def add_new_base_hit(self, equip_id:int, color:int) -> None:
        codename:Union[str, None] = self.query_codename_database(equip_id)
        if (codename == None):
            codename = ""
        for player in self.red_team:
            if player == codename:
                current_score_1:int = self.red_team[player].get()
                self.red_team[player].set(current_score_1 + 100)
                self.red_total_points.set(self.red_total_points.get() + 100)
                break
                #add stylized B
        for player in self.green_team:
            if player == codename:
                current_score_2:int = self.green_team[player].get()
                self.green_team[player].set(current_score_2 + 100)
                self.green_total_points.set(self.green_total_points.get() + 100)
                break
                #add stylized B
        list = self.event_frame.pack_slaves()
        if len(self.event_frame.pack_slaves()) >= 9:
            list[0].destroy()
        self.event_counter += 1
        
        if (color == 0): #red
            Label(self.event_frame, text=(codename + " hit Red Base"), bg='darkblue', fg='white', font='75', name=("event_" + str(self.event_counter))).pack()
            self.root.nametowidget(".player_entry.game_action.players_frame.green_team_frame.green_team_players.green_" + codename.replace(" ", "") + "." + codename.replace(" ", "").lower()).configure(image=self.B)
        if (color == 1): #green
            Label(self.event_frame, text=(codename + " hit Green Base"), bg='darkblue', fg='white', font='75', name=("event_" + str(self.event_counter))).pack()
            self.root.nametowidget(".player_entry.game_action.players_frame.red_team_frame.red_team_players.red_" + codename.replace(" ", "") + "." + codename.replace(" ", "").lower()).configure(image=self.B)

    #Create each player check box and entry field
    def create_main(self) -> None:
        game_action = Frame(self.root.nametowidget(".player_entry"), bg='black', name="game_action", relief='solid', highlightbackground='yellow', highlightthickness='2')
        game_action.pack(expand=True, side=TOP, pady=20)
        top_label_frame = Frame(game_action, bg='black', name="top_label_frame")
        top_label_frame.pack()
        Label(top_label_frame, text="XP", bg='black', fg='red', font='75').pack(side=LEFT, padx=(0,800))
        Label(top_label_frame, text="Current Scores", bg='black', fg='lightblue', font='75').pack(side=RIGHT)

        players_frame = Frame(game_action, bg='black', name="players_frame")
        players_frame.pack()
        red_team_frame = Frame(players_frame, bg='black', name="red_team_frame")
        red_team_frame.pack(side=LEFT)
        Label(red_team_frame, text="RED TEAM", bg = 'black', fg='white', font='100').pack(padx=(175,175))
        red_team_players = Frame(red_team_frame, height=320, width=500, bg='black', name="red_team_players")
        red_team_players.pack_propagate(False)
        red_team_players.pack()
        for player in self.red_team:
            if (player == ""):
                break
            self.create_player(red_team_players, 'red2', player)
        red_total_frame = Frame(red_team_frame, height=20, width=300, bg='black', name="red_team_total")
        red_total_frame.pack_propagate(False)
        red_total_frame.pack()
        #Label(red_total_frame, text="Total points: ", bg = 'black', fg='red2', font='75').pack(side=LEFT, padx=(0,175))
        Label(red_total_frame, textvariable=self.red_total_points, bg = 'black', fg='red2', font='75').pack(padx=(175,0), side=RIGHT)
        green_team_frame = Frame(players_frame, bg='black', name="green_team_frame")
        green_team_frame.pack(side=RIGHT)
        Label(green_team_frame, text="GREEN TEAM", bg = 'black', fg='white', font='100').pack(padx=(175,175))
        green_team_players = Frame(green_team_frame, height=320, width=500, bg='black', name="green_team_players")
        green_team_players.pack_propagate(False)
        green_team_players.pack()
        for player in self.green_team:
            if (player == ""):
                break
            self.create_player(green_team_players, 'green2', player)
        green_total_frame = Frame(green_team_frame, height=20, width=300, bg='black', name="green_team_points")
        green_total_frame.pack_propagate(False)
        green_total_frame.pack()
        #Label(green_total_frame, text="Total points: ", bg = 'black', fg='green2', font='75').pack(side=LEFT, padx=(0,175))
        Label(green_total_frame, textvariable=self.green_total_points, bg = 'black', fg='green2', font='75').pack(padx=(175,0),side=RIGHT)
        action_frame = Frame(game_action, bg='darkblue', name="action_frame", relief='solid', highlightbackground='yellow', highlightthickness='2')
        action_frame.pack()
        #action_top_frame = Frame(action_frame, bg='darkblue', name="action_top_frame")
        #action_top_frame.pack()
        Label(action_frame, text="Current Game Action", bg='darkblue', fg='lightblue', font='75').pack(padx=(800,0))    
        self.event_frame = Frame(action_frame, height=200, width=1000, bg='darkblue', name='events_frame')
        self.event_frame.pack_propagate(False)
        self.event_frame.pack(side=LEFT)
        time_remaining_frame = Frame(game_action, height=25, width=1000, bg='black', name="time_remaining_frame", relief='solid', highlightbackground='yellow', highlightthickness='2')
        time_remaining_frame.pack_propagate(False)
        time_remaining_frame.pack()
        Label(time_remaining_frame, text="Time Remaining: ", bg='black', fg='white', font='100').pack(side=LEFT, padx=(800,0))
        Label(time_remaining_frame, textvariable=self.time_remaining, bg='black', fg='white', font='100').pack(side=LEFT) #implement time remaining
        self.root.nametowidget(".player_entry.option_buttons").pack_forget()
        self.root.nametowidget(".player_entry.option_buttons").pack()