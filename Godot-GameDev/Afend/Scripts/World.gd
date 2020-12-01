extends Node2D

var enemy = preload("res://Scenes/Enemy.tscn")

func _ready():
	Global.world = self
	
func _exit_tree():
	Global.world = null
	
func instance_node(node, location):
	var node_instance = node.instance()
	add_child(node_instance)
	node_instance.global_position = location
	pass
			


func _on_EnemySpawnTime_timeout():
	var enemy_position = Vector2(rand_range(1400, 1600), rand_range(70, 120))
	if Global.enemy_spawned < Global.enemy_max_spawned:
		instance_node(enemy, enemy_position)
		Global.enemy_spawned += 1
	pass # Replace with function body.
