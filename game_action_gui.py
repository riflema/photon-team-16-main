from tkinter import *
from typing import Dict, List
import pygame
import sys
import random

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

        self.root.title('Game Action')
        self.root.configure(bg='black')

        pygame.init()
        pygame.mixer.init()
        self.start_music()

        self.create_main()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    #Clear GUI
    def clear(self) -> None:
        list = self.root.pack_slaves()
        for l in list:
            l.destroy()
        list = self.root.grid_slaves()
        for l in list:
            l.destroy()

    def start_music(self) -> None:
        random_track = random.randint(1, 9)
        track: str = f'photon_tracks/Track0{str(random_track)}.mp3'
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1) # Play music indefinately

    def create_player(self, team_players:Frame, color:str, player:str) -> None:
        if (color == 'red2'):
            new_player = Frame(team_players, height=20, width=300, bg='black', name="red_" + player)
            new_player.pack_propagate(False)
            new_player.pack()
            Label(new_player, text=player, bg = 'black', fg=color, font='75').pack(side=LEFT, padx=(0,175))
            Label(new_player, textvariable=self.red_team[player], bg = 'black', fg=color, font='75').pack(side=RIGHT)
        if (color == 'green2'):
            new_player = Frame(team_players, height=20, width=300, bg='black', name="green_" + player)
            new_player.pack_propagate(False)
            new_player.pack()
            Label(new_player, text=player, bg = 'black', fg=color, font='75').pack(side=LEFT, padx=(0,175))
            Label(new_player, textvariable=self.green_team[player], bg = 'black', fg=color, font='75').pack(side=RIGHT)

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
        events_frame = Frame(action_frame, height=200, width=1000, bg='darkblue', name='events_frame')
        events_frame.pack_propagate(False)
        events_frame.pack()
        time_remaining_frame = Frame(game_action, height=25, width=1000, bg='black', name="time_remaining_frame", relief='solid', highlightbackground='yellow', highlightthickness='2')
        time_remaining_frame.pack_propagate(False)
        time_remaining_frame.pack()
        Label(time_remaining_frame, text="Time Remaining: ", bg='black', fg='white', font='100').pack(side=LEFT, padx=(800,0))
        Label(time_remaining_frame, textvariable=self.time_remaining, bg='black', fg='white', font='100').pack(side=LEFT) #implement time remaining
        self.root.nametowidget(".player_entry.option_buttons").pack_forget()
        self.root.nametowidget(".player_entry.option_buttons").pack()
