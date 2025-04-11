import completiontypes as ct
import func
import os

@func.globalcommand()
def clear():
    """Clears the screen"""
    print("\033c", end="")


@func.globalcommand()
def alias(name: str, command: ct.Command):
    """Alias a command"""
    func.commands[name] = func.commands[command]
    func.commands[name].name = name


@func.globalcommand()
def debug(enabled: bool = None):
    if enabled is None:
        enabled = not func.debug
    print(("enabled" if enabled else "disabled") + " debug mode")

@func.globalcommand()
def cd(dir:str=None):
    if dir == None:
        print(os.getcwd())
        return
    if os.path.exists(dir):
        os.chdir(dir)
    else:
        print("Invalid directory.")

@func.globalcommand("ls")
def listdir(path: ct.File = None):
    if path is None:
        path = os.getcwd()
    for i in os.listdir(path):
        if os.path.isdir(i):
            print(f"{i}/")
        else:
            print(i)
