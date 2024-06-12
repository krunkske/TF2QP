import a2s
import requests
import os
import json
import platform
import subprocess
import asyncio
import webbrowser

import customtkinter
from tkinter import *
from tkinter.ttk import *

from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TF2CC")
        self.geometry("600x700")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        customtkinter.set_appearance_mode("system")

        
        #IMAGES
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "tf2_logo.png")), size=(34, 34))
        
        #FONT
        self.title_font =  customtkinter.CTkFont(size=18, weight="bold")
        self.large_font = customtkinter.CTkFont(size=22, weight="bold")
        self.button_font = customtkinter.CTkFont(size=14, weight="bold")
        self.large_button_font = customtkinter.CTkFont(size=18, weight="bold")
        self.label_font = customtkinter.CTkFont(size=14, weight="bold")
        self.small_label_font = customtkinter.CTkFont(size=14, weight="normal")
        
        # SIDEBAR
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        #LOGO
        self.logo_frame_label = customtkinter.CTkLabel(self.navigation_frame, text= "TF2CC  ",image=self.logo_image, compound="right", font=self.title_font)
        self.logo_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        #BUTTOS SIDE BAR
        self.play_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Play",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.play_button_event, font=self.title_font)
        self.play_button.grid(row=1, column=0, sticky="ew")
        
        self.config_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Config",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.config_button_event, font=self.title_font)
        self.config_button.grid(row=2, column=0, sticky="ew")
        
        self.settings_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Settings",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.settings_button_event, font=self.title_font)
        self.settings_button.grid(row=3, column=0, sticky="ew")
        
        self.info_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="About",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.info_button_event, font=self.title_font)
        self.info_button.grid(row=4, column=0, sticky="s")
        
        self.info_label = customtkinter.CTkLabel(self.navigation_frame, text="Welcome to TF2CC", font=self.label_font)
        self.info_label.grid(row=5, column=0, padx=10, pady=5, sticky="s")
        
        self.ip_label = customtkinter.CTkLabel(self.navigation_frame, text="", font=self.small_label_font)
        self.ip_label.grid(row=6, column=0, padx=5, pady=5, sticky="s")
        
        """ USED TO SWITCH BETWEEN DARK/LIGHT MODE. NOT INPLEMENTED YET
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        """
        
        #CONSTRUCT PLAY PAGE
        self.play_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.play_frame.grid_columnconfigure(0, weight=1)
        
        self.play_label = customtkinter.CTkLabel(self.play_frame, text="Play", font=self.large_font)
        self.play_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.server_type_combo = customtkinter.CTkOptionMenu(self.play_frame, values=["Casual", "Uncletopia", "RTD"], width=200, height=30, command=self.changed_server_type, font=self.button_font)
        self.server_type_combo.grid(row=1, column=0, padx=20, pady=10)
        
        self.amount_of_players_frame = customtkinter.CTkFrame(self.play_frame, corner_radius=0, fg_color="transparent")
        self.amount_of_players_frame.grid(row=2, column=0, padx=0, pady=0)
        
        self.amount_of_players_label = customtkinter.CTkLabel(self.amount_of_players_frame, text=str(int(players)) + " players", font=self.label_font)
        self.amount_of_players_label.grid(row=0, column=1, padx=0, pady=0)
        
        self.amount_of_players_text_label = customtkinter.CTkLabel(self.amount_of_players_frame, text="Players in lobby", font=self.label_font)
        self.amount_of_players_text_label.grid(row=1, column=0, padx=0, pady=0)
        
        self.amount_of_players_slider = customtkinter.CTkSlider(self.amount_of_players_frame, from_=1, to=12, command=self.changed_lobby_count, number_of_steps=11)
        self.amount_of_players_slider.set(int(players))
        self.amount_of_players_slider.grid(row=1, column=1, padx=20, pady=0)
        
        self.start_search_button = customtkinter.CTkButton(self.play_frame, text="Start search", command=start_search, width=150, height=50, font=self.large_button_font, fg_color="#1679AB")
        self.start_search_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.cancel_button = customtkinter.CTkButton(self.play_frame, text="Cancel", command=cancel_search, state=DISABLED, width=150, height=30, font=self.button_font, fg_color="#1679AB")
        self.cancel_button.grid(row=4, column=0, padx=20, pady=0)
        
        #CONSTRUCT CONFIG FRAME
        self.config_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.config_frame.grid_columnconfigure(0, weight=1)
        
        self.config_label = customtkinter.CTkLabel(self.config_frame, text="Config", font=self.large_font)
        self.config_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.work_in_progress_label = customtkinter.CTkLabel(self.config_frame, text="Work in progress.", font=self.title_font)
        self.work_in_progress_label.grid(row=1, column=0, padx=20, pady=10)
        
        
        #CONSTRUCT SETTINGS FRAME
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        self.settings_label = customtkinter.CTkLabel(self.settings_frame, text="Settings", font=self.large_font)
        self.settings_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.player_count_frame = customtkinter.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.player_count_frame.grid(row=1, column=0, padx=0, pady=0)
        
        self.player_count_label = customtkinter.CTkLabel(self.player_count_frame, text="Amount of players", font=self.label_font)
        self.player_count_label.grid(row=0, column=0, padx=0, pady=0)
        
        self.player_count_combo = customtkinter.CTkOptionMenu(self.player_count_frame, values=["0-11", "12-18", "19-24", "24-100"], command=self.changed_player_count, font=self.button_font)
        if capacity == [0, 11]:
            self.player_count_combo.set("0-11")
        elif capacity == [12, 18]:
            self.player_count_combo.set("12-18")
        elif capacity == [19, 24]:
            self.player_count_combo.set("19-24")
        self.player_count_combo.grid(row=0, column=1, padx=20, pady=10)
        
        self.max_ping_frame = customtkinter.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.max_ping_frame.grid(row=2, column=0, padx=0, pady=0)
        
        self.max_ping_label = customtkinter.CTkLabel(self.max_ping_frame, text=str(int(max_ping*1000)) + " ms", font=self.label_font)
        self.max_ping_label.grid(row=0, column=1, padx=0, pady=0)
        
        self.max_ping_text_label = customtkinter.CTkLabel(self.max_ping_frame, text="Max Ping:", font=self.label_font)
        self.max_ping_text_label.grid(row=1, column=0, padx=0, pady=0)
        
        self.max_ping_slider = customtkinter.CTkSlider(self.max_ping_frame, from_=10, to=200, command=self.changed_max_ping)
        self.max_ping_slider.set(int(max_ping*1000))
        self.max_ping_slider.grid(row=1, column=1, padx=20, pady=0)
        """
        self.blacklist_label = customtkinter.CTkLabel(self.settings_frame ,text="Blacklist", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.blacklist_label.grid(row=3, column=0, padx=20, pady=10)
        
        self.blacklist_name_textbox = customtkinter.CTkTextbox(self.settings_frame, width=160, height=20)
        self.blacklist_name_textbox.grid(row=4, column=0, padx=20, pady=10)
        """
        
        #CONSTRUCT INFO FRAME
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        self.name_label = customtkinter.CTkLabel(self.info_frame, text="TF2 Community Casual", font=self.large_font)
        self.name_label.grid(row=0, column=0, padx=5, pady=10)
        
        self.github_link_button = customtkinter.CTkButton(self.info_frame, text="GitHub", command=self.open_gh_url, font=self.button_font, width=100, height=30)
        self.github_link_button.grid(row=1, column=0, padx=5, pady=10)
        
        self.select_frame_by_name("play")
        self.changed_server_type("Casual")
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.play_button.configure(fg_color=("gray75", "gray25") if name == "play" else "transparent")
        self.config_button.configure(fg_color=("gray75", "gray25") if name == "config" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        self.info_button.configure(fg_color=("gray75", "gray25") if name == "info" else "transparent")

        # show selected frame
        if name == "play":
            self.play_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.play_frame.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        if name == "info":
            self.info_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.info_frame.grid_forget()


    def play_button_event(self):
        self.select_frame_by_name("play")

    def config_button_event(self):
        self.select_frame_by_name("config")

    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def info_button_event(self):
        self.select_frame_by_name("info")
    
    def changed_server_type(self, new_server_type):
        global content
        i = 0
        if new_server_type == "Casual":
            i = 0
        elif new_server_type == "Uncletopia":
            i = 1
        elif new_server_type == "RTD":
            i = 2
        
        with open('config/' + all_configs[i], 'r') as f:
            content = json.load(f)
    
    def changed_player_count(self, new_player_count):
        global capacity
        if new_player_count == "0-11":
            capacity = [0, 11]
        elif new_player_count == "12-18":
            capacity = [12, 18]
        elif new_player_count == "19-24":
            capacity = [19, 24]
        elif new_player_count == "24-100":
            capacity = [24,100]
        else:
            print("wrong capacity")
        
        save_settings()

    def changed_lobby_count(self, new_lobby_count):
        global players
        players = new_lobby_count
        app.amount_of_players_label.configure(text=str(int(new_lobby_count)) + " players")
    
    def changed_max_ping(self, value):
        global max_ping
        global app
        max_ping = value/1000
        app.max_ping_label.configure(text=str(int(value)) + " ms")
        save_settings()
    
    def blacklist_save_pressed(self):
        pass

    def open_gh_url(self):
        webbrowser.open("https://github.com/krunkske/TF2CC")

#variables
gh_url = "https://raw.githubusercontent.com/krunkske/TF2CC/main/configs/"
all_configs = ["casual_servers.json", "uncletopia.json", "rtd.json"]
available_servers = []
max_ping = 0.05
capacity = 2

players = 1
content = []
blacklist = []

stop = False
searching = False

def setup():
    global capacity
    global max_ping
    global content
    global blacklist
    
    if not os.path.exists("config"):
        os.makedirs("config")
    if not os.path.exists("config/user_config"):
        os.makedirs("config/user_config")

    if not os.path.exists("config/user_config/config.json"):
        settings_json = {"max_ping": 0.04, "capacity": 2}
        with open("config/user_config/config.json", "w") as f:
            f.write(json.dumps(settings_json, indent=4))
    else:
        with open('config/user_config/config.json', 'r') as f:
            cfg_content = json.load(f)
            max_ping = cfg_content['max_ping']
            capacity = cfg_content['capacity']
    
    if not os.path.exists("config/user_config/blacklist.json"):
        blacklist_json = [{"name": "example_name", "ip": "256.256.256.256", "port": 8080}]
        with open("config/user_config/blacklist.json", "w") as f:
            f.write(json.dumps(blacklist_json, indent=4))
    else:
        with open("config/user_config/blacklist.json", "r") as f:
            blacklist = json.load(f)
            

    if capacity == 1:
        capacity = [0, 11]
    elif capacity == 2:
        capacity = [12, 18]
    elif capacity == 3:
        capacity = [19, 24]
    elif capacity == 4:
        capacity = [24, 100]
    

    for i in all_configs:
        with open("config/" + i, 'w') as f:
            f.write(json.dumps(get_config(i), indent=4))

def get_config(config_name):
    try:
        req = requests.get(gh_url + config_name)
        return req.json()
    except Exception as e:
        print("Something went wrong with getting the config")
        print(e)
        exit()

def save_settings():
    global max_ping
    global capacity
    cap = 2
    if capacity == [0, 11]:
        cap = 1
    elif capacity == [12, 18]:
        cap = 2
    elif capacity == [19, 24]:
        cap = 3
    elif capacity == [24, 100]:
        cap = 4
    
    
    settings_json = {"max_ping": max_ping, "capacity": cap}
    with open("config/user_config/config.json", "w") as f:
        f.write(json.dumps(settings_json, indent=4))
    
    print(f"Saved settings {cap} {max_ping}")

async def refresh_server_list(content, players):
    available_servers.clear()

    async def get_server_info(sv):
        name = sv["name"]
        ip = sv["ip"]
        port = sv["port"]
        
        print(f"name: {name} ip: {ip}")
        
        try:
            server_info = await a2s.ainfo((ip, port), 1)
            #print(server_info.player_count)
            #print(server_info.max_players)
            #print(server_info.ping)

            if server_info.player_count + players <= server_info.max_players:
                print(f"added {server_info.server_name} to list")
                available_servers.append({"ip": ip, "port": port, "name": name, "ping": server_info.ping, "players": server_info.player_count, "max_players": server_info.max_players}) #will be used later
            else:
                print(f"not enough spots: {server_info.player_count} poulated, {players} players")
        except Exception as e:
            print(e)

    tasks = [get_server_info(sv) for sv in content]
    await asyncio.gather(*tasks)

def connect(ip, port, name,):
    global app
    print(f"Connecting to {name}: {ip}:{port}")
    if players > 1:
        app.clipboard_clear()
        app.clipboard_append(f"connect {ip}:{port}")
        app.update()
        print(f"COOMAND COPIED TO CLIPBOARD")
        iptxt(f"Copied command!")
    else:
        iptxt(f"{ip}:{port}")
    infotxt(f"Connecting you to \n{name}")
    
    url = f"steam://connect/{ip}:{port}"
    if platform.system() == "Windows":
        subprocess.Popen(['start', url], shell=True) #for windows NOT TESTED
    elif platform.system() == "Linux":
        #print("disabled linux connect. If this got into the release build, please contact the developer.")
        subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # For Linux

def start_search():
    global content
    global players
    global stop
    global searching
    global app
    if stop:
        stop = False
        return False
    searching = True
    app.cancel_button.configure(state=NORMAL)
    app.start_search_button.configure(state=DISABLED)
    infotxt("Searching...")
    
    asyncio.run(refresh_server_list(content, players))

    i = 0
    Max_ping = max_ping
    Capacity = capacity
    while True:
        #Max_ping += i/20 #will put you in servers with with a way too high ping
        Capacity[0] -= i
        Capacity[1] += i

        for sv in available_servers:
            if sv['ping'] <= Max_ping and Capacity[0] < sv['players'] < Capacity[1]:
                if not stop:
                    print(f"FOUND MATCH: {int(sv['ping']*1000)} ping, {int(Max_ping*1000)} max ping. {sv['players']} {Capacity}")
                    connect(sv['ip'], sv['port'], sv['name'])
                    app.start_search_button.configure(state=NORMAL)
                    app.cancel_button.configure(state=DISABLED)
                    searching = False
                    return True
                else:
                    stop = False
                    return False
            else:
                #this is here for now to check what causes a non-match
                                
                if not sv['ping'] <= Max_ping:
                    print(f"Ping was too high: {int(sv['ping']*1000)}, max {int(Max_ping*1000)} : {sv["name"]}")
                elif not Capacity[0] < sv['players'] < Capacity[1]:
                    print(f"Capacity was not between {Capacity[0]} and {Capacity[1]}, {sv['players']} : {sv["name"]}")
                else:
                    print(f"Something else: {int(sv['ping']*1000)} {int(Max_ping*1000)} {sv['players']} {Capacity} : {sv["name"]}")
                
        i += 1
        if Capacity[0] < 0 and Capacity[1] > 24 or Capacity[0] < 0 and not Capacity[1] >= 100:
            print("could not find a match. retrying in 5 seconds")
            if not stop:
                app.after(5000, start_search)
            else:
                stop = False
            return False

def cancel_search():
    global app
    global stop
    global searching
    if searching:
        app.start_search_button.configure(state=NORMAL)
        app.cancel_button.configure(state=DISABLED)
        infotxt("Cancelled search.")
        print("Cancelled search.")
        stop = True
        searching = False

def infotxt(txt):
    app.info_label.configure(text=txt)

def iptxt(txt):
    app.ip_label.configure(text=txt)


if __name__ == "__main__":
    setup()
    app = App()
    print("Welcome to TF2CC!")
    app.mainloop()