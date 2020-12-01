extends KinematicBody2D

const up = Vector2 (0 ,-1)
var gravity = 20
const acceleration = 300
const jumpheight = -500
var motion = Vector2()
var jumpcount = 0
const dashspeed = 1000
const superjumpheight = -1000
var rng = RandomNumberGenerator.new()
var score = 0

# warning-ignore:unused_argument
func _physics_process(delta):
	motion.y += gravity
	get_tree().paused = false
	
	for i in get_slide_count():
			var collision = get_slide_collision(i)
			if collision.collider.name == "out":
				$Jump3.play()
				get_tree().reload_current_scene()	
					
	
	if Input.is_action_pressed("right"):
		motion.x += 5
		$Sprite.flip_h = false
		$Sprite.play("moving")

	elif Input.is_action_pressed("left"):
		motion.x -= 5
		$Sprite.flip_h = true
		$Sprite.play("moving")
		
			
	else:
		if $Sprite.flip_h == true:
			motion.x -= 1
		elif $Sprite.flip_h != true:
			motion.x += 1
		$Sprite.play("default")
		
	
	if is_on_floor():
		
		if Input.is_action_pressed("jump"):
			rng.randomize()
			var my_random_number = rng.randi_range(1,10)
			
			if my_random_number < 5:
				motion.y = jumpheight
				jumpcount += 1
				$Jump.play()
				
			elif my_random_number > 5:
				motion.y = superjumpheight
				jumpcount += 1
				$Jump2.play()	
			
			
	else:
		#440 and -440 x axis, y axis = 200  and -200
		
		
		$Sprite.play("jump")		
		gravity = 20	
	
		
	if Input.is_action_just_pressed("rload"):
		get_tree().reload_current_scene()
		
	if Input.is_action_just_pressed("closemenu"):
		get_tree().change_scene("res://Menu.tscn")
					
	motion = move_and_slide(motion, up)
	pass

