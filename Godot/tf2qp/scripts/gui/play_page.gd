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
