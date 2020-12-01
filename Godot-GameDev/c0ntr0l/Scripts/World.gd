extends Node2D

var enemy = preload("res://Scenes/Enemy.tscn")

func _ready():
	Global.world = self
	Global.node_creation_parent = self
	
func _exit_tree():
	Global.world = null
	Global.node_creation_parent = null
	
func instance_node(node, location):
	var node_instance = node.instance()
	add_child(node_instance)
	node_instance.global_position = location		


func _on_Spawner_timeout():
	var enemy_pos = Vector2(rand_range(1250, 18000), -150)
	Global.instance_node(enemy, enemy_pos, self)
	pass # Replace with function body.
