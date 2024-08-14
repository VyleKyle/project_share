extends Sprite2D

@onready var tween = self.create_tween()
@onready var timer = $Timer

#  Drift values
var _horizontal_values = [30, 40, 50, 60, 70, 80, 90, 100, 125]
var horizontal = _horizontal_values[randi() % _horizontal_values.size()]

var _horizontal_alternators = [1, -1]
var horizontal_alternator = _horizontal_alternators[randi() % _horizontal_alternators.size()]

var _up_values = [75, 100, 125, 150, 175, 200]
var up = -_up_values[randi() % _up_values.size()]


func _ready():
	animate()
	
	# Start the timer to delete the node after the animation
	timer.wait_time = 1.5
	timer.one_shot = true
	timer.connect("timeout", _on_Timer_timeout)
	timer.start()

func animate():
	
	# Start the tween animation for floating and fading out
	
	tween.set_parallel(true)
	tween.tween_property(self, "position:y", up, 1.5).set_ease(Tween.EASE_IN_OUT).as_relative().set_trans(Tween.TRANS_LINEAR)
	tween.tween_property(self, "position:x", horizontal * horizontal_alternator, 1.5).set_ease(Tween.EASE_IN_OUT).as_relative()
	tween.tween_property(self, "position:x", horizontal * (-horizontal_alternator), 1.5).set_ease(Tween.EASE_IN_OUT).as_relative().set_delay(0.5)
	tween.tween_property(self, "position:x", horizontal * horizontal_alternator, 1.5).set_ease(Tween.EASE_IN_OUT).as_relative().set_delay(1)
	tween.tween_property(self, "modulate:a", 0, 1.5)

func _on_Timer_timeout():
	queue_free()
