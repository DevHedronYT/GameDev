extends KinematicBody2D

var up = Vector2(0, -1)
var move = 1500
var motion = Vector2()
var jump_height = -700
var gravity = 10
var bullet = preload("res://Scenes/Bullet.tscn")
var can_shoot = true

func _ready():
	Global.player = self
	
func _exit_tree():
	Global.player = null	

func _physics_process(delta):

	motion.y += gravity

	
	
	motion.x = move
	$Sprite.flip_h = false
	$Sprite.play("moving")
	
	if motion.x == 0:
		$Sprite.play("idle")
		
	if Input.is_action_pressed("restart"):
		get_tree().reload_current_scene()
		
	if Input.is_action_pressed("menuorquit"):
		get_tree().change_scene("Control.tscn")	
		
	if Input.is_action_pressed("shoot") and Global.node_creation_parent != null and can_shoot:
		if $Sprite.flip_h == false:
			Global.instance_node(bullet, global_position + Vector2(0, -20), Global.node_creation_parent)
		if $Sprite.flip_h == true:
			Global.instance_node(bullet, global_position + Vector2(0 , -20), Global.node_creation_parent)
		$Shoot.play()	
		$Timer.start()

		can_shoot = false
	
	if is_on_ceiling():
		$Sprite.flip_v = true
	
	if is_on_floor():
		$Sprite.flip_v = false	
	
	if is_on_floor() or is_on_ceiling():
		if Input.is_action_pressed("jump"):
			$Jump.play()
			motion.y = jump_height
			$Sprite.play("shoot")
	
	if !is_on_floor():
		$Sprite.play("jump")		
		motion.y += gravity
		
	move_and_slide(motion, up)		
			



func _on_Timer_timeout():
	can_shoot = true
	pass # Replace with function body.
