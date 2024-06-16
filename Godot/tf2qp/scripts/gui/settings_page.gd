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
