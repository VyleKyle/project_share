extends Control

var gold = 0
var gold_per_click = 1
var upgrade_cost = 5
var upgrade_gps_cost = 8
var gold_per_second = 0.5

@onready var mine_button = $MineButton
@onready var gold_label = $GoldLabel
@onready var upgrade_button = $UpgradeButton
@onready var upgrade_cost_label = $UpgradeCostLabel
@onready var auto_mine_timer = Timer.new()
@onready var upgrade_gps_button = $UpgradeGPSButton
@onready var upgrade_gps_label = $UpgradeGPSLabel
@onready var gps_label = $GPSLabel
@onready var gold_per_click_label = $GPCLabel
@onready var gold_bar_sprite = load("res://Assets/Prefabs/gold_bar_sprite.tscn")

func _ready():
	mine_button.text = "Mine Gold"
	mine_button.pressed.connect(self._on_MineButton_pressed)
	
	upgrade_button.text = "Upgrade"
	upgrade_button.pressed.connect(self._on_UpgradeButton_pressed)
	
	auto_mine_timer.wait_time = 1
	auto_mine_timer.connect("timeout", self._on_AutoMineTimer_timeout)
	add_child(auto_mine_timer)
	auto_mine_timer.start()
	
	upgrade_gps_button.text = "Upgrade Gold per Second"
	upgrade_gps_button.pressed.connect(self._on_UpgradeGPSButton_pressed)
	
	_update_ui()

func _on_MineButton_pressed():
	var cursor_pos = get_viewport().get_mouse_position()
	var gold_bar = gold_bar_sprite.instantiate()
	gold_bar.position = cursor_pos
	add_child(gold_bar)
	
	gold += gold_per_click
	_update_ui()

func _on_UpgradeButton_pressed():
	if gold >= upgrade_cost:
		gold -= upgrade_cost
		gold_per_click += gold_per_click * 0.4
		upgrade_cost = upgrade_cost * 1.5
		_update_ui()

func _on_AutoMineTimer_timeout():
	gold += gold_per_second
	_update_ui()

func _on_UpgradeGPSButton_pressed():
	if gold >= upgrade_gps_cost:
		gold -= upgrade_gps_cost
		gold_per_second += gold_per_second * 0.6
		upgrade_gps_cost = int(upgrade_gps_cost * 1.5)
	_update_ui()

func _update_ui():
	gold_label.text = "Gold: " + str("%.2f" % gold)
	gps_label.text = "Gold per Second: " + str("%.2f" % gold_per_second)
	upgrade_cost_label.text = "Upgrade Cost: " + str("%.2f" % upgrade_cost)
	upgrade_gps_label.text = "Upgrade Cost: " + str("%.2f" % upgrade_gps_cost)
	gold_per_click_label.text = str("Gold per Click: " + str("%.2f" % gold_per_click))
