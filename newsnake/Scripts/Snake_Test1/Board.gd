extends Node2D

# Cell types
const EMPTY = 0
const SNAKE = 1
const FOOD = 2

# Colors for the cell types
const COLORS = {
	EMPTY: Color(0.67,0,0),
	SNAKE: Color(0,1,0),
	FOOD: Color(1,0,0)
}

# Pre-baked dicts
const TYPES = {
	EMPTY: {"type": EMPTY, "color": COLORS[EMPTY]},
	SNAKE: {"type": SNAKE, "color": COLORS[SNAKE]},
	FOOD: {"type": FOOD, "color": COLORS[FOOD]}
}

@onready var _window = get_viewport().get_window()
@onready var move_timer = Timer.new()
@onready var score_label = Label.new()
var grid_size = Vector2i(100, 100)  # Size of the grid
var buffer_percentage = 0.05  # Screenspace buffer from grid
var cell_size = 0
var grid_position
var snake_body = []
var direction = Vector2.RIGHT
var next_direction = Vector2.RIGHT  # Direction change buffer, to prevent 180's
var board = []
var score = 0
var snake_speed = 0.15  # Measured in seconds per movement

func _ready():
	RenderingServer.set_default_clear_color(Color(0.233, 0, 0.821)) # A shade of purple I like
	
	# Initialize board
	for x in range(grid_size.x):
		var column = []
		for y in range(grid_size.y):
			column.append({"type": EMPTY, "color": COLORS[EMPTY]})
		board.append(column)
	
	# Initialize snake
	var initial_pos = Vector2(randi() % grid_size.x, randi() % grid_size.y)
	snake_body.append(initial_pos)
	board[initial_pos.x][initial_pos.y] = {"type": SNAKE, "color": COLORS[SNAKE]}
	
	# Set the timer for movement
	move_timer.set_wait_time(snake_speed)
	move_timer.connect("timeout", _move_snake)
	add_child(move_timer)
	move_timer.start()
	
	# Spawn initial food
	spawn_food()
	
	# Create and initialize the score label
	score_label.text = "Score: " + str(score)
	score_label.text = "Score: " + str(score)
	score_label.set_h_size_flags(Control.SIZE_EXPAND_FILL)
	score_label.set_v_size_flags(Control.SIZE_SHRINK_CENTER)
	score_label.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT, Control.PRESET_MODE_KEEP_SIZE)
	score_label.anchor_left = 0.01
	score_label.anchor_right = 0.25
	score_label.anchor_top = 0.01
	score_label.anchor_bottom = 0.1
	add_child(score_label)
	
	# Initial drawing
	queue_redraw()

# Function to draw the grid
func _draw():
	var screen_size = Vector2(_window.size)

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
			var cell = board[x][y]
			draw_rect(Rect2(rect_position, rect_size), cell["color"])

func spawn_food():
	# Generate a random position within the grid
	var food_position = Vector2(randi() % grid_size.x, randi() % grid_size.y)
	
	# Ensure the position doesn't overlap with existing food or the snake
	while board[food_position.x][food_position.y]["type"] != EMPTY:
		food_position = Vector2(randi() % grid_size.x, randi() % grid_size.y)
	
	board[food_position.x][food_position.y] = TYPES[FOOD]
	queue_redraw()

func _move_snake():
	direction = next_direction
	var head_pos = snake_body[0] + direction
	
	# Check for collisions with the body or out of bounds
	if head_pos.x < 0 or head_pos.x >= grid_size.x or head_pos.y < 0 or head_pos.y >= grid_size.y or board[head_pos.x][head_pos.y]["type"] == SNAKE:
		game_over()
		return
	
	if board[head_pos.x][head_pos.y]["type"] == FOOD:
		# Grow the snake
		snake_body.insert(0, head_pos)
		board[head_pos.x][head_pos.y] = TYPES[SNAKE]
		
		score += 1
		score_label.text = "Score: " + str(score)
		
		# Replace the food you ate
		spawn_food()
	else:
		# Move forward
		snake_body.insert(0, head_pos)
		board[head_pos.x][head_pos.y] = TYPES[SNAKE]
		
		# Move the tail
		var tail = snake_body.pop_back()
		board[tail.x][tail.y] = TYPES[EMPTY]
	queue_redraw()

func _input(event):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			
			KEY_UP:
				if direction != Vector2.DOWN:
					next_direction = Vector2.UP
			KEY_W:
				if direction != Vector2.DOWN:
					next_direction = Vector2.UP
					
			KEY_DOWN:
				if direction != Vector2.UP:
					next_direction = Vector2.DOWN
			KEY_S:
				if direction != Vector2.UP:
					next_direction = Vector2.DOWN
					
			KEY_LEFT:
				if direction != Vector2.RIGHT:
					next_direction = Vector2.LEFT
			KEY_A:
				if direction != Vector2.RIGHT:
					next_direction = Vector2.LEFT
					
			KEY_RIGHT:
				if direction != Vector2.LEFT:
					next_direction = Vector2.RIGHT
			KEY_D:
				if direction != Vector2.LEFT:
					next_direction = Vector2.RIGHT
			KEY_B:
				spawn_food()

func game_over():
	print("You died.")
	move_timer.stop()
