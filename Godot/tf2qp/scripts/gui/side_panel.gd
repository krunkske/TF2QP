extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$Panel/VBoxContainer/play.grab_focus()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_play_pressed() -> void:
	vars.main.switch_tabs(0)


func _on_config_pressed() -> void:
	vars.main.switch_tabs(1)


func _on_settings_pressed() -> void:
	vars.main.switch_tabs(2)


func _on_about_pressed() -> void:
	vars.main.switch_tabs(3)
