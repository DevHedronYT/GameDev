extends Position2D

export(PackedScene) var block
export(int) var grid_size

export(int) var max_blocks
var current_block_number = 0

signal instance_node(node, location)

func _process(delta):
	if Global.world != null:
		if !is_connected("instance_node", Global.world, "instance_node"):
			connect("instance_node", Global.world, "instance_node")
			
	if current_block_number < max_blocks:
		var action = round(rand_range(0,20))
		
		if action > 10:
			global_position.y -= grid_size
			
		if action < 10:
			global_position.y += grid_size	
		
		
		global_position.x += grid_size
		emit_signal("instance_node", block, global_position)
		current_block_number += 1 
	else:
		queue_free()	
