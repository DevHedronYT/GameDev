extends Control


func _on_Start_pressed():
	$Click.play()
	get_tree().change_scene("res://Scenes/World.tscn")
	pass # Replace with function body.


func _on_Quit_pressed():
	$Click.play()
	get_tree().quit()
	pass # Replace with function body.
