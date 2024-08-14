extends Node2D

var food_items = []

# Called when the node enters the scene tree for the first time.
func _ready():
	randomize()

func spawn_food():
	var board = get_parent()
	var grid_size = board.grid_size
	var cell_size = board.cell_size
	
	# Generate a random position within the grid
	var food_position = Vector2(randi() % grid_size.x, randi() % grid_size.y)
	
	# Ensure the position doesn't overlap with existing food or the snake
	while food_position in food_items or food_position in board.get_node("Snake").body:
		food_position = Vector2(randi() % grid_size.x, randi() % grid_size.y)
	
	# Create a new food item
	var food = Node2D.new()
	food.set_script("res://Food.gd")
	food.position = food_position
	add_child(food)
	food_items.append(food_position)
	
	# Convert grid position to pixel position
	var grid_position = board.grid_position
	var pixel_position = grid_position + food_position * cell_size
	
	# Update the position of the food
	food.set_position(pixel_position)

func remove_food(food_position):
	food_items.erase(food_position)
	for food in get_children():
		if food.position == food_position:
			food.queue_free()
			break

func _draw():
	for food_position in food_items:
		var grid = get_parent()
		var cell_size = grid.get_cell_size()
		var grid_position = grid.get_grid_position()
		var pixel_position = grid_position + food_position * cell_size
		draw_rect(Rect2(pixel_position, Vector2(cell_size, cell_size)), Color(0, 1, 0))
