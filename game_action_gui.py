from tkinter import *
from typing import Dict, List
import sys

class Game_Action_GUI:
    def __init__(self, red_list:List[str], green_list:List[str]) -> None:
        self.root = Tk()
                        #codename, points
        self.red_team:Dict[str, IntVar] = {}
        for codename in red_list:
            self.red_team[codename] = IntVar()
        self.green_team:Dict[str, IntVar] = {}
        for codename in green_list:
            self.red_team[codename] = IntVar()

        self.root.title('Game Action')
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
    def create_main(self) -> None:
        game_action = Frame(self.root, bg='black', name="game_action", relief='solid', highlightbackground='yellow', highlightthickness='2')
        game_action.pack(expand=True)
        top_label_frame = Frame(game_action, bg='black', name="top_label_frame")
        top_label_frame.pack()
        Label(top_label_frame, text="XP", bg='black', fg='red', font='75').pack(side=LEFT, padx=(0,800))
        Label(top_label_frame, text="Current Scores", bg='black', fg='lightblue', font='75').pack(side=RIGHT)

        players_frame = Frame(game_action, bg='black', name="players_frame")
        players_frame.pack()
        red_team_frame = Frame(players_frame, bg='black', name="red_team_frame")
        red_team_frame.pack(side=LEFT)
        Label(red_team_frame, text="RED TEAM", bg = 'black', fg='lightgray', font='100').pack(padx=(175,175))
        red_team_players = Frame(red_team_frame, bg='black', name="red_team_players")
        red_team_players.pack()
        for player in self.red_team:
            Label(red_team_players, text=player, bg = 'black', fg='red4', font='75').pack(side=LEFT, padx=(0,175))
            Label(red_team_players, textvariable=self.red_team[player], bg = 'black', fg='red4', font='75').pack(side=RIGHT)
        
        green_team_frame = Frame(players_frame, bg='black', name="green_team_frame")
        green_team_frame.pack(side=RIGHT)
        Label(green_team_frame, text="GREEN TEAM", bg = 'black', fg='lightgray', font='100').pack(padx=(175,175))
        green_team_players = Frame(green_team_frame, bg='black', name="red_team_players")
        green_team_players.pack()
        for player in self.green_team:
            Label(green_team_players, text=player, bg = 'black', fg='green4', font='75').pack(side=LEFT, padx=(0,175))
            Label(green_team_players, textvariable=self.green_team[player], bg = 'black', fg='green4', font='75').pack(side=RIGHT)

        action_frame = Frame(game_action, bg='darkblue', name="action_frame", relief='solid', highlightbackground='yellow', highlightthickness='2')
        action_frame.pack()
        Label(action_frame, text="", bg='darkblue').pack(side=LEFT, padx=(0,800))
        Label(action_frame, text="Current Game Action", bg='darkblue', fg='lightblue', font='75').pack(side=RIGHT)    

