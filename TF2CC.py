import a2s
import requests
import os
import json
import platform
import subprocess

from tkinter import *
from tkinter.ttk import *

root = Tk()

#variables
gh_url = "https://raw.githubusercontent.com/krunkske/TF2CC/main/configs/"
all_configs = ["casual_servers.json", "uncletopia.json"]
available_servers = []
max_ping = 0.01
capacity = 2

players = 1
content = []

stop = False
searching = False

def setup():
    global capacity
    global max_ping
    global content
    
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

def connect(ip, port, name,):
    print(f"server found! {name}: {ip}:{port}")
    if players > 1:
        root.clipboard_clear()
        root.clipboard_append(f"connect {ip}:{port}")
        root.update()
        print(f"COOMAND COPIED TO CLIPBOARD")
        iptxt(f"Copied command to clipboard")
    else:
        iptxt(f"{ip}:{port}")
    infotxt(f"Connecting you to {name}")
    
    url = f"steam://connect/{ip}:{port}"
    if platform.system() == "Windows":
        subprocess.Popen(['start', url], shell=True) #for windows NOT TESTED
    elif platform.system() == "Linux":
        pass
        #subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # For Linux

def refresh_server_list():
    available_servers.clear()
    for sv in content:
        name = sv["name"]
        ip = sv["ip"]
        port = sv["port"]
        
        print(f"name: {name}\n ip: {ip}")
        
        try:
            server_info = a2s.info((ip, port), 1)
            
            print(server_info.player_count)
            print(server_info.max_players)
            print(server_info.ping)

            if server_info.player_count + players <= server_info.max_players:
                print("appended")
                available_servers.append({"ip": ip, "port": port, "name": name, "ping": server_info.ping, "players": server_info.player_count, "max_players": server_info.max_players}) #will be used later
        except Exception as e:
            print(e)

def start_search():
    global content
    global players
    global stop
    global searching
    if stop:
        stop = False
        return False
    searching = True
    cancelbtn.config(state=NORMAL)
    searchbtn.config(state=DISABLED)
    infotxt("Searching...")

    type_of_server = combo.get()
    i = 0
    if type_of_server == "Casual":
        i = 0
    elif type_of_server == "Uncletopia":
        i = 1
    
    with open('configs/' + all_configs[i], 'r') as f:
        content = json.load(f)
    
    players = spin_box_value.get()
    
    refresh_server_list()

    i = 0
    Max_ping = max_ping
    while True:
        Max_ping += i/10
        capacity[0] -= i
        capacity[1] += i

        for sv in available_servers:
            if sv['ping'] <= Max_ping and capacity[0] < sv['players'] < capacity[1]:
                if not stop:
                    print(f"FOUND MATCH: {sv['ping']} {Max_ping} {sv['players']} {capacity}")
                    connect(sv['ip'], sv['port'], sv['name'])
                    searchbtn.config(state=NORMAL)
                    cancelbtn.config(state=DISABLED)
                    searching = False
                    return True
                else:
                    stop = False
                    return False
        i += 1
        if capacity[0] < 0 and capacity[1] > 24:
            print("could not find a match. retrying in 5 seconds")
            if not stop:
                root.after(5000, start_search)
            else:
                stop = False
            return False

def cancel_search():
    global stop
    global searching
    if searching:
        searchbtn.config(state=NORMAL)
        cancelbtn.config(state=DISABLED)
        infotxt("Cancelled search.")
        print("Cancelled search.")
        stop = True
        searching = False

def save_settings():
    global max_ping
    global capacity
    cap = 2
    capbox = settings_capacity_combo.get()
    
    if capbox == "0-11":
        cap = 1
    elif capbox == "12-18":
        cap = 2
    elif capbox == "19-24":
        cap = 3
    else:
        print("wrong capacity nr")
    
    settings_json = {"max_ping": settings_max_ping_value.get(), "capacity": cap}
    with open("config/user_config/config.json", "w") as f:
        f.write(json.dumps(settings_json, indent=4))
    
    max_ping = settings_max_ping_value.get()
    capacity = cap

    if capacity == 1:
        capacity = [0, 11]
    elif capacity == 2:
        capacity = [12, 18]
    elif capacity == 3:
        capacity = [19, 24]

def infotxt(txt):
    infolbl.config(text=txt)

def iptxt(txt):
    iplbl.config(text=txt)

