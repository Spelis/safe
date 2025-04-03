import func


@func.command
def help():
    """Help command. shows this message"""
    for i in func.commands.values():
        print(
            f"{i.name}\n  {i.help}{"\n" if len(i.args) > 0 else ""}  {", ".join(i.args)}"
        )
