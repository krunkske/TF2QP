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

func _ready() -> void:
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
	http_request.request_completed.connect(_on_config_request_completed.bind(file_name))
	http_request.request(url + file_name)

func _on_config_request_completed(result, response_code, headers, body, file_name):
	var save = FileAccess.open("user://config/" + file_name, FileAccess.WRITE)
	save.store_string(body.get_string_from_utf8())
	print("saved file " + file_name)

func connect_to_server(ip: String, port: int, Name: String):
	var url = "steam://connect/" + str(ip) + ":" + str(port)
	if players > 1:
		DisplayServer.clipboard_set("connect" + str(ip) + ":" + str(port))
		print("COOMAND COPIED TO CLIPBOARD")
	print("Connecting you to " + str(Name))
	printerr("CONNECT DISABLED. THIS SHOULD NOT BE IN THE RELEASE BUILD. PLEASE CONTACT THE DEVELOPERS")
	#OS.shell_open(url)

func start_search():
	var i = 0
	var Capacity = capacity
	while true:
		#Max_ping += i/20 #will put you in servers with with a way too high ping
		Capacity[0] -= i
		Capacity[1] += i
		
		for sv in available_servers:
			if Capacity[0] < sv['players'] and sv['players'] < Capacity[1]:
				if not stop:
					print("FOUND MATCH: " + str(sv['players']) + " " + str(Capacity))
					connect_to_server(sv['ip'], sv['port'], sv['name'])
					#app.start_search_button.configure(state=NORMAL)
					#app.cancel_button.configure(state=DISABLED)
					searching = false
					return true
				else:
					stop = false
					return true
			else:
				print("Capacity was not between " + str(Capacity[0]) + " and " + str(Capacity[1]) + ", " + str(sv['players']) + " for " + str(sv['name']))
		
		i += 1
		if Capacity[0] < 0 and Capacity[1] > 24:
			print("could not find a match. retrying in 5 seconds")
			if not stop:
				pass
				#app.after(5000, start_search)
			else:
				stop = false
			return false

func get_server_data():
	requests_completed = 0
	searching = true
	content = load_json_file("user://config/" + str(server_type) + ".json")
	needed_results = len(content)
	for server_info in content:
		if server_info["region"] == current_region: 
			var http_request = HTTPRequest.new()
			add_child(http_request)
			http_request.set_timeout(5.0)
			http_request.request_completed.connect(_on_server_request_completed)
			http_request.request("https://api.steampowered.com/IGameServersService/GetServerList/v1/?key=" + vars.API_KEY + "&filter=addr\\" + str(server_info.ip) + ":" + str(server_info.port))
		else:
			needed_results -= 1

func _on_server_request_completed(result, response_code, headers, body):
	if response_code == 200:
		if JSON.parse_string(body.get_string_from_utf8())["response"] == {}:
			printerr("no data, something went wrong")
			requests_completed += 1
			return
		var server = JSON.parse_string(body.get_string_from_utf8())["response"]["servers"][0]
		if server["players"] + players <= server["max_players"]:
			print("added " + server["name"] + " to list")
			var server_info = {"players": server["players"], "max_players" : server["max_players"], "ip": server["addr"], "port": server["gameport"], "name": server["name"]}
			available_servers.append(server_info)
		else:
			print("Not enough spots.")
	else:
		print("response code error, code " + str(response_code))
		print(result)
	requests_completed += 1



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
