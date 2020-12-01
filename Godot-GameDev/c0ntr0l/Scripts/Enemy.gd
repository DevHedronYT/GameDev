extends AnimatedSprite


var speed = 600
var hp = 1
var motion = Vector2()
var stun = false

func _physics_process(delta):
	self.play("default")
	if Global.player != null and stun == false:
		motion = global_position.direction_to(Global.player.global_position)
	
	elif stun:
		motion = lerp(motion, Vector2(0, 0), 0.3)
	
	if hp < 1:
		$Destroy.play()
		queue_free()
		Global.score += 1
	
	global_position += motion * speed * delta	


func _on_Area2D_area_entered(area):
	if area.is_in_group("enemy_damager"):
		modulate = Color.black
		motion = -motion * 4
		stun = true
		area.get_parent().queue_free()
		$Timer.start()
		hp -= 1


func _on_Timer_timeout():
	modulate = Color.white
	stun = false




