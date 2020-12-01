extends Node2D

onready var Player = get_tree().get_root().get_child(0).get_node("Player")
const scn_ground = preload("res://StaticTiles.tscn")
const fire = preload("res://Enemy.tscn")
var LastBlock
const ground_width = 10

func _ready():
	spawn_ground()
	go_next_pos()
	
func _process(delta):
	
	if Player.position.distance_to(Vector2(LastBlock.position)) < 10000:
		spawn_ground()
		go_next_pos()


func spawn_ground():
	var new_ground = scn_ground.instance()
	new_ground.position = position
	get_node("Container").add_child(new_ground)
	LastBlock = new_ground
	pass
	
func go_next_pos():
	position = position + Vector2(ground_width, 0)	
	pass
