extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	self.hide()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_option_button_item_selected(index: int) -> void:
	if not vars.main.searching:
		if index == 0:
			vars.main.capacity = [0, 11]
		elif index == 1:
			vars.main.capacity = [12, 18]
		elif index == 2:
			vars.main.capacity = [19, 24]
		
		vars.main.save_settings()


func _on_region_select_item_selected(index: int) -> void:
	if not vars.main.searching:
		if index == 0:
			vars.main.current_region = "eu"
		elif index == 1:
			vars.main.current_region = "usa"
		elif index == 2:
			vars.main.current_region = "aus"
		elif index == 3:
			vars.main.current_region = "asia"
		elif index == 4:
			vars.main.current_region = "sa"
		
		print("Region is now " + str(vars.main.current_region))
		vars.main.save_settings()
