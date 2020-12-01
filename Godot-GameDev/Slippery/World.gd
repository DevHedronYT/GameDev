extends Node2D

func _ready():
	Global.world = self
	
func _exit_tree():
	Global.world = null



func instance_node(node, location):
	var node_instance = node.instance()
	add_child(node_instance)
	node_instance.global_position = location
	pass # Replace with function body.
