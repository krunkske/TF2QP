extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	self.hide()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass



func _on_github_pressed() -> void:
	OS.shell_open("https://github.com/krunkske/TF2QP")
