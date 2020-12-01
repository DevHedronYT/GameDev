extends Control



func _on_Button_pressed():
	$Click.play()
	get_tree().change_scene("res://Scenes/World.tscn")
	pass # Replace with function body.
	
func _ready():
	$Label2.set_text("Your Score Was: " + str(Global.Score))
