extends Area2D

func _physics_process(delta):
	Global.dead = false
	var bodies = get_overlapping_bodies()
	for body in bodies:
		if body.name == "Enemy":
			Global.dead = true
			
