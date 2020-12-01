extends Sprite


var motion = Vector2(1, 0)
var speed = 5000
var look_once = true

func _physics_process(delta):
	if look_once:
		look_at(get_global_mouse_position())
		look_once = false
	
	global_position += motion.rotated(rotation) * speed * delta


func _on_VisibilityNotifier2D_screen_exited():
	queue_free()
	pass # Replace with function body.
