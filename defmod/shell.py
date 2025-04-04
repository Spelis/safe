import func


@func.command
def clear():
    """Clears the screen"""
    print("\033c", end="")


@func.command
def alias(name: str, command: str):
    """Alias a command"""
    func.commands[name] = func.commands[command]
