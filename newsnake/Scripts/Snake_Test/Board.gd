extends Node2D

var grid_size = Vector2i(25, 25)  # Size of the grid
var _window
var buffer_percentage = 0.05  # Screenspace buffer from grid
var cell_size = 0
var grid_position

func _ready():
	_window = get_viewport().get_window()
	
	RenderingServer.set_default_clear_color(Color(0.233, 0, 0.821)) # A shade of purple I like
	
	#  Add a food supply manager
	var feeder = Node2D.new()
	feeder.name = "Feeder"
	feeder.set_script(load("res://Feeder.gd"))
	add_child(feeder)
	#feeder.spawn_food()

# Function to draw the grid
func _draw():
	var screen_size = _window.size  # Returns Vector2i
	screen_size = Vector2(screen_size.x, screen_size.y)  # Convert to Vector2 for compatibility

	# Calculate the buffer size
	var buffer_size = screen_size * buffer_percentage
	var grid_area_size = screen_size - 2 * buffer_size

	# Calculate the cell size to ensure grid fits the window and cells are square
	cell_size = min(grid_area_size.x / grid_size.x, grid_area_size.y / grid_size.y)
	
	# Calculate the new grid position considering the buffer
	grid_position = buffer_size + (grid_area_size - Vector2(grid_size.x * cell_size, grid_size.y * cell_size)) / 2
	
	# Draw the grid
	var rect_size = Vector2(cell_size, cell_size)
	for x in range(grid_size.x):
		for y in range(grid_size.y):
			var rect_position = grid_position + Vector2(x * cell_size, y * cell_size)
			draw_rect(Rect2(rect_position, rect_size), Color(0.67, 0, 0))