#UI
notebook = Notebook(root)
def main_GUI():
    global infolbl
    global iplbl
    root.geometry("400x600")
    root.resizable(False, False)
    root.title("TF2CC")

    # Create a style for ttk widgets
    style = Style()
    style.configure("TButton", font=("Arial", 14), padding=10)
    style.configure("TCombobox", font=("Arial", 14))
    style.configure("TSpinbox", font=("Arial", 14))

    # Create a notebook
    notebook.pack(expand=True, fill='both')
    
    infolbl = Label(root, text="Welcome to TF2CC", font=("Arial Bold", 15))
    infolbl.pack(pady=(0, 10))

    iplbl = Label(root, text="", font=("Arial Bold", 10))
    iplbl.pack(pady=(0, 10))
    
    
    play_tab_GUI()
    settings_tab_GUI()

def play_tab_GUI():
    global lbl1
    global combo
    global spin_box
    global spin_box_value
    global searchbtn
    global cancelbtn
    # Create the first tab frame
    t1 = Frame(notebook)
    notebook.add(t1, text='Play')
    
    # Main title label
    lbl1 = Label(t1, text="TF2CC", font=("Arial Bold", 30))
    lbl1.pack(pady=(20, 10))
    
    # Combobox section
    combo_frame = Frame(t1)
    combo_frame.pack(pady=(10, 20))

    combo_label = Label(combo_frame, text="Server type:", font=("Arial", 14))
    combo_label.pack(side=LEFT, padx=(0, 10))

    combo = Combobox(combo_frame, state="readonly")
    combo['values'] = ("Casual", "Uncletopia")
    combo.current(0)  # Set the selected item
    combo.pack(side=LEFT)

    # Spinbox section
    spinbox_frame = Frame(t1)
    spinbox_frame.pack(pady=(10, 20))

    spinbox_label = Label(spinbox_frame, text="Players in lobby:", font=("Arial", 14))
    spinbox_label.pack(side=LEFT, padx=(0, 10))

    spin_box_value = IntVar(value=1)
    spin_box = Spinbox(spinbox_frame, from_=1, to=6, wrap=True, width=3, textvariable=spin_box_value, font=("Arial", 14))
    spin_box.pack(side=LEFT)

    # Start search button
    searchbtn = Button(t1, text='Start search', command=start_search)
    searchbtn.pack(pady=10)

    cancelbtn = Button(t1, text="Cancel", command=cancel_search, width=6, state=DISABLED)
    cancelbtn.pack(pady=1)

def settings_tab_GUI():
    global settings_max_ping_value
    global settings_max_ping_nrbox
    global settings_capacity_combo
    
    # Create the second tab frame
    t2 = Frame(notebook)
    notebook.add(t2, text='Settings')
    
    settings_max_ping_frame = Frame(t2)
    settings_max_ping_frame.pack(pady=(10, 20))

    settings_max_ping_lbl = Label(settings_max_ping_frame, text="Max ping:", font=("Arial", 14))
    settings_max_ping_lbl.pack(side=LEFT, padx=(0, 10))

    settings_max_ping_value= IntVar(value=20)
    settings_max_ping_nrbox = Spinbox(settings_max_ping_frame, from_=1, to=500, wrap=True, width=6, textvariable=settings_max_ping_value, font=("Arial", 14))
    settings_max_ping_nrbox.pack(side=LEFT)
    
    settings_capacity_frame = Frame(t2)
    settings_capacity_frame.pack(pady=(0, 0))

    settings_capacity_lbl = Label(settings_capacity_frame, text="Players in server:", font=("Arial", 14))
    settings_capacity_lbl.pack(side=LEFT, padx=(0, 0))

    settings_capacity_combo = Combobox(settings_capacity_frame, state="readonly", font=("Arial", 14), width= 10)
    settings_capacity_combo['values'] = ("0-11", "12-18", "19-24")
    settings_capacity_combo.current(1)  # Set the selected item
    settings_capacity_combo.pack(side=LEFT)
    
    savebtn_style = Style()
    savebtn_style.configure("First.TButton", font=("Arial", 14), foreground="green", background="lightgray")
    
    savebtn = Button(t2, text="Save", command=save_settings, width=5, style="First.TButton")
    savebtn.pack(side=BOTTOM, pady=10)
    
    
    

setup()
main_GUI()

# Run the Tkinter event loop
root.mainloop()