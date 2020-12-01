extends Control



func _on_Button_pressed():
	$Click.play()
	get_tree().change_scene("res://Scenes/World.tscn")
	Global.score = 0 
	pass # Replace with function body.


func _on_Button2_pressed():
	$Click.play()
	get_tree().quit()
	pass # Replace with function body.
