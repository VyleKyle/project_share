extends Node2D

var direction = Vector2.RIGHT
var body = []
var parent

func _ready():
	parent = get_parent()
	
	# Initialize the snake's body with one segment (the head)
	body.append(Vector2(0, 0))  # Initial position (can be changed)
	
	# Set the timer for movement
	var timer = Timer.new()
	timer.set_wait_time(0.25)
	timer.connect("timeout", _move)
	add_child(timer)
	timer.start()
	
	# Initial drawing
	queue_redraw()

func _input(event):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			
			KEY_UP:
				if direction != Vector2.DOWN:
					direction = Vector2.UP
			KEY_W:
				if direction != Vector2.DOWN:
					direction = Vector2.UP
					
			KEY_DOWN:
				if direction != Vector2.UP:
					direction = Vector2.DOWN
			KEY_S:
				if direction != Vector2.UP:
					direction = Vector2.DOWN
					
			KEY_LEFT:
				if direction != Vector2.RIGHT:
					direction = Vector2.LEFT
			KEY_A:
				if direction != Vector2.RIGHT:
					direction = Vector2.LEFT
					
			KEY_RIGHT:
				if direction != Vector2.LEFT:
					direction = Vector2.RIGHT
			KEY_D:
				if direction != Vector2.LEFT:
					direction = Vector2.RIGHT
			KEY_B:
				parent.get_node("Feeder").spawn_food()

func _move():
	print(body[0])
	var head_pos = body[0] + direction
	
	head_pos.x = int(clamp(head_pos.x, 0, parent.grid_size.x - 1))
	head_pos.y = int(clamp(head_pos.y, 0, parent.grid_size.y - 1))
	
	var feeder = parent.get_node("Feeder")
	if head_pos in feeder.food_items:
		# Grow
		body.insert(0, head_pos)
		
		# Eat the food, replace it
		feeder.remove_food(head_pos)
		feeder.spawn_food()
	else:
		body.insert(0, head_pos)
		body.pop_back()
	queue_redraw()


func _draw():
	var cell_size = parent.cell_size
	var grid_position = parent.grid_position
	
	# Draw the snake
	for segment in body:
		var rect_position = grid_position + segment * cell_size
		draw_rect(Rect2(rect_position, Vector2(cell_size, cell_size)), Color(0, 1, 0))
