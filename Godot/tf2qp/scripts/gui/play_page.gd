extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_start_pressed() -> void:
	vars.main.get_server_data()


func _on_option_button_item_selected(index: int) -> void:
	vars.main.change_server_type(index)


func _on_spin_box_value_changed(value: float) -> void:
	vars.main.players = value
	if value > 1:
		$Panel/VBoxContainer/HBoxContainer/SpinBox.suffix = "players"
	else:
		$Panel/VBoxContainer/HBoxContainer/SpinBox.suffix = "player"
	$Panel/VBoxContainer/start.grab_focus()
