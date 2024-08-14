extends Control

@onready var vbox_container = $VBoxContainer

func _ready():
	# Scan the 'games' directory for game scenes
	var dir = DirAccess.open("res://Scenes/games/")
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if file_name.ends_with(".tscn"):
				var button = Button.new()
				button.text = file_name
				button.pressed.connect(get_tree().change_scene_to_file.bind("res://Scenes/games/" + file_name))
				button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
				vbox_container.add_child(button)
			file_name = dir.get_next()
		dir.list_dir_end()
