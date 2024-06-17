extends Node
const gh_url = "https://raw.githubusercontent.com/krunkske/TF2QP/main/configs/"
var content: Array
var available_servers: Array

var searching = false
var stop = false
var needed_results: int
var requests_completed  = 0

var players = 1
var capacity = [11, 18]
enum region {eu, usa, sa, asia, aus} #used as reference
var current_region = "eu"
var server_type = "casual_servers"
var auto_connect_to_server = true

func _ready() -> void:
	DirAccess.make_dir_absolute("user://config/")
	if not DirAccess.dir_exists_absolute("user://config/user_config/"):
		DirAccess.make_dir_absolute("user://config/user_config/")
		if not FileAccess.file_exists("user://config/user_config/settings.json"):
			$ask_for_key_page.show()
	else:
		load_settings()
	get_config_from_url(gh_url, "casual_servers.json")
	get_config_from_url(gh_url, "uncletopia.json")
	get_config_from_url(gh_url, "rtd.json")

func _process(delta: float) -> void:
	if searching:
		if needed_results != -1:
			if requests_completed == needed_results:
				requests_completed = 0
				print("Starting search with " + str(needed_results) + " servers")
				start_search()

func load_json_file(file):
	var file_content = FileAccess.open(file, FileAccess.READ)
	return JSON.parse_string(file_content.get_as_text())

func get_config_from_url(url, file_name):
	var http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_config_request_completed.bind(file_name, http_request))
	http_request.request(url + file_name)

func _on_config_request_completed(result, response_code, headers, body, file_name, sender):
	var save = FileAccess.open("user://config/" + file_name, FileAccess.WRITE)
	save.store_string(body.get_string_from_utf8())
	print("saved file " + file_name)
	sender.queue_free()

func connect_to_server(ip: String, port: int, Name: String):
	var url = "steam://connect/" + str(ip) + ":" + str(port)
	if players > 1 or not auto_connect_to_server:
		DisplayServer.clipboard_set("connect" + str(ip) + ":" + str(port))
		print("COOMAND COPIED TO CLIPBOARD")
		$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "Found server! Command copied to clipboard"
	else:
		$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "Found server!"
	
	#printerr("CONNECT DISABLED. THIS SHOULD NOT BE IN THE RELEASE BUILD. PLEASE CONTACT THE DEVELOPERS")
	if auto_connect_to_server:
		OS.shell_open(url)
		print("Connecting you to " + str(Name))

func cancel_search():
	if searching:
		$restart_search.stop()
		stop = true
		searching = false
		print("Stopping search")
		$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "Stopping search"
		$gui/play_page/Panel/VBoxContainer/start.disabled = false
		$gui/play_page/Panel/VBoxContainer/cancel.disabled = true

func start_search():
	$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "Searching..."
	var i = 0
	var Capacity = [capacity[0], capacity[1]]
	while true:
		#Max_ping += i/20 #will put you in servers with with a way too high ping
		Capacity[0] -= 1
		Capacity[1] += 1
		
		for sv in available_servers:
			if Capacity[0] < sv['players'] and sv['players'] < Capacity[1]:
				if not stop:
					print("FOUND MATCH: " + str(sv['players']) + " " + str(Capacity))
					connect_to_server(sv['ip'], sv['port'], sv['name'])
					$gui/play_page/Panel/VBoxContainer/start.disabled = false
					$gui/play_page/Panel/VBoxContainer/cancel.disabled = true
					searching = false
					return true
				else:
					stop = false
					return true
			else:
				if stop:
					stop = false
					return true
				#print("Capacity was not between " + str(Capacity[0]) + " and " + str(Capacity[1]) + ", " + str(sv['players']) + " for " + str(sv['name']))
		
		i += 1
		if Capacity[0] < 0 and Capacity[1] > 24:
			print("could not find a match. retrying in 5 seconds")
			$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "could not find a match. retrying in 5 seconds"
			if not stop:
				$restart_search.start()
			else:
				stop = false
			return false

func get_server_data():
	requests_completed = 0
	searching = true
	$gui/side_panel/Panel/VBoxContainer2/info_lbl.text = "Getting server data..."
	content = load_json_file("user://config/" + str(server_type) + ".json")
	needed_results = len(content)
	for server_info in content:
		if server_info["region"] == current_region: 
			var http_request = HTTPRequest.new()
			add_child(http_request)
			http_request.set_timeout(5.0)
			http_request.request_completed.connect(_on_server_request_completed.bind(http_request))
			http_request.request("https://api.steampowered.com/IGameServersService/GetServerList/v1/?key=" + vars.API_KEY + "&filter=addr\\" + str(server_info.ip) + ":" + str(server_info.port))
		else:
			needed_results -= 1

func _on_server_request_completed(result, response_code, headers, body, sender):
	if response_code == 200:
		if JSON.parse_string(body.get_string_from_utf8())["response"] == {}:
			printerr("no data, something went wrong")
			requests_completed += 1
			sender.queue_free()
			return
		var server = JSON.parse_string(body.get_string_from_utf8())["response"]["servers"][0]
		if server["players"] + players <= server["max_players"]:
			print("added " + server["name"] + " to list")
			var server_info = {"players": server["players"], "max_players" : server["max_players"], "ip": server["addr"], "port": server["gameport"], "name": server["name"]}
			available_servers.append(server_info)
		else:
			print("Not enough spots.")
	elif response_code == 403 or response_code == 401:
		print("No api key was given")
		cancel_search()
		$ask_for_key_page.show()
	else:
		print("response code error, code " + str(response_code))
		print(result)
	requests_completed += 1
	sender.queue_free()

func save_settings():
	var file = FileAccess.open("user://config/user_config/settings.json", FileAccess.WRITE)
	var save = {"capacity":capacity, "region": current_region, "auto_connect": auto_connect_to_server, "key": vars.API_KEY}
	file.store_string(str(save))
	print("saved settings")

func load_settings():
	var data = load_json_file("user://config/user_config/settings.json")
	capacity = data["capacity"]
	current_region = data["region"]
	auto_connect_to_server = data["auto_connect"]
	vars.API_KEY = data["key"]
	
	$gui/settings_page/Panel/VBoxContainer/auto_connect_toggle.set_pressed_no_signal(auto_connect_to_server)
	
	if capacity[0] == 0:
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer/capacity_select.select(0)
	elif capacity[0] == 12:
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer/capacity_select.select(1)
	elif capacity[0] == 19:
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer/capacity_select.select(2)
	
	if current_region == "eu":
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer2/region_select.select(0)
	elif current_region == "usa":
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer2/region_select.select(1)
	elif current_region == "aus":
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer2/region_select.select(2)
	elif current_region == "asia":
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer2/region_select.select(3)
	elif current_region == "sa":
		$gui/settings_page/Panel/VBoxContainer/HBoxContainer2/region_select.select(4)
	print("loaded settings")


#UI
func switch_tabs(tab: int):
	if tab == 0:
		$gui/play_page.show()
	else:
		$gui/play_page.hide()
	
	if tab == 1:
		$gui/config_page.show()
	else:
		$gui/config_page.hide()
	
	if tab == 2:
		$gui/settings_page.show()
	else:
		$gui/settings_page.hide()
	
	if tab == 3:
		$gui/about_page.show()
	else:
		$gui/about_page.hide()

func change_server_type(idx: int):
	#hard coded for now
	if idx == 0:
		server_type = "casual_servers"
	elif idx == 1:
		server_type = "uncletopia"
	elif idx == 2:
		server_type = "rtd"

func _on_restart_search_timeout() -> void:
	get_server_data()

func show_key_menu():
	$ask_for_key_page.show()
