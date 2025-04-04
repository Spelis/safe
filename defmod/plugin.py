from difflib import get_close_matches

import completiontypes as ct
import func


@func.command
def help(command: ct.Command = ""):
    """Help command. shows this message"""
    if not command:
        for i in func.commands.values():
            print(
                f"{i.name} - {i.file}:{i.line}\n  {i.help}{"\n" if len(i.args) > 0 else ""}  {", ".join(i.args)}"
            )
    else:
        try:
            i: func.FnMeta = func.commands[command]
            print(
                f"{i.name} - {i.file}:{i.line}\n  {i.help}{"\n" if len(i.args) > 0 else ""}  {", ".join(i.args)}"
            )
        except KeyError as e:
            try:
                print(
                    f"command '{command}' doesnt exist. did you mean {get_close_matches(command,list(func.commands.keys()),1)[0]}?"
                )
            except:
                print(f"command '{command}' doesnt exist")


# @func.command
# def loadplugin(filename: ct.File):
#    pass
