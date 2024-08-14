extends Node2D

func _ready():
	queue_redraw()

func _draw():
	# Draw the food
	var board = get_parent().get_parent()  # Assuming FoodManager is a direct child of Board
	var cell_size = board.get_cell_size()
	draw_rect(Rect2(Vector2(), Vector2(cell_size, cell_size)), Color(0, 1, 0))
