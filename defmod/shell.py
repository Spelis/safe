import completiontypes as ct
import func


@func.command
def clear():
    """Clears the screen"""
    print("\033c", end="")


@func.command
def alias(name: str, command: ct.Command):
    """Alias a command"""
    func.commands[name] = func.commands[command]
    func.commands[name].name = name
