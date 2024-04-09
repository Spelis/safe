# SAFE: Slow As F**k Editor

A really stupid text editor with a shell like environment to edit files just as if you're in a real shell. which in turn makes text editing really slow or really fast depending on what you use it for, but will be slow to use most of the time

as of right now it doesnt have syntax highlighting and most likely never will as its meant to be stupid

# Commands:
### insert:
ARGS: index,string

Inserts a string at a line index
### edit:
ARGS: index,string

Replaces a specific line by index
### cat:
ARGS: None

Prints out the current buffer
### cls or clear:
ARGS: None

Clears the screen
### save:
ARGS: None

Saves the file with the current filename
### setfilename:
ARGS: filename

Sets the filename to be used with the save command

### exit:
ARGS: None

Exits the program (wont save!!!)

### debug:
ARGS: None

Toggles debug mode (print full python tracebacks)

### info:
ARGS: None

Shows some info about the file if the file has a filename