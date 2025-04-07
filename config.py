import func

func.prompt = "$savestatus$bytes $filename: "
# $curkan # if kanbans are enabled
func.config.exec("alias", "x", "exit")
func.config.exec("alias", "cls", "clear")

# kanban plugin example
# func.config.exec("loadplugin", "kanban")
# func.config.exec("kanban.create", "Hello")
