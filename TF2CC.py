import a2s
import requests
import os
import json
import platform
import subprocess

from tkinter import *
from tkinter.ttk import *

#variables
gh_url = "https://raw.githubusercontent.com/krunkske/TF2CC/main/configs/"
available_servers = []
max_ping = 0.01
capacity = 2

players = 1
content = []

def setup():
    global capacity
    global max_ping
    global content
    
    if not os.path.exists("config"):
        os.makedirs("config")
    if not os.path.exists("config/user_config"):
        os.makedirs("config/user_config")

    if not os.path.exists("config/user_config/config.json"):
        settings_json = {"max_ping": 0.05, "capacity": 2}
        with open("config/user_config/config.json", "w") as f:
            f.write(json.dumps(settings_json))
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
    

    with open("config/casual_servers.json", 'w') as f:
        f.write(get_config("casual_servers.json"))

    with open('configs/casual_servers.json', 'r') as f: #DEBUG LOADING LOCAL CONFIG
        content = json.load(f)

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
        print(f"SEND THIS COMMAND TO YOUR PARTY MEMBERS:  connect {ip}:{port}")
    print(f"Connecting you to {name}.")
    url = f"steam://connect/{ip}:{port}"
    if platform.system() == "Windows":
        subprocess.Popen(['start', url], shell=True) #for windows NOT TESTED
    elif platform.system() == "Linux":
        subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # For Linux

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
    type_of_server = combo.get()
    refresh_server_list()
    i = 0
    Max_ping = max_ping
    while True:
        Max_ping += i/10
        capacity[0] -= i
        capacity[1] += i

        for sv in available_servers:
            if sv['ping'] <= Max_ping and capacity[0] < sv['players'] < capacity[1]:
                print(f"FOUND MATCH: {sv['ping']} {Max_ping} {sv['players']} {capacity}")
                connect(sv['ip'], sv['port'], sv['name'])
                return True
        i += 1
        if capacity[0] < 0 and capacity[1] > 24:
            print("could not find a match")
            return False


setup()

window = Tk()
window.geometry("500x750")
window.title("TF2CC")

lbl1 = Label(window, text="TF2CC", font=("Arial Bold", 30))
lbl1.pack()

searchbtn = Button(window, text='Start search', command=start_search)
searchbtn.pack()

combo = Combobox(window)
combo['values']= ("Casual", "Uncletopia")
combo.current(0) #set the selected item
combo.pack()

window.mainloop()