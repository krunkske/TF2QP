extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_key_link_pressed() -> void:
	OS.shell_open("https://steamcommunity.com/dev/apikey")


func _on_save_pressed() -> void:
	vars.API_KEY = $Panel/HBoxContainer/VBoxContainer/LineEdit.text
	vars.main.save_settings()
	self.hide()
