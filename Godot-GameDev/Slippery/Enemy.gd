extends Area2D



func _physics_process(delta):
	var bodies = get_overlapping_bodies()
	for body in bodies:
		if body.name == "Player":
			$Hit.play()
			get_tree().reload_current_scene()
			
	
			
