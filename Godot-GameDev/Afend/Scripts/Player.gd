extends KinematicBody2D

var gravity = 20
const up = Vector2(0, -1)
var motion = Vector2()
var acceleration = 400
var jump_height = -600
var dash = 800
var super_jump_height = -800 
var rng = RandomNumberGenerator.new()
var isattacking = false


func _physics_process(delta):
	motion.y += gravity 
	isattacking = false
	$Attack/Atack.disabled = true
	
	if Input.is_action_pressed("attack"): 
		if $Sprite.flip_h == true:
			$Attack.position = Vector2(-53.087, -42.228)
			$Attack.rotation_degrees = 85.2
			$Attack/Atack.disabled = false
			isattacking = true
			$Sprite.play("slash")
			get_node("AttackSound").play()
		else:
			$Attack.position = Vector2(31.369, -43.837)
			$Attack.rotation_degrees = 0
			$Attack/Atack.disabled = false
			isattacking = true
			$Sprite.play("slash")
			$AttackSound.play()
	
	for i in get_slide_count():
		var collision = get_slide_collision(i) 
		if collision.collider.name == "Enemy":
			get_tree().change_scene("res://Scenes/Retry.tscn")
			
						
	if Input.is_action_pressed("move_left") && isattacking == false:
		motion.x = -acceleration
		$Sprite.flip_h = true
		$Sprite.play("move")
	
	elif Input.is_action_pressed("move_right") && isattacking == false:
		motion.x = acceleration
		$Sprite.flip_h = false
		$Sprite.play("move")
	
	else:
		if isattacking == false:	
			$Sprite.play("default")	
		motion.x = 0	
	
	if is_on_floor():
		if Input.is_action_pressed("jump") && isattacking == false:
			rng.randomize()			
			var my_random_number = rng.randi_range(1,10)
			$JumpSound.play() 
			
			if my_random_number < 5:
				motion.y = jump_height
				$Sprite.play("jump")
				
			elif my_random_number > 5:
				motion.y = super_jump_height
				$Sprite.play("jump")
	
	
	if !is_on_floor():
		$Sprite.play("jump")		
		
	if Input.is_action_pressed("restart"):
		get_tree().reload_current_scene()	
	
	if Input.is_action_pressed("Menu_or_Close"):
		get_tree().change_scene("res://Scenes/Menu.tscn")
	
	
	move_and_slide(motion, up)

		


#func _on_Sprite_animation_finished():
	#if $Sprite.animation == "slash" && $Sprite.flip_h == true:
		#$Attack/Atack.disabled = true
		#isattacking = false
	
	#if $Sprite.animation == "slash" && $Sprite.flip_h == true:
		#$Attack2/Atack.disabled = true
		#isattacking = false	
		
	#pass # Replace with function body.










