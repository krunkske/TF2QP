import a2s
import requests
import os
import json
import platform
import subprocess
import asyncio

import customtkinter
from tkinter import *
from tkinter.ttk import *

from PIL import Image

class IntSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 command: callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(3, 0), pady=3)
        
        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        
        

        # default value
        self.entry.insert(0, "0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            if value >= 0:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self): #removed type safety due to bug
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TF2CC")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        #IMAGES
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "tf2_logo.png")), size=(34, 34))
        
        
        # SIDEBAR
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        #LOGO WILL GO HERE
        self.logo_frame_label = customtkinter.CTkLabel(self.navigation_frame, text= "TF2CC  ",image=self.logo_image, compound="right", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        #BUTTOS SIDE BAR
        self.play_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Play",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.play_button_event)
        self.play_button.grid(row=1, column=0, sticky="ew")
        
        self.config_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Config",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.config_button_event)
        self.config_button.grid(row=2, column=0, sticky="ew")
        
        self.settings_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text="Settings",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="s", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")
        
        self.info_label = customtkinter.CTkLabel(self.navigation_frame, text="Welcome to TF2CC")
        self.info_label.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        
        #doesn't show up yet
        self.ip_label = customtkinter.CTkLabel(self.navigation_frame, text="test")
        self.info_label.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        
        """ USED TO SWITCH BETWEEN DARK/LIGHT MODE. NOT INPLEMENTED YET
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        """
        
        #CONSTRUCT PLAY PAGE
        self.play_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.play_frame.grid_columnconfigure(0, weight=1)
        
        self.server_type_combo = customtkinter.CTkOptionMenu(self.play_frame, values=["Casual", "Uncletopia"], command=self.changed_server_type)
        self.server_type_combo.grid(row=1, column=0, padx=20, pady=10)
        
        self.start_search_button = customtkinter.CTkButton(self.play_frame, text="Start search", command=start_search)
        self.start_search_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.cancel_button = customtkinter.CTkButton(self.play_frame, text="Cancel", command=cancel_search, state=DISABLED)
        self.cancel_button.grid(row=3, column=0, padx=20, pady=10)
        
        #CONSTRUCT CONFIG FRAME
        self.config_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.config_frame.grid_columnconfigure(0, weight=1)
        
        
        #CONSTRUCT SETTINGS FRAME
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        self.player_count_combo = customtkinter.CTkOptionMenu(self.settings_frame, values=["0-11", "12-18", "19-24"], command=self.changed_player_count)
        if capacity == [0, 11]:
            self.player_count_combo.set("0-11")
        elif capacity == [12, 18]:
            self.player_count_combo.set("12-18")
        elif capacity == [19, 24]:
            self.player_count_combo.set("19-24")
        self.player_count_combo.grid(row=1, column=0, padx=20, pady=10)
        
        self.max_ping_label = customtkinter.CTkLabel(self.settings_frame, text="Max Ping:")
        self.max_ping_label.grid(row=2, column=0, padx=0, pady=0)
        
        self.max_ping_nrbox = IntSpinbox(self.settings_frame, step_size=1, command=self.changed_max_ping)
        self.max_ping_nrbox.set(int(max_ping*1000))
        self.max_ping_nrbox.grid(row=2, column=1, padx=20, pady=10)
        
        self.blacklist_label = customtkinter.CTkLabel(self.settings_frame ,text="Blacklist", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.blacklist_label.grid(row=3, column=0, padx=20, pady=10)
        
        self.blacklist_name_textbox = customtkinter.CTkTextbox(self.settings_frame, width=160, height=20)
        self.blacklist_name_textbox.grid(row=4, column=0, padx=20, pady=10)
        
        
        self.select_frame_by_name("play")
        self.changed_server_type("Casual")
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.play_button.configure(fg_color=("gray75", "gray25") if name == "play" else "transparent")
        self.config_button.configure(fg_color=("gray75", "gray25") if name == "config" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

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


    def play_button_event(self):
        self.select_frame_by_name("play")

    def config_button_event(self):
        self.select_frame_by_name("config")

    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def changed_server_type(self, new_server_type):
        global content
        i = 0
        if new_server_type == "Casual":
            i = 0
        elif new_server_type == "Uncletopia":
            i = 1
        with open('configs/' + all_configs[i], 'r') as f:
            content = json.load(f)
    
    def changed_player_count(self, new_player_count):
        global capacity
        if new_player_count == "0-11":
            capacity = [0, 11]
        elif new_player_count == "12-18":
            capacity = [12, 18]
        elif new_player_count == "19-24":
            capacity = [19, 24]
        else:
            print("wrong capacity")
        
        save_settings()

    def changed_max_ping(self):
        global max_ping
        global app
        max_ping = app.max_ping_nrbox.get()/1000
        save_settings()
    
    def blacklist_save_pressed(self):
        pass


#variables
gh_url = "https://raw.githubusercontent.com/krunkske/TF2CC/main/configs/"
all_configs = ["casual_servers.json", "uncletopia.json"]
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
        settings_json = {"max_ping": 0.02, "capacity": 2}
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
        
        print(f"name: {name}\n ip: {ip}")
        
        try:
            server_info = await a2s.ainfo((ip, port), 1)
            #print(server_info.player_count)
            #print(server_info.max_players)
            #print(server_info.ping)

            if server_info.player_count + players <= server_info.max_players:
                #print("appended")
                available_servers.append({"ip": ip, "port": port, "name": name, "ping": server_info.ping, "players": server_info.player_count, "max_players": server_info.max_players}) #will be used later
        except Exception as e:
            print(e)

    tasks = [get_server_info(sv) for sv in content]
    await asyncio.gather(*tasks)

def connect(ip, port, name,):
    global app
    print(f"server found! {name}: {ip}:{port}")
    if players > 1:
        app.clipboard_clear()
        app.clipboard_append(f"connect {ip}:{port}")
        app.update()
        print(f"COOMAND COPIED TO CLIPBOARD")
        iptxt(f"Copied command to clipboard")
    else:
        iptxt(f"{ip}:{port}")
    infotxt(f"Connecting you to \n{name}")
    
    url = f"steam://connect/{ip}:{port}"
    if platform.system() == "Windows":
        subprocess.Popen(['start', url], shell=True) #for windows NOT TESTED
    elif platform.system() == "Linux":
        print("disabled linux connect")
        #subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # For Linux

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
    
    players = 1#spin_box_value.get()
    
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
                    print(f"FOUND MATCH: {sv['ping']} {Max_ping} {sv['players']} {Capacity}")
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
                    print(f"Ping was too high: {sv['ping']}, max {Max_ping} : {sv["name"]}")
                elif not Capacity[0] < sv['players'] < Capacity[1]:
                    print(f"Capacity was not between {Capacity[0]} and {Capacity[1]}, {sv['players']} : {sv["name"]}")
                else:
                    print(f"Something else: {sv['ping']} {Max_ping} {sv['players']} {Capacity} : {sv["name"]}")
                
        i += 1
        if Capacity[0] < 0 and Capacity[1] > 24:
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