extends Label

func _ready():
	self.text = "Score: " + str(Global.score)
