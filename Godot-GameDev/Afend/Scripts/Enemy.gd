extends KinematicBody2D

onready var Player = get_parent().get_node("Player")

var gravity = 20
const up = Vector2(0, -1)
var motion = Vector2()
var acceleration = 400
var jump_height = -600
var react_time = 400
var direction = 0
var next_direction = 0
var next_direction_time = 0
var dead = false


var target_player_dist = 0

func set_dir(target_dir):
	if next_direction != target_dir:
		next_direction = target_dir
		next_direction_time = OS.get_ticks_msec() + react_time
		

func _physics_process(delta):
	motion.y += gravity 
	
	#for i in get_slide_count():
		#var collision = get_slide_collision(i)
		#if collision.collider.name == "Attack":
			#queue_free()
	
	
	if Player.position.x < position.x - target_player_dist:
		set_dir(-1)
	
	elif Player.position.x > position.x + target_player_dist:
		set_dir(1)

	else:
		set_dir(0)
	
	if OS.get_ticks_msec() > next_direction_time:
		direction = next_direction

	if Player.position.y	< position.y	- target_player_dist and is_on_floor():
		motion.y = jump_height
	
	motion.x = direction * 200
	
	move_and_slide(motion, up)
	
	if Global.dead == true:
		Global.Score += 1
		$Destroy.play()
		self.queue_free()
	
		
		
		
		
		
		
